"""Captioned computational demonstration; renders actual core.py outputs, not browser capture."""
from pathlib import Path
import sys,subprocess,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'software'))
from core import simulate,analyse,forecast,interlock
W,H,FPS,DURATION=1280,720,12,86
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def f(size,b=False):return ImageFont.truetype(bold if b else font,size)
BG='#edf4f7';INK='#133748';TEAL='#078994';GRAY='#58727f'
output=ROOT/'docs'/'atomQUEST2026_Spartans_ThiagarajarCollegeOfEngineering_Track2_Video.mp4'
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-movflags','+faststart',str(output)],stdin=subprocess.PIPE)
def wrap(draw,text,x,y,width=1120,size=25,color=INK,b=False):
 words=text.split();line=''
 for word in words:
  candidate=(line+' '+word).strip()
  if draw.textlength(candidate,font=f(size,b))>width:
   draw.text((x,y),line,font=f(size,b),fill=color);y+=size+12;line=word
  else:line=candidate
 draw.text((x,y),line,font=f(size,b),fill=color)
 return y+size+12
def card(draw,x,title,value):
 draw.rounded_rectangle((x,155,x+365,270),radius=14,fill='white')
 draw.text((x+20,172),title,font=f(18),fill=GRAY)
 draw.text((x+20,205),value,font=f(33,True),fill=INK)

def chart(draw,data,field,limit,label,x,y,w=540,h=220):
 draw.rounded_rectangle((x,y,x+w,y+h),radius=12,fill='white')
 draw.text((x+20,y+12),label,font=f(19,True),fill=INK)
 left,top,right,bottom=x+50,y+52,x+w-20,y+h-35
 vmax=max(float(data[field].max())*1.15,limit*1.2);vmin=0
 draw.line((left,top,left,bottom,right,bottom),fill='#9ab0ba',width=2)
 limit_y=bottom-limit/vmax*(bottom-top)
 draw.line((left,limit_y,right,limit_y),fill='#de8b39',width=2)
 draw.text((left+5,limit_y-22),f'Assumed threshold: {limit:g}',font=f(13),fill='#a05a1e')
 pts=[(left+float(row.day)/60*(right-left),bottom-float(row[field])/vmax*(bottom-top)) for _,row in data.iterrows()]
 if len(pts)>1:draw.line(pts,fill=TEAL,width=4)
 draw.text((left,bottom+8),'0',font=f(13),fill=GRAY);draw.text((right-85,bottom+8),'60 days',font=f(13),fill=GRAY)
all_data={s:analyse(simulate(s)) for s in ['Clean filter','Severe clogging','RO deterioration']}
for frame in range(FPS*DURATION):
 t=frame/FPS
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 d.rectangle((0,0,W,105),fill=INK)
 d.text((45,22),'FilterSense',font=f(36,True),fill='white')
 d.text((880,30),'ATOMQUEST 2026 / TRACK 2',font=f(19,True),fill='#a7e4e8')
 d.text((45,76),'Spartans • Thiagarajar College of Engineering',font=f(17),fill='#cae0e8')
 d.rectangle((0,647,W,H),fill=INK)
 d.text((45,665),'SIMULATED OUTPUTS + CONCEPT CAD  |  No physical prototype or validated filter life',font=f(20),fill='white')
 if t<10:
  d.text((60,150),'Replace by condition.',font=f(52,True),fill=INK)
  d.text((60,220),'Understand the evidence.',font=f(46),fill=TEAL)
  wrap(d,'Fixed replacement schedules can miss changing inlet water quality and operating conditions.',60,330,size=30)
  wrap(d,'Our prototype explains pressure, flow and RO performance trends before recommending inspection.',60,450,size=27)
 elif t<23:
  cad=Image.open(ROOT/'cad'/('assembly.png' if t<17 else 'exploded.png')).convert('RGB');cad.thumbnail((755,500));im.paste(cad,(10,115))
  y=150
  for txt in ['CAD development','31 STEP part / routing files','Assembled and exploded geometry','Assumed dimensions','Native SOLIDWORKS verification pending']:
   y=wrap(d,txt,790,y,width=440,size=24,b=(txt=='CAD development'))+18
 elif t<40:
  day=min(60,6+int((t-23)/17*54))
  data=all_data['Severe clogging'].iloc[:day+1];r=data.iloc[-1];pred=forecast(data)
  d.text((45,118),f'Severe restriction scenario / replay day {day}',font=f(23,True),fill=INK)
  card(d,45,'Restriction index (illustrative)',f'{r.restriction_index_pct:.0f}%')
  card(d,455,'Product flow',f'{r.product_flow_lpm:.3f} L/min')
  card(d,865,'Forecast to threshold','Unavailable' if pred['days'] is None else f"{pred['days']:.1f} days")
  chart(d,data,'dp_smoothed_mpa',0.10,'Pressure difference / MPa',45,300)
  chart(d,data,'flow_ratio',0.6,'Flow / clean baseline',660,300)
  wrap(d,'Actual core.py calculations replay synthetic history. Rising pressure loss and falling flow drive the alert.',45,555,size=25)
 elif t<51:
  data=all_data['RO deterioration'];r=data.iloc[-1]
  d.text((45,120),'Separate RO performance monitoring',font=f(27,True),fill=INK)
  card(d,45,'Inlet TDS (25 °C)',f'{r.inlet_tds_25_ppm:.0f} ppm')
  card(d,455,'Outlet TDS (25 °C)',f'{r.outlet_tds_25_ppm:.0f} ppm')
  card(d,865,'RO salt rejection',f'{r.rejection_pct:.1f}%')
  chart(d,data,'rejection_pct',90,'Salt rejection / %',45,300,w=750)
  wrap(d,'RO deterioration can occur without severe pre-filter restriction.',840,330,width=380,size=25)
  wrap(d,'TDS and turbidity do not certify drinking-water safety.',45,560,size=25)
 elif t<65:
  stage=int((t-51)/3.5)
  if stage==0:state=interlock(leak=True);title='1 / Inject leak'
  elif stage==1:state=interlock(previous_trip=True);title='2 / Remove leak: trip remains latched'
  elif stage==2:state=interlock(previous_trip=True,reset=True,leak=True);title='3 / Reset while fault active: refused'
  else:state=interlock(previous_trip=True,reset=True);title='4 / Clear fault and reset: normal'
  d.text((45,116),title,font=f(25,True),fill=INK)
  card(d,45,'Simulated pump command',state['pump'])
  card(d,455,'Simulated valve command',state['valve'])
  card(d,865,'Latched trip',str(state['trip']))
  wrap(d,'Local fail-safe logic: leak, invalid sensor or overpressure stops the pump and closes the valve.',55,340,size=31)
  wrap(d,'These are software commands only. Physical interlocks have not been built or tested.',55,470,size=29,color='#ad5a20')
 elif t<76:
  d.text((55,150),'Completed and tested',font=f(42,True),fill=INK)
  y=240
  for txt in ['Five labelled synthetic scenarios and CSV export','Condition calculations, causal smoothing and dashboard','25 functional checks + 19 dashboard interaction checks','12 held-out synthetic runs; no field-accuracy claim']:
   y=wrap(d,'• '+txt,60,y,size=26)+20
 else:
  d.text((55,150),'Next: physical evidence',font=f(42,True),fill=INK)
  y=240
  for txt in ['Hardware spending reported: INR 0 / ~INR 12,000 planned','Seek approved borrowed rig and calibrated sensors','Verify leak shutdown, pressure protection and clean baseline','Collect independent degradation runs; validate predictions']:
   y=wrap(d,'• '+txt,60,y,size=26)+18
 if frame in [0,300,450,650,950]:im.save(ROOT/'evidence'/f'video_frame_{frame:04d}.png')
 proc.stdin.write(im.tobytes())
proc.stdin.close();assert proc.wait()==0
print(output)
