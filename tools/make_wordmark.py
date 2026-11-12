"""Builds the Notturno wordmark (the bottom-right drawing on the scanned label sheet: a wide brushed N with "otturno" lettered
after it) as a flat vector mark: notturno-wordmark.svg. Same treatment as the icon (tools/make_icon.py in the
widget): upscale, classify ink with a darker cut-off inside the label's printed grey disc, leave the disc itself out, flat ink.
The label's printed address crosses the top of the N; it is removed by keeping only ink at least ~2 scan px wide."""
import sys
from PIL import Image, ImageFilter
import numpy as np
from scipy import ndimage as ndi
from skimage.morphology import disk
SCAN=sys.argv[1]; OUT=sys.argv[2] if len(sys.argv)>2 else 'notturno-wordmark.svg'
c=Image.open(SCAN).convert('L').crop((520,880,960,1230))
S=6; big=c.resize((c.width*S,c.height*S),Image.BICUBIC).filter(ImageFilter.GaussianBlur(2.0)); a=np.asarray(big).astype(float)/255
def ss(lo,hi,x): t=np.clip((x-lo)/(hi-lo),0,1); return t*t*(3-2*t)
# the printed disc: fit it from the mid-grey pixels in its corner of the crop
yy,xx=np.mgrid[0:a.shape[0],0:a.shape[1]]
g=(a>0.37)&(a<0.50)&(xx<140*S)&(yy>230*S); g=ndi.binary_opening(g,disk(6))
ccy,ccx=ndi.center_of_mass(g); R=np.sqrt(np.hypot(xx-ccx,yy-ccy)[g].max()**2)*1.0
print('disc',ccx/S,ccy/S,R/S)
dist=np.hypot(xx-ccx,yy-ccy); side=ss(-1.5*S,1.5*S,dist-(R+1.0*S))
th=0.335+(0.60-0.335)*side; wd=0.02+(0.07-0.02)*side
ink=1-ss(th-wd,th+wd,a)
b=ink>0.5
core=ndi.binary_opening(b,disk(7))                                       # drops the address (strokes ~1 scan px wide)
keep=ndi.binary_dilation(core,disk(3))&b
keep=np.where(yy<70*S,core,keep)                                         # where the address crossed the N, no regrowth: its stubs stay off
lab,nl=ndi.label(keep); area=ndi.sum(keep,lab,range(1,nl+1)); keep=np.isin(lab,1+np.flatnonzero(area>=1500))
ink=ink*ndi.gaussian_filter(ndi.binary_dilation(keep,disk(2)).astype(float),1.0)
ink=np.where(yy<70*S,np.minimum(ink,ndi.gaussian_filter(keep.astype(float),1.5)*1.6).clip(0,1),ink)
ys,xs=np.where(ink>0.05); ink=ink[ys.min()-6:ys.max()+7,xs.min()-6:xs.max()+7]
# --- vector: trace the ink outline (smoothed along its length, so no pixel steps) into one SVG path, crisp at any size
from skimage import measure
h,w=ink.shape; P=np.pad(ink,4); d=[]
def curve(x,y):
    """A closed outline as cubic Beziers through its points (Catmull-Rom), so edges are curves, not facets."""
    n=len(x); out=['M%.1f %.1f'%(x[0],y[0])]
    for k in range(n):
        p0,p1,p2,p3=[(x[(k+o)%n],y[(k+o)%n]) for o in (-1,0,1,2)]
        c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6); c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
        out.append('C%.1f %.1f %.1f %.1f %.1f %.1f'%(c1+c2+p2))
    return ''.join(out)+'Z'
for cc in measure.find_contours(P,0.5):
    if len(cc)<40: continue
    big_=len(cc)>3000; sg=22.0 if big_ else 6.0; step=26 if big_ else 9     # the N takes more smoothing than the small lettering
    y=ndi.gaussian_filter1d(cc[:-1,0],sg,mode='wrap')-4; x=ndi.gaussian_filter1d(cc[:-1,1],sg,mode='wrap')-4
    d.append(curve(x[::step],y[::step]))
svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="Notturno"><path fill="#1b1b1b" fill-rule="evenodd" d="%s"/></svg>\n'%(w,h,''.join(d))
open(OUT,'w').write(svg); print(w,h,len(svg),len(d))
