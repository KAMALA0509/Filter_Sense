# FilterSense engineering decisions

## Source hierarchy
The supplied master prompt is the project brief; official Stage 1 and Stage 2 PDFs are the competition rules. The actual submitted Round 1 abstract was not supplied. Original target claims and detailed BOM cannot be independently confirmed. The installation guide is available, but installed SOLIDWORKS version/add-ins are unknown.

## Equations and assumptions
- Differential pressure: DP=P1-P2. Example: 0.36-0.32=0.04 MPa. Compare at equivalent feed flow/pressure/temperature. Combined pre-filter restriction cannot identify a single failed cartridge.
- Demonstration restriction index: 100*(DP-0.015)/(0.100-0.015), clamped 0–100. At DP=0.0575 MPa it is 50. This is NOT a percentage of blocked pores or remaining capacity.
- Flow ratio=Q/Qclean. With Q=0.15 and Qclean=0.20 L/min, ratio=0.75 and flow decay=25%. Baseline should account for inlet pressure, temperature, membrane and tank backpressure; demo conditions are simplified.
- Salt rejection=100*(1-TDSout/TDSin). 25/500 ppm gives 95%. Do not divide by zero; invalid data must suppress diagnosis.
- Temperature compensation: raw conductivity-equivalent reading/(1+alpha*(T-25)), alpha=0.02 per C as an illustrative coefficient. 600 at 35 C becomes 500 at 25 C. This is not a universal TDS calibration. Do not compensate an already compensated probe output again. Demo inlet/outlet share temperature; physical systems may need two temperature measurements.
- Estimated feed volume=product flow*active minutes/recovery. 0.20 L/min*60 min/0.30=40 L. Turbidity-weighted exposure=sum(NTU*estimated feed litres), e.g. 3 NTU*40 L=120 NTU.L. Turbidity is not universally proportional to solids mass. Feed-flow measurement is preferred; product flow alone does not establish feed exposure.
- Causal scalar Kalman filter smooths DP. It never sees future observations.
- Linear regression on the last 14 samples projects DP, flow ratio and rejection to illustrative limits 0.10 MPa, 0.60 and 90%. The earliest crossing gives remaining time. At DP=0.08 with slope=0.002 MPa/day, remaining=10 days. Flat/non-deteriorating signals abstain. Crossings beyond 365 days are not displayed. These are not manufacturer limits.
- RUL presumes the current trend and usage continue. No confidence band, validated service interval or failure probability is claimed. The dashboard intentionally does not show pseudo-precise “accuracy”.

## Model scope
The dashboard's physics-informed model is interpretable threshold forecasting, not a trained digital twin. Exposure is computed and displayed. A separate pooled regression uses DP, flow ratio, salt rejection and exposure as features in leave-one-run-out evaluation. Every complete run is excluded from its corresponding training fold; preprocessing is causal. Twelve synthetic runs, five snapshots/run, are evaluated. Future threshold crossings define synthetic labels only. The optional gradient-boosted model is deferred: real run-to-failure data would be more valuable than a more complex model of invented data.

## Hydraulic and electronic design intent
Feed tank -> inlet TDS/turbidity/temperature -> normally closed valve -> pump -> P1 -> sediment -> carbon -> P2 -> RO. Product branch -> outlet TDS and product flow -> collection. Reject branch -> appropriate restrictor -> separate waste collection. Add pump high-pressure switch, rated relief, approved check valves and any manufacturer-required suction pre-strainer. Pump location is retained from the brief, but actual pump filtration and dry-run requirements must be verified.

Five analogue signals are proposed: P1, P2, TDSin, TDSout and turbidity. One ADS1115 supports only four single-ended inputs. Use a second ADS1115 at another address, or validate a suitably conditioned ESP32 ADC channel. Sensor supply/output ranges are unspecified. Do not connect a 5 V or higher signal directly to a 3.3 V input. Use manufacturer-compatible conditioning and common reference where appropriate. Flow pulses and DS18B20 use digital interfaces. Driver stages are required for pump and valve; GPIO cannot power them directly.

## Safety state machine
Normal -> fault -> latched shutdown. Leak, invalid sensor or illustrative overpressure causes pump OFF and valve CLOSED. Removing the fault alone does not restart; explicit reset is required. Reset is refused while fault remains. Dashboard has only simulated commands; it does not actuate hardware. A deployed controller needs local independent interlocks, watchdog and fail-closed power-loss behaviour independent of Wi-Fi/dashboard. Code here is not firmware.

## CAD caveats
Housings and ports are geometry concepts, not pressure vessels. No seal grooves, threaded engagement, pressure calculations, material approvals or certification are supplied. Tubes are routing envelopes and do not form sealed hydraulic interfaces. Mounting arrangements require measured vendor parts, support brackets, clearance and interference review. The electronics enclosure is above the wet zone, but ingress protection and separation are unvalidated. Never manufacture these concept housings for pressurised operation. Borrow approved housings instead.

## Free / provided / borrowed / purchased
Free: Python stack and supplied source. Provided: SOLIDWORKS licence per email (not verified activated). Borrowing candidates: college mechanical lab CAD workstation, existing pressure-rated purifier rig, electronics lab ESP32/ADC, calibrated pressure/flow instruments. None is confirmed borrowed. Purchased: none reported. Longest risks: calibrated sensors, pressure-rated fittings, pump, housings, fabrication and time for degradation tests.

## Round 3 validation plan
1. Obtain approved components and supervision; record exact specifications and calibration.
2. Verify water/electrical isolation, pressure relief, independent stop and leak shutoff before testing.
3. Collect repeated clean baselines at controlled pressure, temperature and usage.
4. Record independent full degradation runs across water conditions; never use dosed test water for drinking.
5. Define intervention endpoints with manufacturer limits and measured performance.
6. Validate by complete held-out runs; report MAE in days/litres, uncertainty, false alerts and missed endpoints. Compare with fixed-time/litre baselines.
7. Treat membrane, pre-filter restriction and carbon exhaustion as separate failure modes.

## Documentation references
- User-supplied atomQUEST 2026 Stage 1 and Stage 2 PDFs; Stage 2 due 4 November 2026, 23:59 IST.
- SOLIDWORKS STEP import: https://help.solidworks.com/2024/english/SolidWorks/sldworks/t_reading_step_iges_acis_sw.htm
- Streamlit AppTest: https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest
- ADS1115 datasheet: https://www.ti.com/lit/ds/symlink/ads1115.pdf

SOLIDWORKS Premium is not proof that Flow Simulation is licensed. On the actual installation, inspect Tools > Add-Ins and licence availability. No CFD/FEA result is claimed in this package.

## Version 2 usability changes
Theme-aware cards remove the white-on-white text conflict observed on the user laptop. Default Light theme is supplied, without forcing global CSS colours. Fault messages distinguish an active fault from a retained latch. The offline HTML 3D viewer uses tessellated STEP geometry; it does not provide native SOLIDWORKS parametric editing.
