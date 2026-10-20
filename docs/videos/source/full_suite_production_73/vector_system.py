"""Original WBS-LINK icons. Shared 24-unit grid, 1.6-unit square-ended stroke.
No external icon asset, borrowed path or runtime dependency.
"""
from pathlib import Path
import json, math

ICONS={
 'schedule':[('r',3,5,18,16),('l',3,10,21,10),('l',7,2,7,7),('l',17,2,17,7),('l',7,14,13,14),('l',11,18,17,18)],
 'cost':[('r',3,3,18,18),('l',3,8,21,8),('l',9,8,9,21),('l',13,12,18,12),('l',13,16,18,16),('l',5.5,12,6.5,12),('l',5.5,16,6.5,16)],
 'packages':[('p',[(7,3),(21,3),(21,17)]),('p',[(4,6),(18,6),(18,20)]),('r',2,9,13,13),('l',5,13,12,13),('l',5,17,10,17)],
 'wbs':[('r',8,2,8,5),('l',12,7,12,11),('l',4,11,20,11),('l',4,11,4,16),('l',12,11,12,16),('l',20,11,20,16),('r',1,16,6,6),('r',9,16,6,6),('r',17,16,6,6)],
 'evidence':[('p',[(4,2),(14,2),(20,8),(20,22),(4,22),(4,2)]),('p',[(14,2),(14,8),(20,8)]),('l',8,12,16,12),('l',8,16,16,16),('l',8,19,12,19)],
 'unresolved':[('p',[(8,5),(4,5),(2,7),(2,13),(4,15),(8,15)]),('p',[(16,9),(20,9),(22,11),(22,17),(20,19),(16,19)]),('l',6,10,8,10),('l',16,14,18,14),('l',10,10,11,10),('l',13,14,14,14),('l',11,4,11,6),('l',14,18,14,20)],
 'review':[('r',9,2,13,20),('l',13,6,18,6),('l',13,10,18,10),('c',5,11,3),('p',[(1,21),(1,19),(3,17),(7,17),(9,19),(9,21)])],
 'approval':[('p',[(3,2),(15,2),(21,8),(21,14)]),('p',[(15,2),(15,8),(21,8)]),('p',[(6,22),(3,22),(3,2)]),('l',7,7,11,7),('p',[(14,12),(21,14),(21,19),(17.5,22),(14,19),(14,12)]),('p',[(16,17),(17.5,18.5),(19.5,15.5)])],
 'report':[('r',3,2,18,20),('l',7,6,17,6),('l',7,10,17,10),('r',7,14,4,4),('l',14,14,17,14),('l',14,18,17,18)]
}

def icon(d,name,x,y,size,col):
 s=size/24;lw=1.6*s
 for op,*v in ICONS[name]:
  if op=='l':d.line(x+v[0]*s,y+v[1]*s,x+v[2]*s,y+v[3]*s,col,lw)
  elif op=='r':
   a,b,w,h=v
   for aa,bb,cc,ee in [(a,b,a+w,b),(a+w,b,a+w,b+h),(a+w,b+h,a,b+h),(a,b+h,a,b)]:d.line(x+aa*s,y+bb*s,x+cc*s,y+ee*s,col,lw)
  elif op=='c':d.circle(x+v[0]*s,y+v[1]*s,v[2]*s,col,lw)
  elif op=='p':
   for a,b in zip(v[0],v[0][1:]):d.line(x+a[0]*s,y+a[1]*s,x+b[0]*s,y+b[1]*s,col,lw)

def write_assets(root):
 root.mkdir(exist_ok=True)
 for name,ops in ICONS.items():
  bits=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#121A2E" stroke-width="1.6" stroke-linecap="butt" stroke-linejoin="miter" role="img">',f'<title>{name} | original WBS-LINK semantic icon</title>']
  for op,*v in ops:
   if op=='l':bits.append(f'<path d="M{v[0]} {v[1]}L{v[2]} {v[3]}"/>')
   elif op=='r':bits.append(f'<rect x="{v[0]}" y="{v[1]}" width="{v[2]}" height="{v[3]}"/>')
   elif op=='c':bits.append(f'<circle cx="{v[0]}" cy="{v[1]}" r="{v[2]}"/>')
   else:bits.append('<path d="'+' '.join(('M' if i==0 else 'L')+str(a)+' '+str(b) for i,(a,b) in enumerate(v[0]))+'"/>')
  (root/f'{name}.svg').write_text('\n'.join(bits+['</svg>']))
 (root/'GEOMETRY.json').write_text(json.dumps({'grid':24,'stroke':1.6,'linecap':'butt','linejoin':'miter','corner_radius':0,'palette':['121A2E','8F5A28','C98F52','FFFFFF'],'icons':ICONS},indent=2))

class View:
 def __init__(self,d,x,y,w,h,basew,baseh):self.d,self.x,self.y,self.s=d,x,y,w/basew;assert abs(w/basew-h/baseh)<.002
 def rect(self,x,y,w,h,*a,**k):return self.d.rect(self.x+x*self.s,self.y+y*self.s,w*self.s,h*self.s,*a,**k)
 def line(self,x,y,xx,yy,col,lw=1,dash=False):return self.d.line(self.x+x*self.s,self.y+y*self.s,self.x+xx*self.s,self.y+yy*self.s,col,lw*self.s,dash)
 def circle(self,x,y,r,col,lw=1):return self.d.circle(self.x+x*self.s,self.y+y*self.s,r*self.s,col,lw*self.s)
 def text(self,x,y,t,size=12,bold=False,col='121A2E',width=None,leading=None,**k):
  return self.d.text(self.x+x*self.s,self.y+y*self.s,t,size*self.s,bold,col,width=width*self.s if width else None,leading=leading*self.s if leading else None,**k)

N='121A2E';MID='1B2A4A';PAPER='F5F5F3';GREY='565B64';STEEL='A2A7AF';WHITE='FFFFFF';COG='8F5A28';COGLIGHT='C98F52'
TIMELINE=[{'scene_seconds':[0,2.5],'film_time':'00:08–00:10.5','action':'Source cards enter separately with their calendar, ledger and document-stack icons. The Owner WBS reference surface settles independently.'},{'scene_seconds':[2.5,4],'film_time':'00:10.5–00:12','action':'Reveal only the schedule reference path.'},{'scene_seconds':[4,5.5],'film_time':'00:12–00:13.5','action':'Reveal the cost/forecast reference path on its separate route.'},{'scene_seconds':[5.5,7],'film_time':'00:13.5–00:15','action':'Reveal the package reference path on its separate route.'},{'scene_seconds':[7,9],'film_time':'00:15–00:17','action':'Hold the Owner WBS with six actual work-area labels. Introduce the evidence, visible gap and human-review vocabulary. None of the paths is an approval or direct source-to-source equivalence.'}]

def path_reveal(v,points,amount):
 # A sampled cubic route; the same deterministic geometry supplies every keyframe.
 if amount<=0:return
 def pt(t):
  a,b,c,d=points;u=1-t;return(u**3*a[0]+3*u*u*t*b[0]+3*u*t*t*c[0]+t**3*d[0],u**3*a[1]+3*u*u*t*b[1]+3*u*t*t*c[1]+t**3*d[1])
 last=points[0]
 for i in range(1,61):
  t=min(amount,i/60);q=pt(t);v.line(*last,*q,COGLIGHT,1.6);last=q
  if i/60>=amount:break

def scene2(d,x,y,w,h,t,branches,mobile=False):
 bw,bh=(540,960) if mobile else (960,540);v=View(d,x,y,w,h,bw,bh)
 v.rect(0,0,bw,bh,N)
 if not mobile:
  v.text(36,24,'WBS LINK  /  INDEPENDENT SOURCE RELATIONSHIPS',10,True,COGLIGHT)
  v.text(36,49,'Three sources. One owner reference.',27,True,WHITE)
  v.text(36,87,'Relate each source through the Owner WBS. Keep its evidence and authority distinct.',13,col=STEEL)
  cardx,cardw,cardys,cardh=36,240,[130,232,334],78
  hubx,huby,hubw,hubh=574,130,350,282
 else:
  v.text(24,24,'WBS LINK  /  INDEPENDENT SOURCES',17,True,COGLIGHT)
  v.text(24,50,'Three sources.\nOne owner reference.',28,True,WHITE,leading=32)
  cardx,cardw,cardys,cardh=24,350,[140,248,356],82
  hubx,huby,hubw,hubh=24,550,492,276
 labels=[('schedule','Schedule Source','Delivery sequence'),('cost','Cost / Forecast','Control accounts'),('packages','Work Packages','Commercial scope')]
 for i,(name,label,sub) in enumerate(labels):
  if t<i*.5:continue
  off=-24*max(0,1-(t-i*.5)/.8)
  xx=cardx+off;yy=cardys[i]
  v.rect(xx,yy,cardw,cardh,MID);v.rect(xx,yy,3,cardh,COGLIGHT)
  icon(v,name,xx+14,yy+23,30 if mobile else 28,WHITE)
  v.text(xx+58,yy+16,label,20 if mobile else 17,True,WHITE,width=cardw-68)
  v.text(xx+58,yy+45,sub,17 if mobile else 12,col=STEEL,width=cardw-68)
 # Relationship paths connect only to the shared reference, never to another source.
 for i,yy in enumerate(cardys):
  amount=max(0,min(1,(t-(2.5+1.5*i))/1.5))
  if mobile:
   lane=[480,446,412][i];end=(lane,huby);start=(cardx+cardw,yy+cardh/2)
   # Separate outside rails are ordered so paths do not cross any source card or each other.
   verts=[start,(lane,start[1]),end];dist=[abs(verts[1][0]-verts[0][0]),abs(verts[2][1]-verts[1][1])];left=amount*sum(dist)
   for j in range(2):
    frac=min(1,left/dist[j]) if dist[j] else 1
    if frac>0:v.line(*verts[j],verts[j][0]+(verts[j+1][0]-verts[j][0])*frac,verts[j][1]+(verts[j+1][1]-verts[j][1])*frac,COGLIGHT,1.6)
    left-=dist[j]
  else:
   ports=[192,271,350];path_reveal(v,[(276,yy+39),(375,yy+39),(475,ports[i]),(574,ports[i])],amount)
   if amount==1:v.rect(570,ports[i]-3,6,6,COGLIGHT)
 # Owner WBS hub: authored illustration of actual coverage branches, not fabricated UI.
 if t>=1.3:
  v.rect(hubx,huby,hubw,hubh,PAPER)
  if mobile:
   icon(v,'wbs',44,571,35,N);v.text(100,577,'Owner WBS',27,True)
   v.text(44,622,'Shared scope reference',18,col=GREY)
   rootx,rowx,rowy,step=55,78,657,23
  else:
   icon(v,'wbs',595,151,29,N);v.text(638,154,'Owner WBS',22,True)
   v.text(596,201,'Shared scope reference',13,col=GREY)
   rootx,rowx,rowy,step=609,633,236,24
  v.line(rootx,rowy+5,rootx,rowy+step*5+5,GREY,.8)
  shown=6 if t>=2.5 else max(1,int((t-1.3)/1.2*6))
  for i,b in enumerate(branches[:shown]):
   ry=rowy+i*step;v.line(rootx,ry+5,rowx-8,ry+5,GREY,.8);v.rect(rowx-10,ry+3,4,4,COG if b['code']=='1.5' else GREY)
   v.text(rowx,ry,b['code'],18 if mobile else 12,True,COG if b['code']=='1.5' else N)
   v.text(rowx+(49 if mobile else 34),ry,b['name'],18 if mobile else 12,col=N,width=hubw-(rowx-hubx)-(65 if mobile else 48))
  v.text(44 if mobile else 596,805 if mobile else 389,'Reference paths are not confirmation.',17 if mobile else 10,col=GREY)
 if t>=7:
  if not mobile:v.text(36,430,'RELATIONSHIP OUTCOMES REMAIN DISTINCT',9,True,STEEL)
  states=[('evidence','Source-backed','Evidence preserved'),('unresolved','Gap visible','Not forced into WBS'),('review','Human review','Decision scope recorded')]
  for i,(name,label,sub) in enumerate(states):
   if mobile:
    xx=24+i*172;icon(v,name,xx+3,854,25,COGLIGHT);v.text(xx+3,891,label,18,True,WHITE,width=163)
   else:
    xx=36+i*300;icon(v,name,xx,461,26,COGLIGHT);v.text(xx+40,452,label,16,True,WHITE);v.text(xx+40,476,sub,11,col=STEEL)
 if mobile:v.text(24,937,'Method illustration. No automatic approval or merged data.',17,col=STEEL,width=492)
 else:v.text(36,522,'Method illustration. Sources remain separate; no automatic confirmation, progress claim or merged dataset.',10,col=STEEL)
 return v
