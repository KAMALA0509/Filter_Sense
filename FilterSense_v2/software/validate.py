"""Repeatable functional tests and held-out synthetic-run forecasting evaluation."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from core import *
ROOT = Path(__file__).resolve().parents[1]
checks=[]
def check(name, condition):
    assert condition, name
    checks.append(name)
check('25 C compensation', float(compensate(500,25)) == 500)
check('35 C compensation', abs(float(compensate(600,35))-500)<1e-8)
check('Leak closes valve and stops pump', interlock(leak=True)['valve']=='CLOSED' and interlock(leak=True)['pump']=='OFF')
check('Latch persists', interlock(previous_trip=True)['trip'])
check('Reset requires absent fault', interlock(leak=True,reset=True)['trip'])
check('Healthy reset clears latch', not interlock(previous_trip=True,reset=True)['trip'])
check('Invalid input trips', interlock(invalid=True)['trip'])
check('Overpressure trips', interlock(pressure=0.56)['trip'])
frames=[]
for scenario in SCENARIOS:
    d=analyse(simulate(scenario))
    check(scenario+' finite indicators',np.isfinite(d[['dp_mpa','rejection_pct','restriction_index_pct']]).all().all())
    check(scenario+' accumulated exposure monotonic', d.turbidity_exposure_ntu_l.is_monotonic_increasing)
    frames.append(d)
check('Known rejection calculation', abs(analyse(simulate()).iloc[0].rejection_pct-100*(1-simulate().iloc[0].outlet_tds_raw_ppm/simulate().iloc[0].inlet_tds_raw_ppm))<1e-8)
check('Short history abstains', forecast(frames[0].head(3))['days'] is None)
for field,value in [('inlet_tds_raw_ppm',0),('p2_mpa',1),('product_flow_lpm',-1),('temperature_c',np.nan),('assumed_recovery',0)]:
    d=simulate();d.loc[5,field]=value
    try: analyse(d)
    except ValueError: checks.append('Reject invalid '+field)
    else: raise AssertionError(field)
pd.concat(frames).to_csv(ROOT/'data'/'simulated_scenarios.csv',index=False)
# Each complete run is held out. Train pooled regression on other runs, then
# evaluate snapshots from the held-out run. Feature engineering is causal.
features=['dp_smoothed_mpa','flow_ratio','rejection_pct','turbidity_exposure_ntu_l']
records=[]
for run in range(12):
    scenario=['Moderate clogging','Severe clogging','RO deterioration'][run%3]
    d=analyse(simulate(scenario,seed=100+run,days=181))
    reached=(d.dp_smoothed_mpa>=DP_LIMIT)|(d.flow_ratio<=FLOW_LIMIT)|(d.rejection_pct<=REJECTION_LIMIT)
    failure=int(np.flatnonzero(reached)[0])
    for t in [14,21,28,35,42]:
        if t>=failure: continue
        row={k:float(d.iloc[t][k]) for k in features}
        row.update(run=run,day=t,target_days=failure-t,trend_days=forecast(d.iloc[:t+1])['days'])
        records.append(row)
x=pd.DataFrame(records); predictions=[]
for run in sorted(x.run.unique()):
    train=x[x.run!=run];test=x[x.run==run]
    model=LinearRegression().fit(train[features],train.target_days)
    y=np.maximum(0,model.predict(test[features]))
    for (_,row),p in zip(test.iterrows(),y):
        predictions.append({'held_out_run':int(run),'observed_day':int(row.day),'synthetic_true_remaining_days':row.target_days,'regression_days':float(p),'trend_days':row.trend_days})
p=pd.DataFrame(predictions);p.to_csv(ROOT/'evidence'/'held_out_predictions.csv',index=False)
metrics={'scope':'SYNTHETIC ONLY; not real filter-life validation','functional_checks_passed':len(checks),'checks':checks,'held_out_runs':12,'snapshots':len(p),'pooled_regression_mae_days':float(np.mean(abs(p.regression_days-p.synthetic_true_remaining_days))),'dashboard_trend_mae_days':float(np.mean(abs(p.trend_days-p.synthetic_true_remaining_days))),'model_note':'Pooled regression is an evaluation baseline; dashboard uses causal trend model. All run generation families are shared; this is a software consistency test, not evidence of field generalisation.'}
(ROOT/'evidence'/'test_results.json').write_text(json.dumps(metrics,indent=2))
print(json.dumps(metrics,indent=2))
