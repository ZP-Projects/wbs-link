"""Reproducible synthetic HarbourLink application montage; original instrumental score.

Run with the existing host Pillow/numpy tooling. UI captures are actual candidate
pages, not reconstructed UI. Close-ups and motion are editorial; no approval
interaction is simulated. See PO_CORRECTIONS_PROVENANCE.json for exact sources.
"""
from pathlib import Path
import math
from functools import lru_cache
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
DOCS = HERE.parents[1]
WORK = Path('/workspace/work/po-corrections-73/video-build')
WORK.mkdir(parents=True, exist_ok=True)
W, H, FPS = 1920, 1080, 24
BG = (15, 21, 37)
WHITE = (238, 240, 236)
GOLD = (205, 160, 116)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

SCENES = [
    ('One project. Views that do not align.', 'integration', 'link', 'Schedule and cost meet only through the Owner WBS. HarbourLink exposes the missing coverage.', 8),
    ('The executive finding comes first.', 'project', 'eye', 'In this approved synthetic position, 4 of 6 Owner-WBS branches have both schedule and cost relationships. Two have only one view.', 8),
    ('Follow the finding into Owner WBS 1.5.', 'wbs', 'tree', 'Testing and Commissioning has schedule relationships but no governed cost relationships. That is an issue for professional review, not a project-health score.', 8),
    ('Open the Crosswalk. Inspect the source.', 'evidence', 'source', 'This schedule record states WBS Code 1.5.1. The source assertion and its evidence stay visible; the relationship does not establish a direct schedule-to-cost link.', 8),
    ('Interpretation and decision stay distinct.', 'interpretation', 'review', 'Elsewhere in the same project, changed source evidence has been re-decided by Maya Chen, Owner Project Controls. Software interpretation does not approve a professional decision.', 8),
    ('The approved position travels with you.', 'report', 'document', 'The actual two-page executive briefing carries the approved position, exact professional Actions and quantitative withholding, with supporting evidence on page two.', 8),
    ('Four charts. Four stated populations.', 'charts', 'chart', 'The Premium Workbook retains all 21 worksheets and four charts: Owner-WBS coverage, relationships by source, cycle movement and unresolved outcomes. Their populations remain distinct.', 8),
    ('Cycle 2 preserves what still holds.', 'cycle2', 'cycle', 'The actual Cycle 2 application separates what carried forward, was revalidated, returned for a decision, was new or lost support. Changed evidence returns to professional review.', 8),
    ('Professional approval remains traceable.', 'approval', 'review', 'The approved Crosswalk records Version 2 and Maya Chen as its professional approver. No automatic approval is demonstrated or implied.', 8),
    ('Explore HarbourLink. Follow the evidence.', 'guide', 'link', 'Explore the fictional HarbourLink practice project. Inspect the source assertion, interpretation, evidence, decision and next reporting cycle.', 8),
]

def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)

def icon(draw, kind, x, y):
    c=GOLD
    if kind == 'cycle':
        draw.arc((x,y,x+42,y+42),25,320,fill=c,width=3)
        draw.polygon([(x+40,y+6),(x+29,y+7),(x+39,y+17)],fill=c)
    elif kind == 'chart':
        for i,h in enumerate([17,30,40]):draw.rectangle((x+i*15,y+42-h,x+i*15+9,y+42),fill=c)
    elif kind == 'review':
        draw.rounded_rectangle((x,y,x+42,y+42),radius=9,outline=c,width=3)
        draw.line([(x+9,y+21),(x+18,y+30),(x+34,y+11)],fill=c,width=4)
    elif kind == 'tree':
        draw.line([(x+8,y+4),(x+8,y+38),(x+36,y+38)],fill=c,width=3)
        for dy in [8,23,38]:draw.line([(x+8,y+dy),(x+36,y+dy)],fill=c,width=3)
    elif kind == 'eye':
        draw.ellipse((x,y+8,x+45,y+34),outline=c,width=3)
        draw.ellipse((x+16,y+13,x+29,y+28),fill=c)
    else:
        draw.rounded_rectangle((x+5,y,x+37,y+43),radius=4,outline=c,width=3)
        for dy in [12,22,32]:draw.line((x+12,y+dy,x+30,y+dy),fill=c,width=2)

@lru_cache(maxsize=32)
def load_image(path):
    return Image.open(path).convert("RGB")

def image_for(name, progress):
    motion=WORK / "motion" / name / f"{min(191,int(progress*192))+1:04d}.jpg"
    if motion.exists():
        return Image.open(motion).convert("RGB")
    if name == 'integration':
        image=Image.new('RGB',(1760,780),BG)
        diagram=load_image(HERE/'harbourlink_ui/integration.png').copy()
        diagram.thumbnail((620,760),Image.Resampling.LANCZOS)
        image.paste(diagram,(15,(780-diagram.height)//2))
        finding=load_image(HERE/'harbourlink_ui/project.png').crop((0,0,1450,520))
        finding.thumbnail((1090,740),Image.Resampling.LANCZOS)
        image.paste(finding,(655,(780-finding.height)//2))
        return image
    if name == 'report':
        im=load_image(DOCS/'assets/flagship/executive-briefing-cycle2.png')
        # Magnified complete summary body; only outside margins omitted.
        box=(60,50,im.width-60,1225)
        return im.crop(box)
    if name == 'charts':
        # Two charts at a time, full chart images with no cover-cropping.
        if progress<.25:
            return load_image(DOCS/'assets/flagship/premium-executive-view.png')
        indices=[1,2] if progress<.625 else [3,4]
        pair=Image.new('RGB',(1760,690),'white')
        for j,i in enumerate(indices):
            im=load_image(DOCS/f'assets/flagship/chart{i}.png').copy()
            im.thumbnail((860,640),Image.Resampling.LANCZOS)
            pair.paste(im,(j*880+(880-im.width)//2,(690-im.height)//2))
        return pair
    if name=='approval':
        im=load_image(HERE/'harbourlink_ui/approval.png')
    else:
        im=load_image(HERE/f'harbourlink_ui/{name}.png')
    if name=='project' and progress<.5:
        return im.crop((0,0,im.width,min(730,im.height)))
    return im

def render(index, t):
    title,name,kind,caption,duration=SCENES[index]
    progress=t/duration
    frame=Image.new('RGB',(W,H),BG)
    draw=ImageDraw.Draw(frame)
    draw.text((72,28),'WBS↔LINK',font=font(25,True),fill=WHITE)
    draw.text((280,33),'HARBOURLINK  /  SYNTHETIC APPLICATION DEMONSTRATION',font=font(18),fill=GOLD)
    draw.text((W-172,32),f'{index+1:02d} / 10',font=font(20),fill=GOLD)
    icon(draw,kind,74,94)
    draw.text((144,89),title,font=font(41,True),fill=WHITE)
    shot=image_for(name,progress)
    maxw,maxh=1760,780
    scale=min(maxw/shot.width,maxh/shot.height)
    # Subtle motion preserves the entire visual; no image clipping.
    scale*=.965+.025*(.5-.5*math.cos(math.pi*progress))
    size=(int(shot.width*scale),int(shot.height*scale))
    shot=shot.resize(size,Image.Resampling.LANCZOS)
    x=(W-shot.width)//2;y=180+(maxh-shot.height)//2
    draw.rounded_rectangle((x-8,y-8,x+shot.width+8,y+shot.height+8),radius=16,fill=(58,70,89))
    frame.paste(shot,(x,y))
    draw=ImageDraw.Draw(frame)
    # An animated navigation trail links actual views without fabricating clicks.
    for j,lab in enumerate(['Finding','Owner WBS','Evidence','Decision','Outputs','Cycle 2']):
        px=80+j*273
        active=j<=min(5,index//2)
        draw.ellipse((px,987,px+9,996),fill=GOLD if active else (71,83,105))
        draw.text((px+18,980),lab,font=font(17),fill=WHITE if active else (126,139,158))
        if j<5:draw.line((px+162,991,px+252,991),fill=GOLD if active else (49,61,83),width=2)
    draw.text((80,1032),'Actual candidate visuals · professional authority retained · fictional data only',font=font(16),fill=(164,177,194))
    draw.rectangle((0,H-5,int(W*(index+progress)/len(SCENES)),H),fill=GOLD)
    # Short scene-edge fades keep transitions quiet and coherent.
    fade=min(1,t/.32,(duration-t)/.32)
    if fade<1:frame=Image.blend(Image.new('RGB',(W,H),BG),frame,max(0,fade))
    return frame

def score(duration):
    rate=48000
    mix=np.zeros((duration*rate,2),dtype=np.float64)
    rng=np.random.default_rng(73)
    def note(start,length,midi,gain,pan=0,soft=False):
        n=int(length*rate);tt=np.arange(n)/rate;freq=440*2**((midi-69)/12)
        envelope=(1-np.exp(-tt/(.24 if soft else .012)))*np.exp(-tt/(2.3 if soft else .55))
        envelope*=np.minimum(1,np.maximum(0,(length-tt)/.18))
        tone=(np.sin(2*np.pi*freq*tt)+.28*np.sin(4*np.pi*freq*tt)+.08*np.sin(6*np.pi*freq*tt))*envelope*gain
        start=int(start*rate);n=min(n,len(mix)-start)
        if n>0:
            mix[start:start+n,0]+=tone[:n]*(.7-.25*pan)
            mix[start:start+n,1]+=tone[:n]*(.7+.25*pan)
    chords=[[48,55,60,63],[44,51,56,60],[51,58,63,67],[46,53,58,62]]
    beat=60/90
    for bar in range(math.ceil(duration/(beat*4))):
        start=bar*beat*4;chord=chords[(bar//2)%4]
        for j,m in enumerate(chord):note(start,beat*4,m,.055,pan=(j-1.5)/2,soft=True)
        note(start,beat*2,chord[0]-12,.09)
        for step in range(8):note(start+step*beat/2,beat*1.3,chord[step%4]+12,.065,pan=(-1 if step%2 else 1)*.6)
        for step in range(4):
            at=start+step*beat
            if at>=duration:continue
            n=int(.18*rate);tt=np.arange(n)/rate
            if step in [0,2]:hit=np.sin(2*np.pi*(55*tt+30*(1-np.exp(-tt*30))/30))*np.exp(-tt*26)*.1
            else:hit=rng.normal(size=n)*np.exp(-tt*60)*.018
            i=int(at*rate);n=min(n,len(mix)-i);mix[i:i+n]+=hit[:n,None]
    ramp=np.minimum(1,np.arange(len(mix))/rate/2)*np.minimum(1,(len(mix)-np.arange(len(mix)))/rate/3)
    mix*=ramp[:,None]
    mix/=max(1,np.max(np.abs(mix))/.8)
    with wave.open(str(WORK/'score.wav'),'wb') as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(rate);f.writeframes((mix*32767).astype('<i2').tobytes())

if __name__=='__main__':
    duration=sum(s[-1] for s in SCENES)
    out=DOCS/'videos/wbslink-video-2-how-it-works.mp4'
    score(duration)
    cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(WORK/'score.wav'),'-map','0:v','-map','1:a','-af','loudnorm=I=-20:TP=-2:LRA=7','-c:v','libx264','-preset','veryfast','-threads','2','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-shortest',str(out)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    vtt=['WEBVTT',''];clock=0
    def stamp(seconds):return f'00:{int(seconds)//60:02d}:{int(seconds)%60:02d}.000'
    board=[]
    for index,scene in enumerate(SCENES):
        title,name,kind,caption,seconds=scene
        still=render(index,seconds*.4)
        still.save(WORK/f'storyboard-{index+1:02d}.jpg',quality=92)
        if index==0:still.save(DOCS/'videos/wbslink-video-2-how-it-works.jpg',quality=92)
        board.append(f'{clock:02d}–{clock+seconds:02d}s | {title} | actual {name} visual | {caption}')
        vtt.extend([f'{stamp(clock)} --> {stamp(clock+seconds)}',caption,''])
        for n in range(seconds*FPS):process.stdin.write(render(index,n/FPS).tobytes())
        clock+=seconds
        print(f'Scene {index+1}/10 encoded',flush=True)
    process.stdin.close()
    assert process.wait()==0
    (DOCS/'videos/wbslink-video-2-harbourlink.vtt').write_text('\n'.join(vtt))
    (HERE/'HARBOURLINK_STORYBOARD.txt').write_text('\n'.join(board)+'\n')
    print(out)
