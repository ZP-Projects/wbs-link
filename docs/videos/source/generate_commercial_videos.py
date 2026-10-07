from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import subprocess, shutil

ROOT = Path(__file__).resolve().parents[2]
VIDEO_DIR = ROOT / 'videos'
ASSET = ROOT / 'assets' / 'flagship'
WORK = VIDEO_DIR / 'source' / '_frames'
WORK.mkdir(parents=True, exist_ok=True)

W,H=1920,1080
BG=(15,21,37); INK=(235,236,232); MUTED=(174,180,190); ACC=(196,137,83); PALE=(42,52,72); GOOD=(95,145,120)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONTB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def font(sz,b=False): return ImageFont.truetype(FONTB if b else FONT, sz)

def wrap(draw, text, f, width):
    words=text.split(); lines=[]; cur=''
    for word in words:
        test=(cur+' '+word).strip()
        if draw.textbbox((0,0),test,font=f)[2] <= width: cur=test
        else:
            if cur: lines.append(cur)
            cur=word
    if cur: lines.append(cur)
    return lines

def cover_crop(img, size):
    w,h=size
    im=img.copy().convert('RGB')
    ratio=max(w/im.width,h/im.height)
    im=im.resize((int(im.width*ratio),int(im.height*ratio)),Image.LANCZOS)
    l=(im.width-w)//2; t=(im.height-h)//2
    return im.crop((l,t,l+w,t+h))

def frame(title, body, kicker='WBS↔LINK', image=None, badge=None, footer=None, diagram=None):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,10),fill=ACC)
    d.text((110,70),kicker,font=font(25,True),fill=ACC)
    left=110; top=190; textw=760 if image else 1550
    for line in wrap(d,title,font(62,True),textw):
        d.text((left,top),line,font=font(62,True),fill=INK); top+=76
    top+=25
    for line in wrap(d,body,font(31),textw):
        d.text((left,top),line,font=font(31),fill=MUTED); top+=46
    if badge:
        bx=left; by=min(top+35,H-145); bb=d.textbbox((0,0),badge,font=font(22,True)); bw=bb[2]+42
        d.rounded_rectangle((bx,by,bx+bw,by+50),radius=14,fill=PALE,outline=ACC,width=2)
        d.text((bx+21,by+12),badge,font=font(22,True),fill=INK)
    if image:
        path=ASSET/image
        if path.exists():
            shot=Image.open(path)
            box=(980,125,825,790)
            shot=cover_crop(shot,(box[2],box[3]))
            shot=shot.filter(ImageFilter.GaussianBlur(.15))
            im.paste(shot,(box[0],box[1]))
            d.rounded_rectangle((box[0]-5,box[1]-5,box[0]+box[2]+5,box[1]+box[3]+5),radius=16,outline=(77,88,109),width=4)
            d.rounded_rectangle((1195,930,1760,978),radius=12,fill=(20,29,49))
            d.text((1220,943),'Accepted synthetic flagship evidence',font=font(19),fill=MUTED)
    if diagram: diagram(im,d)
    if footer: d.text((110,1010),footer,font=font(19),fill=(120,128,143))
    return im

def spine(im,d):
    labels=[('SCHEDULE',160,690),('COST / FORECAST',160,820),('PACKAGE / CONTRACT',160,950)]
    for lab,x,y in labels:
        d.rounded_rectangle((x,y,x+390,y+82),radius=14,fill=(27,36,57),outline=(76,88,108),width=2)
        d.text((x+22,y+25),lab,font=font(24,True),fill=INK)
        d.line((x+390,y+41,840,y+41),fill=ACC,width=4)
    d.rounded_rectangle((840,735,1290,930),radius=22,fill=(44,38,51),outline=ACC,width=4)
    d.text((940,780),'OWNER WBS',font=font(34,True),fill=INK)
    d.text((900,835),'integration spine',font=font(24),fill=ACC)
    d.line((1290,832,1630,832),fill=ACC,width=4)
    d.rounded_rectangle((1630,760,1810,905),radius=18,fill=(24,48,42),outline=GOOD,width=3)
    d.text((1660,790),'GOVERNED',font=font(22,True),fill=INK)
    d.text((1655,830),'RELATIONSHIP',font=font(22,True),fill=INK)
    d.text((1680,870),'STATE',font=font(22,True),fill=INK)

video1=[
 ('Same project. Different structures.', 'Schedule, cost/forecast, package and contract views can each be credible — and still organize the project differently.', None, None),
 ('Each view makes sense on its own.', 'The contractor schedule follows delivery logic. Cost follows control accounts. Packages follow commercial scope. The owner still needs one authorized project structure.', None, None),
 ('The hard part is not joining files.', 'It is establishing whether independently authored records really describe the same authorized scope — and knowing where they do not.', 'project-intelligence-cycle1.png', None),
 ('Some relationships are clear. Some are not.', 'A missing relationship is a question. An unsupported relationship should stay uncertain until evidence or professional judgment resolves it.', 'cycle2-changes.png', None),
 ('The Owner WBS is the integration spine.', 'WBS↔LINK preserves each source view and connects it through governed relationships to the Owner WBS — not by inventing direct source-to-source truth.', None, spine),
 ('Professional authority stays visible.', 'Evidence, uncertainty and professional decisions remain distinct. Approval governs the relationship state; it does not turn inference into source fact.', 'outputs-cycle1.png', None),
 ('And the work can persist.', 'When the next reporting cycle arrives, relationships that remain valid carry forward. Only affected relationships return for renewed attention.', 'cycle2-changes.png', None),
 ('Make relationship integrity visible, governable and reusable.', 'WBS↔LINK helps project teams see whether their control views actually reconcile through the Owner WBS — and preserve that intelligence across reporting cycles.', None, None),
]

video2=[
 ('Start with an ordinary project.', 'A project has an Owner WBS and independently authored schedule, cost/forecast and package/contract files.', None),
 ('Upload the project-control views.', 'WBS↔LINK receives ordinary structured project files. Source systems remain the source systems.', None),
 ('First: understand each source.', 'The product establishes what each file represents, its structure and where interpretation is still required.', 'project-intelligence-cycle1.png'),
 ('Do not force unsupported relationships.', 'If the evidence does not support placement, uncertainty stays visible. Professional input is exception-first.', 'project-intelligence-cycle1.png'),
 ('Review the relationships that need judgment.', 'The user can inspect evidence, competing interpretations and the WBS scope before making a professional decision.', 'cycle1-project-desktop.png' if (ASSET/'cycle1-project-desktop.png').exists() else 'project-intelligence-cycle1.png'),
 ('Approve the governed relationship state.', 'Approval records the accepted relationship state and professional authority. It does not replace source evidence.', 'outputs-cycle1.png'),
 ('Project Intelligence shows what matters now.', 'See where project views align through the Owner WBS, where gaps remain, and where attention is required.', 'project-intelligence-cycle1.png'),
 ('Carry the approved intelligence outside the app.', 'The Premium Workbook provides the deeper working view. The one-page management briefing carries the reporting-cycle message.', 'premium-workbook.png'),
 ('Next cycle: do not rebuild the crosswalk.', 'WBS↔LINK carries forward what remains valid, revalidates affected relationships and isolates reopened, new or retired items.', 'cycle2-changes.png'),
 ('Persistent governed intelligence.', 'The value compounds across reporting cycles: retained state, visible change, bounded revalidation and a reusable evidence trail.', 'cycle2-changes.png'),
]

def make_video(name, scenes, durations):
    vwork=WORK/name; shutil.rmtree(vwork,ignore_errors=True); vwork.mkdir(parents=True)
    imgs=[]
    for idx,(title,body,img,*rest) in enumerate(scenes,1):
        diagram=rest[0] if rest else None
        fr=frame(title,body,image=img,diagram=diagram,footer='Synthetic demonstration. No real-client provenance or performance claim.')
        p=vwork/f'{idx:02d}.png'; fr.save(p); imgs.append(p)
    listfile=vwork/'concat.txt'
    with listfile.open('w') as f:
        for p,dur in zip(imgs,durations):
            f.write(f"file '{p.as_posix()}'\n")
            f.write(f"duration {dur}\n")
        f.write(f"file '{imgs[-1].as_posix()}'\n")
    silent=vwork/'silent.mp4'
    subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(listfile),'-vf','fps=30,format=yuv420p','-c:v','libx264','-crf','19','-preset','medium',str(silent)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    total=sum(durations)
    out=VIDEO_DIR/f'{name}.mp4'
    subprocess.run(['ffmpeg','-y','-i',str(silent),'-f','lavfi','-i',f'sine=frequency=110:sample_rate=48000:duration={total+1}',
                    '-filter_complex','[1:a]volume=0.018,lowpass=f=300[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','96k','-shortest',str(out)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    shutil.copy(imgs[0],VIDEO_DIR/f'{name}.jpg')
    return out

make_video('wbslink-video-1-challenge',video1,[8,8,8,8,9,8,8,9])
make_video('wbslink-video-2-how-it-works',video2,[8,8,8,8,8,8,8,8,9,9])
