from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
ROOT=Path(__file__).resolve().parent
fig,ax=plt.subplots(figsize=(13,10));ax.set_xlim(0,13);ax.set_ylim(0,10);ax.axis('off')
fig.patch.set_facecolor('#f3f8fa')
def box(x,y,w,h,text,color='#dceef2'):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.08',facecolor=color,edgecolor='#22778a'))
 ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=11,color='#143a4a')
def arrow(a,b,dash=False,color='#3c7587'):
 ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='->',lw=1.8,color=color,linestyle='--' if dash else '-'))
ax.text(.3,9.6,'FilterSense / system architecture',fontsize=23,weight='bold',color='#143a4a')
ax.text(.3,9.15,'Hardware = future design intent     |     Synthetic source = implemented software',fontsize=12,color='#587782')
water=[('Feed + inlet sensors',8),('NC valve + pump',6.8),('P1 / sediment / carbon / P2',5.6),('RO membrane',4.4)]
for text,y in water:box(.4,y,4,.65,text)
for i in range(3):arrow((2.4,water[i][1]),(2.4,water[i+1][1]+.65))
box(.4,2.9,2,.8,'Product\nTDS + flow');box(2.9,2.9,2,.8,'Reject\nrestrictor + waste','#f8e6ce')
arrow((1.4,4.4),(1.4,3.7));arrow((3.4,4.4),(3.9,3.7))
box(6,7.9,2.7,.8,'Future ESP32\n+ ADC channels')
box(9.5,7.9,3,.8,'Implemented\nsynthetic simulator','#bde5dc')
box(7.4,6.4,4,.8,'Input validation + history')
box(7.4,5,4,.8,'Pressure / flow / rejection\n+ estimated feed exposure')
box(7.4,3.6,4,.8,'Causal smoothing\n+ time-to-threshold forecast')
box(7.4,2.2,4,.8,'Dashboard + CSV + alert')
arrow((4.4,8.3),(6,8.3),True);arrow((4.4,5.9),(6,8),True)
ax.plot([2.4,5.3,5.3],[3.3,3.3,7.6],linestyle='--',color='#3c7587',lw=1.8);arrow((5.3,7.6),(6,8),True)
arrow((7.3,7.9),(8.4,7.2));arrow((10.8,7.9),(10.5,7.2))
for a,b in [(6.4,5.8),(5,4.4),(3.6,3)]:arrow((9.4,a),(9.4,b))
box(.4,1.2,4.5,.8,'Leak / invalid sensor / pressure\nlocal latched interlock','#f8e6ce')
ax.plot([.4,.15,.15],[1.6,1.6,7.1],linestyle='--',color='#b57637',lw=1.8);arrow((.15,7.1),(.4,7.1),True,'#b57637')
ax.text(.5,.5,'Safety commands are simulated. Physical pump/valve protection remains untested.',fontsize=12,color='#a26325')
fig.savefig(ROOT/'architecture.png',dpi=160,bbox_inches='tight');fig.savefig(ROOT/'architecture.svg',bbox_inches='tight');plt.close(fig)
