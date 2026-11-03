from pathlib import Path
import streamlit as st
from core import SCENARIOS, simulate, analyse, forecast, interlock

st.set_page_config(page_title='FilterSense', page_icon='💧', layout='wide')
st.markdown('''<style>
[data-testid="stMetric"] {
 background:var(--secondary-background-color);
 color:var(--text-color);
 padding:18px;border-radius:14px;
 border:1px solid rgba(128,128,128,.3);
}
</style>''', unsafe_allow_html=True)

st.caption('SPARTANS / THIAGARAJAR COLLEGE OF ENGINEERING / ATOMQUEST 2026')
st.title('FilterSense')
st.caption('Version 2 • Works with light and dark themes')
st.subheader('Smart water purifier monitoring system')
st.info('SIMULATED DATA • Concept CAD • Unvalidated lifetime estimates • No physical hardware connected')
scenario = st.sidebar.selectbox('Operating scenario', SCENARIOS, index=2)
day = st.sidebar.slider('Replay day', 6, 60, 40)
seed = st.sidebar.number_input('Simulation seed', 1, 9999, 42)
leak = st.sidebar.checkbox('Inject leak fault')
invalid = st.sidebar.checkbox('Inject sensor fault')
overpressure = st.sidebar.checkbox('Inject overpressure')
reset = st.sidebar.button('Reset safety latch')
st.session_state.setdefault('trip', False)
safety = interlock(leak, invalid, 0.58 if overpressure else 0.36, st.session_state.trip, reset)
st.session_state.trip = safety['trip']
with st.sidebar.expander('How to demonstrate', expanded=False):
    st.write('1. Choose Clean filter. 2. Choose Severe clogging and day 60. 3. Inject leak. 4. Clear leak: shutdown remains. 5. Reset safety latch.')
    st.write('The restriction index is a demo scale. Remaining life is an unvalidated time-to-threshold estimate.')
st.sidebar.caption('To restore forecasts: clear all three fault checkboxes, then Reset safety latch.')
d = analyse(simulate(scenario, int(seed)).iloc[:day + 1])
r = d.iloc[-1]
prediction = forecast(d)
a,b,c,e = st.columns(4)
a.metric('Pre-filter restriction index', f'{r.restriction_index_pct:.0f}%')
b.metric('Differential pressure', f'{r.dp_mpa:.3f} MPa')
c.metric('RO salt rejection', f'{r.rejection_pct:.1f}%')
e.metric('Illustrative days to threshold', 'Unavailable' if safety['trip'] or prediction['days'] is None else f"{prediction['days']:.1f}")
st.caption('Restriction index is an assumed pressure-based scale; it is not measured percentage clogging. Playback days are synthetic operating history.')
if safety['trip']:
    st.error('SIMULATED SHUTDOWN: pump OFF; normally closed valve CLOSED. Forecast suppressed.')
    active_faults = [label for flag,label in [(leak,'leak'),(invalid,'invalid sensor'),(overpressure,'overpressure')] if flag]
    st.write('Active fault: ' + ', '.join(active_faults) if active_faults else 'Fault removed, but the safety latch is still set.')
    st.write('Clear all Inject fault checkboxes in the sidebar, then press Reset safety latch.')
else:
    st.success('Simulated pump ON • Valve OPEN')
    st.write(prediction['reason'])
    if prediction['days'] is not None and prediction['days'] <= 14:
        st.warning('Demo intervention threshold approaching or reached. Inspect the relevant stage; confirm with real measurements before replacement.')
tabs = st.tabs(['Overview','Water and pressure','Prediction and history','CAD and architecture','Replacement and safety'])
with tabs[0]:
    st.line_chart(d.set_index('day')[['restriction_index_pct','rejection_pct','flow_decay_pct']])
    cols=st.columns(3)
    cols[0].metric('Inlet TDS at 25 °C', f'{r.inlet_tds_25_ppm:.0f} ppm')
    cols[1].metric('Inlet turbidity', f'{r.turbidity_ntu:.1f} NTU')
    cols[2].metric('Product flow', f'{r.product_flow_lpm:.3f} L/min')
with tabs[1]:
    st.line_chart(d.set_index('day')[['p1_mpa','p2_mpa','dp_mpa']])
    st.line_chart(d.set_index('day')[['inlet_tds_25_ppm','outlet_tds_25_ppm']])
    st.dataframe(d[['temperature_c','turbidity_ntu','estimated_feed_litres','turbidity_exposure_ntu_l']].tail(10), hide_index=True)
    st.caption('Feed volume is inferred using assumed 30% recovery and 60 active minutes/day. Actual feed exposure requires feed measurement or validated recovery.')
with tabs[2]:
    st.write('Physics-informed threshold forecasting: causal Kalman smoothing and 14-observation linear trends. Earliest forecast crossing sets the displayed estimate.')
    st.dataframe(prediction['details'], hide_index=True)
    st.caption('No confidence interval is claimed. Stable use, baseline and input conditions are assumptions. Validation metrics in the package apply only to synthetic runs.')
    st.dataframe(d, hide_index=True)
    st.download_button('Download simulated CSV', d.to_csv(index=False), 'filtersense_simulated.csv', 'text/csv')
with tabs[3]:
    path = Path(__file__).resolve().parents[1] / 'cad' / 'assembly.png'
    view = st.radio('CAD view', ['Assembled', 'Exploded', 'System diagram'], horizontal=True)
    root = Path(__file__).resolve().parents[1]
    path = {'Assembled':root/'cad'/'assembly.png','Exploded':root/'cad'/'exploded.png','System diagram':root/'docs'/'architecture.png'}[view]
    if path.exists(): st.image(str(path), caption='Concept design / assumed dimensions / physical validation pending')
    for title, filename in [('Download assembled STEP','FilterSense_assembly.step'),('Download exploded STEP','FilterSense_exploded.step')]:
        st.download_button(title, (root/'cad'/filename).read_bytes(), filename, 'application/octet-stream')
    viewer = root/'cad'/'FilterSense_3D_Viewer.html'
    if viewer.exists():
        st.download_button('Download offline interactive 3D viewer', viewer.read_bytes(), viewer.name, 'text/html')
    st.caption('Open the downloaded HTML in your browser to rotate, zoom and switch assembled/exploded geometry. Native SOLIDWORKS mates are not included.')
    st.write('Feed → inlet sensing → NC valve → pump → P1 → sediment → carbon → P2 → RO. Product: TDS + flow. Reject: restrictor → waste tank.')
    st.write('Future sensor interfaces: 5 analogue channels need more than one 4-channel ADS1115, or a separately validated ESP32 ADC channel. Temperature and flow use digital inputs.')
with tabs[4]:
    st.write('1. Follow the purifier manufacturer’s service instructions. 2. Isolate electrical power and water. 3. Depressurise before opening any housing. 4. Fit the exact approved cartridge and seals. 5. Flush and leak-check as specified. 6. Re-establish the clean baseline only after successful service.')
    st.warning('Do not drink experimental or kaolin-dosed water. TDS and turbidity cannot certify microbiological safety. CAD housings are conceptual and must not be fabricated for pressure service without engineering validation.')
    st.write('Physical design intent: pressure-rated bought/borrowed wet components, 24 V DC wet zone, protected enclosed supply outside wet zone, relief device, leak tray, independent pump cut-off and NC valve. These have not been physically tested.')
