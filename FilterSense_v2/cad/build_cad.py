"""Reproducible concept geometry in mm. Requires cadquery; no pressure certification."""
from pathlib import Path
import json
import cadquery as cq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parent
(ROOT/'parts').mkdir(exist_ok=True)
parts={}
def box(x,y,z): return cq.Workplane('XY').box(x,y,z,centered=(True,True,False))
def cylinder(r,h): return cq.Workplane('XY').circle(r).extrude(h)
def cup(r,h,w): return cylinder(r,h).cut(cylinder(r-w,h).translate((0,0,w)))
def tray(x,y,z,w): return box(x,y,z).cut(box(x-2*w,y-2*w,z).translate((0,0,w)))
def add(name,shape,pos,color): parts[name]=(shape,pos,color)
add('01_feed_tank',tray(140,130,200,4),(-235,10,12),'#76bbcf')
add('02_sediment_housing',cup(44,270,4),(-65,0,40),'#c4d9e3')
add('03_sediment_cartridge',cq.Workplane('XY').circle(30).circle(10).extrude(240),(-65,0,48),'#ecdfae')
add('04_carbon_housing',cup(44,270,4),(55,0,40),'#c4d9e3')
add('05_carbon_cartridge',cq.Workplane('XY').circle(30).circle(10).extrude(240),(55,0,48),'#354d5a')
add('06_ro_housing',cup(28,310,3).rotate((0,0,0),(0,1,0),90),(-145,25,390),'#9ab2c7')
add('07_ro_membrane',cq.Workplane('XY').circle(22).circle(7).extrude(280).rotate((0,0,0),(0,1,0),90),(-135,25,390),'#dad4c1')
add('08_tube_segment',cq.Workplane('XY').circle(3.175).circle(2).extrude(100),(210,0,30),'#1c9eb0')
add('09_connector',cq.Workplane('XY').circle(8).circle(3.2).extrude(24),(210,0,130),'#0c7186')
add('10_pump_bracket',box(100,65,5).faces('>Z').workplane().pushPoints([(-35,-20),(35,-20),(-35,20),(35,20)]).hole(5),(215,70,12),'#637a8a')
add('11_pressure_sensor_mount',cq.Workplane('XY').circle(15).circle(5).extrude(25),(-125,0,300),'#d6a657')
add('12_tds_sensor_mount',cq.Workplane('XY').circle(12).circle(4).extrude(30),(-220,15,215),'#d6a657')
add('13_turbidity_mount',tray(50,40,45,3),(-220,60,215),'#d6a657')
add('14_flow_sensor_mount',cq.Workplane('XY').circle(16).circle(3.2).extrude(45),(210,0,160),'#d6a657')
add('15_electronics_enclosure',tray(150,90,45,3),(210,65,440),'#397d8e')
add('16_electronics_plate',box(140,80,3).faces('>Z').workplane().pushPoints([(-60,-30),(60,-30),(-60,30),(60,30)]).hole(3),(210,65,444),'#6ba6b6')
add('17_leak_tray',tray(620,260,12,3),(0,0,0),'#2a6175')
stand=box(640,280,6).translate((0,0,-6)).union(box(640,6,540).translate((0,137,0)))
add('18_stand',stand,(0,0,0),'#b1bcc4')
add('19_sediment_cap',cylinder(48,18),(-65,0,310),'#168e9e')
add('20_carbon_cap',cylinder(48,18),(55,0,310),'#168e9e')
add('21_ro_cap',cylinder(31,14).rotate((0,0,0),(0,1,0),90),(165,25,390),'#168e9e')
add('22_pump_envelope',box(90,55,75),(215,70,17),'#436173')
add('23_nc_valve_envelope',box(35,30,45),(-150,-50,20),'#d6a657')
add('24_enclosure_lid',box(150,90,3),(210,65,485),'#265d70')
# Tubes are routing envelopes; interfaces not sealed or pressure detailed.
def tube_between(a,b):
    a,b=cq.Vector(*a),cq.Vector(*b);v=b-a
    return cq.Workplane('XY').newObject([cq.Solid.makeCylinder(3.175,v.Length,a,v.normalized()).cut(cq.Solid.makeCylinder(2,v.Length,a,v.normalized()))])
routes=[((-190,-40,215),(-150,-50,60)),((-150,-50,60),(210,60,95)),((210,60,95),(-110,-15,325)),((-20,-15,325),(10,-15,325)),((100,-15,325),(-145,25,390)),((180,25,390),(210,0,205)),((180,35,390),(280,-70,30))]
for i,(a,b) in enumerate(routes): add(f'route_{i+1:02d}',tube_between(a,b),(0,0,0),'#16a8b8' if i<6 else '#e59640')
assembly=cq.Assembly(name='FilterSense_concept')
exploded=cq.Assembly(name='FilterSense_exploded')
manifest=[]
for i,(name,(shape,pos,color)) in enumerate(parts.items()):
    assert shape.val().isValid(),name
    cq.exporters.export(shape,str(ROOT/'parts'/f'{name}.step'))
    assembly.add(shape,name=name,loc=cq.Location(cq.Vector(*pos)))
    ep=list(pos)
    if 'cartridge' in name or 'cap' in name or 'lid' in name or 'membrane' in name: ep[2]+=140
    if 'housing' in name: ep[1]-=65
    exploded.add(shape,name=name,loc=cq.Location(cq.Vector(*ep)))
    bb=shape.val().BoundingBox()
    manifest.append({'name':name,'position_mm':pos,'size_mm':[round(bb.xlen,2),round(bb.ylen,2),round(bb.zlen,2)],'solid_valid':True,'status':'CONCEPT / ASSUMED DIMENSIONS'})
assembly.save(str(ROOT/'FilterSense_assembly.step'))
exploded.save(str(ROOT/'FilterSense_exploded.step'))
(ROOT/'parts_manifest.json').write_text(json.dumps(manifest,indent=2))
# Tessellated images of actual generated geometry.
for explode in [False,True]:
    fig=plt.figure(figsize=(12,8));ax=fig.add_subplot(111,projection='3d')
    for name,(shape,pos,color) in parts.items():
        offset=list(pos)
        if explode and any(s in name for s in ['cartridge','cap','lid','membrane']): offset[2]+=140
        if explode and 'housing' in name: offset[1]-=65
        verts,faces=shape.val().tessellate(2.5)
        xyz=[(v.x+offset[0],v.y+offset[1],v.z+offset[2]) for v in verts]
        polys=[[xyz[j] for j in f] for f in faces]
        ax.add_collection3d(Poly3DCollection(polys,facecolor=color,edgecolor='none',alpha=0.33 if 'housing' in name or name=='18_stand' else 0.95))
    ax.set(xlim=(-350,350),ylim=(-200,200),zlim=(-20,700 if explode else 550),xlabel='X / mm',ylabel='Y / mm',zlabel='Z / mm')
    ax.set_box_aspect((700,400,720 if explode else 570));ax.view_init(22,-65)
    ax.set_title('FilterSense / '+('exploded concept' if explode else 'assembled concept')+'\nAssumed geometry • Not pressure-rated • Tubing is routing intent',fontsize=14)
    fig.tight_layout();fig.savefig(ROOT/('exploded.png' if explode else 'assembly.png'),dpi=160);plt.close(fig)
print(f'{len(parts)} valid solids/part files and two STEP assemblies created')
