from pathlib import Path
import json, textwrap
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'docs';C=ROOT/'cad'
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodySmall',fontName='Helvetica',fontSize=9,leading=13,spaceAfter=7,textColor=HexColor('#243d4a')))
styles['Title'].textColor=HexColor('#123447');styles['Heading2'].textColor=HexColor('#087e8b')
def p(s):return Paragraph(s,styles['BodySmall'])
def heading(s):return Paragraph(s,styles['Heading2'])
def footer(c,d):
 c.setFont('Helvetica',8);c.setFillColor(HexColor('#657882'));c.drawString(40,24,'FilterSense | Spartans | 03 November 2026 | SIMULATED SOFTWARE + CONCEPT CAD');c.drawRightString(555,24,str(d.page))
metrics=json.loads((ROOT/'evidence/test_results.json').read_text())
report=D/'atomQUEST2026_Spartans_ThiagarajarCollegeOfEngineering_Track2_Report.pdf'
story=[Paragraph('FilterSense',styles['Title']),p('<b>Round 2 prototype progress report</b> | Team Spartans | Thiagarajar College of Engineering, Madurai'),p('<b>Track 2: Water Purifier.</b> Primary: prognostics of filter failure using data analytics. Secondary: inlet water quality sensing beyond TDS.'),heading('Problem and proposed solution'),p('Fixed time/litre replacement schedules may not reflect variation in water quality and operating conditions. FilterSense combines differential pressure across the pre-filter train, flow decay, turbidity exposure and RO salt rejection to explain deterioration and estimate time to an intervention threshold.'),heading('Completed and demonstrated'),p('Version 2 removes forced light backgrounds to preserve text contrast across themes, adds guided reset instructions and an offline interactive 3D viewer. A runnable Streamlit software prototype includes five labelled synthetic scenarios, history replay, CSV export, sensor cards, pressure/flow/TDS plots, causal Kalman smoothing, threshold forecasts and replacement guidance. Leak, invalid-sensor and overpressure fault controls demonstrate latched pump-OFF/valve-CLOSED logic; this is simulation only.'),p('CAD deliverables include 31 STEP part/routing files, an assembled STEP, an exploded STEP, actual geometry renders and dimensioned concept reference sheets. CAD uses assumed dimensions; native SOLIDWORKS import, mating, interference review, fabrication and pressure validation remain pending. The user has confirmed the dashboard opens on their laptop.'),Image(str(C/'assembly.png'),width=310,height=207),p('<b>Evidence:</b> 25 functional checks and 19 Streamlit interaction checks passed in the development environment. Twelve synthetic held-out runs (60 snapshots) were evaluated. Dashboard trend MAE: %.2f days; pooled regression baseline MAE: %.2f days. These are synthetic consistency results, not real-world accuracy.'%(metrics['dashboard_trend_mae_days'],metrics['pooled_regression_mae_days'])),PageBreak(),heading('Costs, sourcing and changes'),p('<b>Reported hardware spending: INR 0 / approximately INR 12,000 planned</b>, based on the supplied project brief. No hardware purchases or laboratory loans are confirmed. Sensor calibration, pressure-rated housings/fittings, pump availability and physical test time are the principal sourcing/execution risks. Proposed next source: existing college laboratory equipment or a supervised borrowed purifier rig.'),p('<b>Change in execution:</b> physical build is deferred because no hardware is available and the team cannot fund the complete setup. This round demonstrates CAD plus software. Revised claim: the prototype computes and explains simulated condition indicators and time-to-threshold estimates; it does not establish actual remaining filter life.'),p('Design review adds the RO reject route and identifies the need for an additional ADC input: the five proposed analogue signals exceed one ADS1115. Estimated feed exposure uses an explicit recovery assumption because product-flow measurement alone is insufficient. P1/P2 diagnose combined restriction, not individual sediment/carbon failure.'),p('<b>Source limitation:</b> the actual submitted Round 1 abstract was not available during preparation. The supplied master brief was used for project details and original cost; team review against the submitted abstract remains pending.'),heading('Safety and fail-safe status'),p('Software interlock tests cover leak trip, invalid input, overpressure, latch persistence and reset refusal while fault remains. No physical valve, pump, sensor, pressure relief or electrical protection has been tested. Physical intent: approved pressure-rated wet components, 24 V DC wet zone, protected enclosed supply outside wet zone, leak tray, independent pressure protection and fail-closed valve.'),p('Concept housings are not manufacture-ready pressure vessels. Test water must not be consumed. TDS/turbidity measurements do not certify drinking-water safety. Safety-critical control must remain local and independent of the dashboard.'),heading('Round 3 plan'),p('Obtain approved borrowed hardware; verify exact dimensions/interfaces; calibrate sensors and establish clean baselines; verify local safety functions under supervision; collect repeated full degradation runs with measured endpoints; validate on complete held-out physical runs and report errors, false alerts and uncertainty against fixed-time/litre baselines.'),heading('Submission status'),p('Prepared deliverables: report, source/CAD package, video script and captioned software/CAD demonstration. No competition upload has been performed. Team should verify playback, confirm consistency with its original abstract and upload one video (maximum 90 s / 50 MB) and this report (2 pages) by 4 November 2026, 11:59 PM IST.')]
SimpleDocTemplate(str(report),pagesize=(595,842),rightMargin=40,leftMargin=40,topMargin=34,bottomMargin=42).build(story,onFirstPage=footer,onLaterPages=footer)
# CAD handbook: explicit local feature workflows and actual orthographic projections.
manifest=json.loads((C/'parts_manifest.json').read_text())
procedures={
1:('Feed storage','Top Plane: centre rectangle 140 x 130; Boss-Extrude 200. Select top face, Sketch centre rectangle 132 x 122; Cut-Extrude 196. Wall/base 4.'),
2:('Sediment housing envelope','Top Plane: circle diameter 88; Boss-Extrude 270. Top face: circle diameter 80; Cut-Extrude 266. Wall/base 4. No threaded closure or seal is designed.'),
3:('Sediment cartridge envelope','Top Plane: concentric circles diameter 60 and 20; Boss-Extrude 240. Assumed annular cartridge; filtration media not modelled.'),
4:('Carbon housing envelope','Repeat sediment housing: diameter 88 x 270; bore diameter 80, depth 266. Save as a separate part.'),
5:('Carbon cartridge envelope','Top Plane: circles diameter 60 and 20; Boss-Extrude 240. Carbon media and adsorption life are not modelled.'),
6:('RO housing envelope','Right Plane: circle diameter 56; Boss-Extrude 310. End face: circle diameter 50; Cut-Extrude 307. Axis along X. No pressure-rated closure.'),
7:('RO membrane envelope','Right Plane: circles diameter 44 and 14; Boss-Extrude 280. Membrane layers and hydraulic internals omitted.'),
8:('Tube routing section','Top Plane: circles diameter 6.35 and 4; Boss-Extrude 100. For curved routing create a path sketch and Swept Boss/Base using this annular profile.'),
9:('Connector envelope','Top Plane: circles diameter 16 and 6.4; Boss-Extrude 24. Real connector thread, collet, seals and bore must follow vendor dimensions.'),
10:('Pump mounting plate','Top Plane: centre rectangle 100 x 65; Boss-Extrude 5. Top face: four diameter 5 circles centred at (+/-35, +/-20); Cut-Extrude Through All. Hole Wizard can replace cuts using plain holes.'),
11:('Pressure sensor adapter envelope','Top Plane: circles diameter 30 and 10; Boss-Extrude 25. Repeat as P1/P2 locations after matching actual transducer thread and pressure rating.'),
12:('TDS probe holder envelope','Top Plane: circles diameter 24 and 8; Boss-Extrude 30. Repeat for product probe after vendor dimensions and wet materials are checked.'),
13:('Turbidity module bracket','Top Plane: rectangle 50 x 40; Boss-Extrude 45. Top face: rectangle 44 x 34; Cut-Extrude 42. This is a mounting envelope, not a calibrated optical cell.'),
14:('Flow sensor envelope','Top Plane: circles diameter 32 and 6.4; Boss-Extrude 45. Adapt to a meter rated for the low product flow; calibrate pulses/litre.'),
15:('Dry electronics enclosure','Top Plane: rectangle 150 x 90; Boss-Extrude 45. Top face: rectangle 144 x 84; Cut-Extrude 42. Keep cable entries above drip zone; ingress protection is unverified.'),
16:('Electronics mounting plate','Top Plane: rectangle 140 x 80; Boss-Extrude 3. Four diameter 3 through holes centred (+/-60,+/-30). PCB spacers remain vendor dependent.'),
17:('Leak collection tray','Top Plane: rectangle 620 x 260; Boss-Extrude 12. Top face: rectangle 614 x 254; Cut-Extrude 9. Add approved leak sensor at lowest point in detailed design.'),
18:('Prototype stand envelope','Top Plane: rectangle 640 x 280; Boss-Extrude 6 downward. On top at rear edge: rectangle 640 x 6 centred at Y=137; Boss-Extrude 540. Merge solids. This is a conceptual backplate; stiffness/fasteners not verified.'),
19:('Sediment cap envelope','Top Plane: circle diameter 96; Boss-Extrude 18. No threaded or sealed interface is provided.'),
20:('Carbon cap envelope','Top Plane: circle diameter 96; Boss-Extrude 18. No threaded or sealed interface is provided.'),
21:('RO cap envelope','Right Plane: circle diameter 62; Boss-Extrude 14. No threaded or sealed interface is provided.'),
22:('Pump clearance envelope','Top Plane: rectangle 90 x 55; Boss-Extrude 75. Replace with vendor geometry; this is not a pump mechanism.'),
23:('Normally closed valve clearance','Top Plane: rectangle 35 x 30; Boss-Extrude 45. Replace with rated valve geometry. Simulated shutdown does not prove valve behaviour.'),
24:('Electronics lid','Top Plane: rectangle 150 x 90; Boss-Extrude 3. Fasteners/gasket are pending.'),
}
manual=D/'FilterSense_CAD_Handbook.pdf'
c=canvas.Canvas(str(manual),pagesize=(842,595))
def base(title,page):
 c.setFillColor(HexColor('#11384a'));c.rect(0,515,842,80,fill=1,stroke=0);c.setFillColor(white);c.setFont('Helvetica-Bold',20);c.drawString(35,550,title);c.setFont('Helvetica',9);c.drawString(35,530,'CONCEPT REFERENCE DRAWING | Units: mm | Assumed dimensions | Not for pressure manufacture')
 c.setFillColor(HexColor('#344f5d'));c.setFont('Helvetica',8);c.drawString(35,20,'FilterSense / Spartans / Rev B / 03-Nov-2026 / Geometry generated using CadQuery, not SOLIDWORKS');c.drawRightString(807,20,str(page))
def lines(text,x,y,width=105,size=10):
 c.setFont('Helvetica',size);c.setFillColor(HexColor('#243d4a'))
 for line in textwrap.wrap(text,width): c.drawString(x,y,line);y-=15
 return y
base('CAD package and SOLIDWORKS workflow',1)
y=485
for txt in ['Open SOLIDWORKS > File > Open > select STEP > cad/FilterSense_assembly.step. Open parts individually to inspect imported solids. Save As native documents if needed. Import was not run here; installed version is unknown.',
'For native feature trees: File > New > Part > set MMGS (bottom-right units). Select the named plane > Sketch. Use Smart Dimension to fully define the profile, then Features > Extruded Boss/Base or Extruded Cut as listed on each sheet.',
'Assembly: File > New > Assembly > insert stand first and fix it. Insert each part. Use Concentric mates for housing/cartridge axes, Coincident mates for mounting faces, and Distance mates for height/offset. The manifest gives assumed assembly origins in mm. STEP positions do not imply mates.',
'Exploded view: Assembly tab > Exploded View; select cartridges/caps/lid and translate upward about 140 mm; move housings forward 65 mm. An exported exploded STEP is supplied. Clearance and supports must be refined against real components.',
'Engineering drawing: File > Make Drawing from Part/Assembly > choose sheet > Model View > front/top/right; use Smart Dimension or Model Items for native features. These reference sheets give actual projections, overall envelopes and specified sketch dimensions, not production tolerances.',
'Feature notes: Boss adds material; Cut removes it. Revolve rotates a closed half-section about a centreline (alternative for axisymmetric housings). Hole Wizard defines standard holes. Fillet rounds edges; Chamfer bevels them. No decorative fillets are applied here; mating/pressure details must be reviewed first.',
'No flow or structural simulation has been run. Check Tools > Add-Ins and licence availability before using simulation. A Premium licence alone does not establish Flow Simulation entitlement.']:
 y=lines(txt,35,y,120,10)-15
c.showPage()
for i in range(1,25):
 item=manifest[i-1];name=item['name'];purpose,procedure=procedures[i]
 base(name.replace('_',' '),i+1)
 shape=cq.importers.importStep(str(C/'parts'/f'{name}.step'))
 for j,(direction,label) in enumerate([((0,-1,0),'FRONT'),((0,0,1),'TOP')]):
  svg=cq.exporters.getSVG(shape.val(),opts={'width':365,'height':245,'marginLeft':20,'marginTop':20,'projectionDir':direction,'showAxes':False,'showHidden':False,'strokeWidth':1})
  path=C/f'_view_{i}_{j}.svg';path.write_text(svg)
  drawing=svg2rlg(str(path));renderPDF.draw(drawing,c,35+395*j,225)
  c.setFont('Helvetica-Bold',10);c.drawString(35+395*j,475,label)
  path.unlink()
 dims=item['size_mm'];c.setFont('Helvetica-Bold',11);c.drawString(35,215,f'Overall X = {dims[0]:g} mm     Y = {dims[1]:g} mm     Z = {dims[2]:g} mm')
 y=lines('Purpose: '+purpose+'. Assembly origin: '+str(item['position_mm'])+' mm.',35,190,120)
 y=lines('Native feature sequence: '+procedure,35,y-10,120)
 lines('Dimensions define concept envelopes only. No material specification, thread/seal detail, tolerance, certified pressure rating or manufacturing release is implied.',35,y-12,120)
 c.showPage()
base('Assembly and routing reference',26)
c.drawImage(str(C/'assembly.png'),35,110,width=390,height=260,preserveAspectRatio=True)
c.drawImage(str(C/'exploded.png'),425,110,width=390,height=260,preserveAspectRatio=True)
lines('Stand: 640 x 280 mm base, 540 mm backplate height. Turquoise tubes: intended supply/product routing; orange: reject routing. Seven tube segments are routing placeholders. Duplicate sensor holders, rated supports, restrictor and collection plumbing are pending detailed integration.',35,480,120)
lines('Source geometry: cad/build_cad.py. Assembly placements: parts_manifest.json. Inspect every mating/interface detail before any physical build. Electronic and hydraulic safety are design intent, not validated hardware.',35,85,120)
c.showPage();c.save()
print(report,manual)
