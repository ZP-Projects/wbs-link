"""A 60-second original graphic explainer over actual approved report evidence.

No stock montage, fabricated application transaction, new speech, or new licence.
Concept diagrams are labelled; actual report components carry capture custody.
"""
from pathlib import Path
import json,argparse,subprocess,hashlib,re
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;VIDEO=HERE.parent
NAVY='#121A2E';PAPER='#F5F5F3';GREY='#565B64';ACCENT='#8F5A28';LIGHT='#C98F52'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def build(model,proof,work):
 model=Path(model);m=json.loads(model.read_text());proof=Path(proof);work=Path(work);work.mkdir(parents=True,exist_ok=True)
 action=next(x['next'] for x in m['findings'] if x.get('branch',{}).get('code')=='1.5')
 fonts=HERE/'fonts'
 def font(size,bold=False):return ImageFont.truetype(str(fonts/('Archivo-700.ttf' if bold else 'Archivo-400.ttf')),size)
 def text(d,s,x,y,w,size=44,bold=False,colour=NAVY):
  f=font(size,bold)
  def drawline(line,x,y):
   for part in re.split('([↔→≠])',line):
    if not part:continue
    face=ImageFont.truetype(str(VIDEO.parent/'assets/fonts/DejaVuSans.ttf'),size) if part in ['↔','→','≠'] else f
    d.text((x,y),part,font=face,fill=colour);x+=d.textlength(part,font=face)
  for para in s.split('\n'):
   line=''
   for word in para.split():
    a=(line+' '+word).strip()
    if line and d.textlength(a,font=f)>w:drawline(line,x,y);y+=size*1.25;line=word
    else:line=a
   drawline(line,x,y);y+=size*1.25
  return y
 titles=['Credible records. Different views of the work.','A familiar code does not settle the relationship.','An absent view limits the management comparison.','Make the review need explicit.','Relate each view through the Owner WBS.','Keep the original assertion visible.','Record what was actually decided.','Approve the reporting position separately.','Changed evidence requires renewed review.','Turn the gap into an evidence-led conversation.']
 captions=[
 'Schedule, cost and package records can each be credible while describing project work differently.',
 'A source WBS Code is an assertion. Its meaning still requires evidence and professional judgement.',
 'HarbourLink has 180 Testing and Commissioning schedule relationships. Cost relationships are absent; this does not establish zero cost or missing work.',
 action,
 'Schedule, cost and package information relate independently through the owner’s Work Breakdown Structure. No direct schedule-to-cost equivalence is implied.',
 'Inspect the original source assertion and contrary evidence. Software interpretation is separate from a professional decision.',
 'A separate cost example records a group decision to keep 81 relationships unresolved. That scope does not extend to every relationship.',
 'Maya Chen’s fictional recorded whole-version approval establishes the reporting position. It does not individually confirm every relationship.',
 'July unresolved relationships increase from 263 to 264, including one package relationship. Both work-area gaps remain; cause and impact are not established.',
 'Read the approved Management Report and exact Action. Follow the workbook evidence before drawing a project conclusion.'
 ]
 frames=[];segments=[]
 def box(d,x,y,w,h,label,sub):
  d.rectangle((x,y,x+w,y+h),fill='white',outline='#D7D9D5',width=2);text(d,label,x+28,y+28,w-56,38,True);text(d,sub,x+28,y+95,w-56,30,False,GREY)
 for i,title in enumerate(titles):
  im=Image.new('RGB',(1920,1080),PAPER);d=ImageDraw.Draw(im);d.rectangle((0,0,1920,10),fill=ACCENT)
  text(d,'WBS↔LINK · ZP SYNERGY GROUP INC.',90,50,1740,30,True);text(d,title,90,140,1740,66,True)
  text(d,'FICTIONAL HARBOURLINK · '+('EXPLANATORY DIAGRAM' if i in [0,1,4,8,9] else 'APPROVED REPORT EVIDENCE'),90,310,1740,25,True,ACCENT)
  if i==0:
   for j,(a,b) in enumerate([('Schedule','Sequence and activities'),('Cost / forecast','Accounts and amounts'),('Work packages','Commercial scope')]):
    x=90+j*590;box(d,x,405,555,260,a,b)
    # Different original structures, not a copied software screen.
    for k in range(3):d.rectangle((x+30+k*25,590+k*14,x+470,594+k*14),fill=ACCENT)
   text(d,'Where do these records describe the same work?',90,775,1740,56,True)
  elif i==1:
   box(d,90,410,720,285,'Original source assertion','WBS Code = 1.5.1')
   text(d,'≠',895,475,160,110,True,ACCENT) # Graphic separator; no implied source-to-source relationship.
   box(d,1100,410,730,285,'Professional confirmation','Not established by the code alone')
   text(d,'Evidence → interpretation → scoped professional decision',90,800,1740,43,True)
  elif i in [2,5,6,7]:
   name={2:'gap',5:'stage1',6:'bounded-decision',7:'stage4'}[i];p=Image.open(proof/(name+'-1440.png')).convert('RGB');scale=min(1740/p.width,540/p.height);p=p.resize((round(p.width*scale),round(p.height*scale)),Image.Resampling.LANCZOS);im.paste(p,(90,390));d=ImageDraw.Draw(im)
   notes={2:'Work-area counts establish the missing cost view. A single record alone does not.',5:'Original assertion, interpretation, contrary evidence and approval remain distinct.',6:'Separate cost example · group of 81 · no invented individual confirmation.',7:'Fictional recorded attribution; professional identity is not independently verified.'}
   text(d,notes[i],90,390+p.height+45,1740,34,False,GREY)
  elif i==3:
   d.rectangle((90,415,1830,850),fill=NAVY);text(d,'EXACT RECORDED ACTION',130,450,1660,29,True,LIGHT);text(d,action,130,535,1660,62,True,PAPER)
   text(d,'No invented assignee, deadline, cause or financial effect.',90,900,1740,32,False,GREY)
  elif i==4:
   for j,a in enumerate(['Schedule','Cost / forecast','Work packages']):
    x=90+j*590;box(d,x,410,555,150,a,'')
    d.line((x+277,575,960,740),fill=ACCENT,width=5)
   d.rectangle((580,740,1340,880),fill=NAVY);text(d,'Owner WBS',640,780,640,60,True,PAPER)
   text(d,'Independent relationships · original assertions preserved',90,935,1740,31,False,GREY)
  elif i==8:
   box(d,90,410,840,340,'Unresolved relationships','June 263  →  July 264\nPackage unresolved: 0  →  1')
   box(d,990,410,840,340,'Both views present','4 of 6 work areas\nThe same two gaps remain')
   text(d,'A reporting change is not a proven project impact.',90,850,1740,47,True)
  else:
   for j,(a,b) in enumerate([('Management Report','Position · gap · exact Action'),('Premium Workbook','Original evidence · decision scope'),('Management review','Check what is expected')]):box(d,90+j*590,420,555,300,a,b)
   text(d,'Start with the July Testing and Commissioning finding.',90,820,1740,48,True)
  text(d,f'{i+1:02d} / 10 · Coverage is not progress or project health.',90,1015,1740,24,False,GREY)
  frame=work/f'scene-{i+1:02d}.png';im.save(frame);frames.append(frame);seg=work/f'scene-{i+1:02d}.mp4';segments.append(seg)
  subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-i',str(frame),'-t','6','-r','24','-vf','fade=t=in:st=0:d=0.2,fade=t=out:st=5.8:d=0.2','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','2','-pix_fmt','yuv420p',str(seg)],check=True);print('ENCODED FILM1',i+1,flush=True)
 listing=work/'segments.txt';listing.write_text(''.join("file '"+str(p.resolve())+"'\n" for p in segments));picture=work/'picture.mp4';subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(picture)],check=True)
 # Retain the licensed, previously authored instrumental; not faux site Foley under diagrams.
 audio=work.parent/'film2/retained-film2-audio.aac';assert audio.exists();out=VIDEO/'wbslink-video-1-challenge.mp4'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(picture),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','copy','-af','afade=t=out:st=57:d=3,volume=0.8','-c:a','aac','-b:a','160k','-t','60','-movflags','+faststart',str(out)],check=True)
 def stamp(t):return f'00:{t//60:02d}:{t%60:02d}.000'
 vtt='WEBVTT\n\n'+''.join(f'{i+1}\n{stamp(i*6)} --> {stamp((i+1)*6)}\n'+('[Recorded instrumental music; no spoken narration]\n' if i==0 else '')+s+'\n\n' for i,s in enumerate(captions));(VIDEO/'wbslink-video-1-cinematic.vtt').write_text(vtt.rstrip()+'\n')
 (work/'PROVENANCE.json').write_text(json.dumps({'source_model_sha256':sha(model),'actual_capture_provenance_sha256':sha(proof/'PROVENANCE.json'),'film_sha256':sha(out),'captions':captions,'scenes':[{'scene':i+1,'start':i*6,'duration':6,'image_sha256':sha(p),'purpose':titles[i]} for i,p in enumerate(frames)],'audio':'60s excerpt from existing licensed Advertime instrumental; level0.8, final3s fade; no new voice/media dependency. Historical Foley no longer accompanies graphic scenes.','human_listening':'NOT VERIFIED','source':'Approved fictional report model only; no hidden oracle or client data'},indent=2)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--model',required=True);p.add_argument('--proof',required=True);p.add_argument('--work',required=True);a=p.parse_args();build(a.model,a.proof,a.work)
