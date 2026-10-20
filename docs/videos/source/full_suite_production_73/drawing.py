"""Original motion-graphic drawing vocabulary. Material text is laid out, not cropped."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import re,math
FONT=Path(__file__).resolve().parents[1]/'fonts'
N='121A2E';MID='1B2A4A';PAPER='F5F5F3';WHITE='FFFFFF';GREY='565B64';COG='8F5A28';CL='C98F52';STEEL='A2A7AF';LIGHT='EAEAE6'
class Draw:
 def __init__(self,w,h,image=None):self.w,self.h=w,h;self.im=image or Image.new('RGB',(w,h),'#'+N);self.d=ImageDraw.Draw(self.im);self.records=[]
 def rect(self,x,y,w,h,fill=WHITE,*a,**k):self.d.rectangle((x,y,x+w,y+h),fill='#'+fill.lstrip('#'))
 def line(self,x,y,xx,yy,col=LIGHT,lw=1,dash=False):
  if dash:
   length=math.hypot(xx-x,yy-y);steps=max(1,int(length/8))
   for i in range(0,steps,2):
    a=i/steps;b=min(1,(i+1)/steps);self.d.line((x+(xx-x)*a,y+(yy-y)*a,x+(xx-x)*b,y+(yy-y)*b),fill='#'+col.lstrip('#'),width=max(1,round(lw)))
  else:self.d.line((x,y,xx,yy),fill='#'+col.lstrip('#'),width=max(1,round(lw)))
 def circle(self,x,y,r,col=N,lw=1):self.d.ellipse((x-r,y-r,x+r,y+r),outline='#'+col.lstrip('#'),width=max(1,round(lw)))
 def text(self,x,y,text,size=32,bold=False,col=WHITE,width=None,leading=None,font=None,**kw):
  size=max(1,round(size));face=ImageFont.truetype(str(FONT/('Archivo-700.ttf' if bold else 'Archivo-400.ttf')),size);symbol=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',size)
  lines=[]
  def length(t):return sum(self.d.textlength(q,font=symbol if q in ['↔','→'] else face) for q in re.split('([↔→])',t) if q)
  for para in str(text).split('\n'):
   line=''
   for word in para.split():
    q=(line+' '+word).strip()
    if width and length(q)>width and line:lines.append(line);line=word
    else:line=q
   lines.append(line)
  leading=leading or size*1.25
  for i,line in enumerate(lines):
   xx=x
   for part in re.split('([↔→])',line):
    if not part:continue
    f=symbol if part in ['↔','→'] else face;self.d.text((xx,y+i*leading),part,font=f,fill='#'+col.lstrip('#'));xx+=self.d.textlength(part,font=f)
   assert xx<=self.w+1,(text,xx,self.w)
  end=y+len(lines)*leading;assert end<=self.h+1,(text,end,self.h)
  self.records.append({'text':'\n'.join(lines),'x':x,'y':y,'size':size,'end':end,'colour':col});return end
 def brand(self,x,y,size=32,col=WHITE):return self.text(x,y,'WBS↔LINK',size,True,col)

def ease(t):t=max(0,min(1,t));return t*t*(3-2*t)

def contained(im,w,h):
 scale=min(w/im.width,h/im.height);return im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.LANCZOS)
