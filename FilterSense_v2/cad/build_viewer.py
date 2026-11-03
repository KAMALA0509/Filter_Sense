from pathlib import Path
import json
import cadquery as cq
import plotly.graph_objects as go
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'parts_manifest.json').read_text())
traces=[];exploded=[]
for item in manifest:
 name=item['name'];p=item['position_mm']
 shape=cq.importers.importStep(str(ROOT/'parts'/f'{name}.step')).val()
 vertices,triangles=shape.tessellate(1.5)
 x=[v.x+p[0] for v in vertices];y=[v.y+p[1] for v in vertices];z=[v.z+p[2] for v in vertices]
 color='#1c9db0' if 'route' in name or 'cap' in name else '#7896a8'
 if 'cartridge' in name or 'membrane' in name:color='#cfb777'
 trace=go.Mesh3d(x=x,y=y,z=z,i=[a for a,b,c in triangles],j=[b for a,b,c in triangles],k=[c for a,b,c in triangles],name=name,showlegend=True,color=color,opacity=.28 if 'housing' in name or 'stand' in name else 1,hovertemplate=name+'<extra></extra>')
 traces.append(trace)
 shiftz=140 if any(w in name for w in ['cartridge','cap','lid','membrane']) else 0
 shifty=-65 if 'housing' in name else 0
 exploded.append(go.Mesh3d(x=x,y=[v+shifty for v in y],z=[v+shiftz for v in z]))
fig=go.Figure(data=traces,frames=[go.Frame(name='Assembled',data=[go.Mesh3d(x=t.x,y=t.y,z=t.z) for t in traces]),go.Frame(name='Exploded',data=exploded)])
fig.update_layout(title='FilterSense — interactive concept CAD<br><sup>Drag to rotate • Scroll to zoom • Click legend to hide parts • Assumed dimensions, not pressure-rated</sup>',height=850,scene=dict(aspectmode='data',xaxis_title='X / mm',yaxis_title='Y / mm',zaxis_title='Z / mm'),sliders=[dict(steps=[dict(label=name,method='animate',args=[[name],dict(mode='immediate',frame=dict(duration=0,redraw=True),transition=dict(duration=0))]) for name in ['Assembled','Exploded']])],legend=dict(font=dict(size=10)),margin=dict(l=10,r=10,b=80,t=100))
fig.write_html(str(ROOT/'FilterSense_3D_Viewer.html'),include_plotlyjs=True,auto_open=False)
print('Self-contained offline viewer created with',len(traces),'parts and two views')
