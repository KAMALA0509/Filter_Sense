from pathlib import Path
import json
from streamlit.testing.v1 import AppTest
root=Path(__file__).resolve().parents[1]
a=AppTest.from_file(str(root/'software'/'app.py'),default_timeout=30).run()
assert not a.exception
count=1
for name in ['Clean filter','Slight clogging','Moderate clogging','Severe clogging','RO deterioration']:
    a.selectbox[0].select(name).run()
    assert not a.exception,name
    count+=1
a.checkbox[0].check().run();assert a.error
count+=1
a.checkbox[0].uncheck().run();assert a.error
count+=1
a.button[0].click().run();assert not a.error
count+=1
a.checkbox[1].check().run();assert a.error
count+=1
(root/'evidence'/'ui_tests.json').write_text(json.dumps({'checks_passed':count,'method':'Streamlit AppTest','scope':'render and scenario/safety interactions; not physical validation'},indent=2))
print('UI checks passed:',count)
# Version 2: all fault paths, reset and geometry views.
a.checkbox[1].uncheck().run();a.button[0].click().run();assert not a.error
count+=1
a.checkbox[2].check().run();assert a.error
count+=1
a.button[0].click().run();assert a.error
count+=1
a.checkbox[2].uncheck().run();assert a.error
count+=1
a.button[0].click().run();assert not a.error
count+=1
for label in ['Assembled','Exploded','System diagram']:
    a.radio[0].set_value(label).run();assert not a.exception
    count+=1
a.selectbox[0].select('Severe clogging').run();a.slider[0].set_value(60).run()
assert a.metric[3].value=='0.0';count+=1
(root/'evidence'/'ui_tests.json').write_text(json.dumps({'checks_passed':count,'method':'Streamlit AppTest','scope':'scenario, safety latch, reset, forecast and geometry-view interactions; not browser pixel or physical validation'},indent=2))
print('Version 2 UI checks passed:',count)
