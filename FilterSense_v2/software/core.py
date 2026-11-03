"""FilterSense: synthetic engineering demonstration, not calibrated diagnostics."""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

SCENARIOS = ['Clean filter', 'Slight clogging', 'Moderate clogging', 'Severe clogging', 'RO deterioration']
DP_LIMIT = 0.10  # MPa: illustrative intervention threshold, not a pressure rating
FLOW_LIMIT = 0.60
REJECTION_LIMIT = 90.0

def compensate(raw, temperature, alpha=0.02):
    """Illustrative conductivity-equivalent correction to 25 C; not for already compensated TDS."""
    divisor = 1 + alpha * (np.asarray(temperature) - 25)
    if np.any(divisor <= 0):
        raise ValueError('Invalid temperature compensation divisor')
    return np.asarray(raw) / divisor

def simulate(scenario='Moderate clogging', seed=42, days=61):
    if scenario not in SCENARIOS or days < 2:
        raise ValueError('Choose a known scenario and at least two days')
    rng = np.random.default_rng(seed)
    day = np.arange(days, dtype=float)
    rate = [0.00012, 0.00055, 0.00105, 0.00165, 0.0002][SCENARIOS.index(scenario)]
    rate *= rng.uniform(0.85, 1.15)
    turbidity = np.clip(rng.normal(3.0, 0.6, days), 0.2, 12)
    temp = 25 + 2 * np.sin(day / 8)
    inlet25 = 450 + rng.normal(0, 10, days)
    dp_true = 0.015 + rate * day
    dp = np.maximum(0, dp_true + rng.normal(0, 0.0007, days))
    p1 = 0.36 + rng.normal(0, 0.001, days)
    flow_ratio = np.clip(1 - 3.8 * (dp_true - 0.015), 0.10, 1)
    rejection = 97 - (0.14 * day if scenario == 'RO deterioration' else 0.006 * day)
    rejection += rng.normal(0, 0.08, days)
    factor = 1 + 0.02 * (temp - 25)
    return pd.DataFrame({
        'timestamp': pd.date_range('2026-01-01', periods=days, freq='D'),
        'day': day, 'run_id': f'{scenario}-{seed}', 'source': 'SIMULATED',
        'inlet_tds_raw_ppm': inlet25 * factor,
        'outlet_tds_raw_ppm': inlet25 * (1 - rejection / 100) * factor,
        'temperature_c': temp, 'turbidity_ntu': turbidity,
        'p1_mpa': p1, 'p2_mpa': p1 - dp,
        'product_flow_lpm': np.maximum(0, 0.20 * flow_ratio + rng.normal(0, 0.0008, days)),
        'clean_flow_lpm': 0.20, 'active_minutes': 60.0,
        'assumed_recovery': 0.30, 'leak': False,
    })

def kalman(values, q=1e-6, r=5e-7):
    values = np.asarray(values, dtype=float)
    x, p, result = values[0], 1.0, []
    for z in values:
        p += q
        gain = p / (p + r)
        x += gain * (z - x)
        p *= (1 - gain)
        result.append(x)
    return np.array(result)

def analyse(df):
    d = df.copy()
    fields = ['day','inlet_tds_raw_ppm','outlet_tds_raw_ppm','temperature_c','turbidity_ntu','p1_mpa','p2_mpa','product_flow_lpm','clean_flow_lpm','active_minutes','assumed_recovery']
    if not np.isfinite(d[fields].to_numpy(dtype=float)).all():
        raise ValueError('Invalid sensor data: non-finite value; shut down simulated pump')
    if (d.inlet_tds_raw_ppm <= 0).any() or (d.outlet_tds_raw_ppm < 0).any():
        raise ValueError('Invalid TDS input')
    if (d.p2_mpa > d.p1_mpa).any() or (d[['p1_mpa','p2_mpa']] < 0).any().any():
        raise ValueError('Pressure ordering or range invalid')
    if (d[['product_flow_lpm','turbidity_ntu','active_minutes']] < 0).any().any() or (d.clean_flow_lpm <= 0).any():
        raise ValueError('Invalid flow, turbidity or duration')
    if (d.assumed_recovery <= 0).any() or (d.assumed_recovery > 1).any():
        raise ValueError('Recovery must be in (0, 1]')
    if not (d.day.diff().dropna() > 0).all():
        raise ValueError('Samples must be ordered with unique increasing days')
    if ((d.temperature_c < 0) | (d.temperature_c > 50)).any():
        raise ValueError('Temperature outside demo range')
    d['dp_mpa'] = d.p1_mpa - d.p2_mpa
    d['dp_smoothed_mpa'] = kalman(d.dp_mpa)
    d['inlet_tds_25_ppm'] = compensate(d.inlet_tds_raw_ppm, d.temperature_c)
    d['outlet_tds_25_ppm'] = compensate(d.outlet_tds_raw_ppm, d.temperature_c)
    d['rejection_pct'] = 100 * (1 - d.outlet_tds_25_ppm / d.inlet_tds_25_ppm)
    d['flow_ratio'] = d.product_flow_lpm / d.clean_flow_lpm
    d['flow_decay_pct'] = 100 * (1 - d.flow_ratio)
    # Product flow alone cannot measure feed volume: assumed recovery is explicit.
    d['estimated_feed_litres'] = d.product_flow_lpm * d.active_minutes / d.assumed_recovery
    d['turbidity_exposure_ntu_l'] = (d.estimated_feed_litres * d.turbidity_ntu).cumsum()
    d['restriction_index_pct'] = np.clip(100 * (d.dp_smoothed_mpa - 0.015) / (DP_LIMIT - 0.015), 0, 100)
    return d

def forecast(d, window=14):
    """Trend regression to assumed limits, evaluated only on observed history."""
    if len(d) < 7:
        return {'days': None, 'reason': 'At least 7 observations required', 'details': []}
    h = d.tail(window)
    candidates, details = [], []
    for field, limit, direction in [('dp_smoothed_mpa',DP_LIMIT,1),('flow_ratio',FLOW_LIMIT,-1),('rejection_pct',REJECTION_LIMIT,-1)]:
        model = LinearRegression().fit(h[['day']], h[field])
        slope = float(model.coef_[0])
        current = float(h[field].iloc[-1])
        if direction * (current - limit) >= 0:
            remaining = 0.0
        elif direction * slope > 1e-6:
            remaining = max(0.0, (limit - current) / slope)
        else:
            remaining = None
        details.append({'indicator': field, 'slope_per_day': slope, 'threshold': limit, 'days': remaining})
        if remaining is not None and remaining <= 365:
            candidates.append((remaining, field))
    if not candidates:
        return {'days': None, 'reason': 'No threshold crossing within the 365-day demo horizon', 'details': details}
    remaining, field = min(candidates)
    return {'days': round(remaining,1), 'reason': f'{field} trend reaches its assumed intervention threshold first', 'details': details}

def interlock(leak=False, invalid=False, pressure=0.36, previous_trip=False, reset=False):
    fault = leak or invalid or not np.isfinite(pressure) or pressure > 0.55 or pressure < 0
    latched = bool(fault or (previous_trip and not reset))
    return {'trip': latched, 'pump': 'OFF' if latched else 'ON', 'valve': 'CLOSED' if latched else 'OPEN', 'reason': 'Fault / latched trip' if latched else 'Normal simulated operation'}
