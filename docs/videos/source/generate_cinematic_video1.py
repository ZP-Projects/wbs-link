"""Cinematic, scene-led Video 1. Synthetic visual metaphor, not product footage."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math, subprocess, shutil
HERE=Path(__file__).resolve().parent
OUT=HERE.parent
FRAMES=HERE/'_cinematic_frames'
FRAMES.mkdir(exist_ok=True)
W,H=1280,720
NAVY=(10,20,33); WHITE=(242,239,227); GOLD=(211,156,88)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
SCENES=[
 ('ONE PROJECT','Three different views of the same scope',0),
 ('THE SCHEDULE','A credible delivery sequence',1),
 ('THE FORECAST','A credible financial picture',2),
 ('THE CONTRACTS','A credible commercial structure',3),
 ('BUT DO THEY ALIGN?','Similar labels do not prove shared scope',4),
 ('THE OWNER WBS','A common integration spine',5),
 ('SOME LINKS NEED JUDGMENT','Uncertainty must remain visible',6),
 ('MAKE THE RELATIONSHIPS VISIBLE','Governed. Reviewable. Reusable.',7)]
DUR=[8,8,8,8,9,8,9,8]
def font(size,bold=False): return ImageFont.truetype(BOLD if bold else FONT,size)
def line(d,points,color,width=3): d.line(points,fill=color,width=width,joint='curve')
def render(k,phase):
    im=Image.new('RGB',(W,H),NAVY);d=ImageDraw.Draw(im)
    # Moving architectural silhouette, grid, project lines and scope structures.
    for x in range(0,W,80):
        line(d,[(x+int(phase*25)%80,0),(x+int(phase*25)%80,H)],(20,34,50),1)
    for y in range(0,H,80):line(d,[(0,y),(W,y)],(20,34,50),1)
    if k<4:
        # A recognizable synthetic infrastructure site with bridge piers and a rail deck.
        d.polygon([(0,490),(W,460),(W,550),(0,570)],fill=(40,58,72))
        for x in (130,390,650,910,1150):
            d.polygon([(x,485),(x+44,484),(x+35,700),(x+5,700)],fill=(66,80,91))
        for x in range(0,W,120):
            xx=(x+int(phase*110))%W
            d.rectangle((xx,450,xx+70,462),fill=(109,129,136))
        if k==1:
            for i in range(5):
                x=125+i*185; d.rounded_rectangle((x,365,x+150,404),radius=7,outline=GOLD,width=3)
                if i<4:line(d,[(x+150,384),(x+184,384)],GOLD,3)
        elif k==2:
            for i,v in enumerate((90,130,115,165,140,205)):
                x=130+i*150;d.rectangle((x,460-v,x+72,460),fill=(70+i*12,105+i*8,121+i*6))
        elif k==3:
            for i in range(4):
                x=135+i*235;d.rectangle((x,340,x+192,437),outline=GOLD,width=3)
                d.text((x+16,360),f'PACKAGE {i+1}',font=font(21,True),fill=WHITE)
    else:
        centers=[(265,320),(265,430),(265,540)]
        for j,(x,y) in enumerate(centers):
            d.rounded_rectangle((x-135,y-38,x+135,y+38),radius=12,fill=(34,52,69),outline=(110,130,142),width=2)
            d.text((x-103,y-13),('SCHEDULE','COST / FORECAST','CONTRACTS')[j],font=font(18,True),fill=WHITE)
        d.rounded_rectangle((805,360,1100,492),radius=18,fill=(44,55,65),outline=GOLD,width=4)
        d.text((846,396),'OWNER WBS',font=font(31,True),fill=WHITE)
        for j,(_,y) in enumerate(centers):
            if k==4 and j==2:continue
            color=GOLD if k!=6 or j!=1 else (178,104,75)
            points=[(400,y),(600,y),(670,426),(805,426)]
            line(d,points,color,4)
            if k==6 and j==1:
                d.ellipse((635,390,674,429),fill=(178,104,75))
                d.text((647,397),'?',font=font(21,True),fill=WHITE)
    d.rectangle((0,0,W,7),fill=GOLD)
    d.text((72,55),'WBS↔LINK  /  THE CHALLENGE',font=font(18,True),fill=GOLD)
    title,sub,_=SCENES[k]
    d.text((72,125),title,font=font(48,True),fill=WHITE)
    d.text((74,198),sub,font=font(24),fill=(196,204,210))
    d.text((74,665),'Synthetic illustration. Relationships require evidence and professional judgment.',font=font(15),fill=(157,172,183))
    return im
concat=FRAMES/'scenes.txt'
with concat.open('w') as f:
    for k,duration in enumerate(DUR):
        for j in range(5):
            path=FRAMES/f'{k:02d}-{j:02d}.png'
            render(k,j/5).save(path)
            f.write(f"file '{path.as_posix()}'\nduration {duration/5}\n")
    f.write(f"file '{path.as_posix()}'\n")
poster=OUT/'wbslink-video-1-challenge.jpg'
render(0,0).save(poster,quality=90)
video=OUT/'wbslink-video-1-challenge.mp4'
subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(concat),'-vf','fps=24,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','23','-movflags','+faststart',str(video)],check=True)
shutil.rmtree(FRAMES)
print(video)
