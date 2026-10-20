"""Eight-scene /60s WHY film. Original cinematic illustrations and governed evidence.

Real motion in source reveals, independent reference paths, gap contrast and the
finding-to-Action resolution. No fictional invoice, delay fact, UI or approval.
"""
from pathlib import Path
import argparse,json,hashlib,subprocess,wave
import numpy as np
from PIL import Image,ImageDraw
from drawing import Draw,ease,contained,N,MID,PAPER,WHITE,GREY,COG,CL,STEEL,LIGHT
from vector_system import icon,scene2
HERE=Path(__file__).resolve().parent;VIDEO=HERE.parents[1];ART=HERE/'art';FPS=24
SCENES=[
 ('Month-end. Four views to reconcile.',6,'Month-end. The owner’s controls manager must reconcile scope, schedule, cost and work-package records.'),
 ('Payment requests need a clear review basis.',6,'Contractors expect payment. Leadership needs a clear basis for reviewing the payment applications.'),
 ('Are we reviewing the same work?',8,'If activities appear behind schedule, why are we paying so much? Are these records describing the same work?'),
 ('Different records. Different structures.',7,'The records may each be valid. Their codes and scope boundaries can still differ.'),
 ('Owner WBS is the shared reference.',9,'WBS LINK relates each source through the Owner WBS, preserving its evidence and decision authority.'),
 ('The gap stays visible.',8,'Here, a cost relationship is absent. Uncertainty stays visible. Professional decisions and whole-version approval remain separate.'),
 ('A precise Action. An evidence path.',10,'Confirm whether the missing governed relationship is expected or requires project-controls attention. Keep that Action linked to its original evidence.'),
 ('From the question to the evidence.',6,'Follow the source-to-report workflow in Video 2, including professional review and separate version approval.')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def build(model,report,proof,work,inspect_only=False):
 model=Path(model);m=json.loads(model.read_text());report_path=Path(report);report=Image.open(report_path).convert('RGB');proof=Path(proof);work=Path(work);work.mkdir(parents=True,exist_ok=True)
 assert m['project']=='HarbourLink Urban Transit Expansion' and m['source']['total']==1622
 assert sum(n for label,n in m['outcomes']['rows'] if 'UNSURE' in label)==264
 custody=json.loads((proof/'PROVENANCE.json').read_text());assert len(custody)==24
 assert all(row['source_sha256']==sha(model.parent/'Integrated_Management_Report.html') and row['sha256']==sha(proof/row['image']) for row in custody)
 action=next(f['next'] for f in m['findings'] if (f.get('branch') or {}).get('code')=='1.5');assert SCENES[6][2].startswith(action)
 art=[Image.open(ART/n).convert('RGB') for n in ['01_controls_manager.png','02_contractor_lead.png','03_ceo_question.png']]
 actuals={False:Image.open(proof/'stage1-640.png').convert('RGB'),True:Image.open(proof/'stage1-390.png').convert('RGB')};records=[];outputs=[]
 def frame(i,t,phone):
  W,H=(1080,1920) if phone else (1920,1080);d=Draw(W,H);margin=68 if phone else 90;local=t/SCENES[i][1]
  if i<3:
   photo=art[i];z=1.025+.045*local
   if phone:
    pic=contained(photo,1080*z,615*z);crop=pic.crop(((pic.width-1080)//2,0,(pic.width+1080)//2,min(pic.height,615))) if pic.width>=1080 else pic
    d.im.paste(crop,(0,550));d.d=ImageDraw.Draw(d.im);d.brand(margin,55,38);d.text(margin,121,'ILLUSTRATIVE MONTH-END SCENARIO',31,True,CL,width=W-2*margin)
    titles=['Month-end.\nFour views\nto reconcile.','Payment requests\nneed a clear\nreview basis.','Are we reviewing\nthe same work?']
    d.text(margin,215,titles[i],70,True,width=W-2*margin,leading=79)
    if i==0:
     for j,(glyph,label) in enumerate([('schedule','Schedule'),('cost','Cost / Forecast'),('packages','Work Packages'),('wbs','Owner WBS')]):icon(d,glyph,margin,1240+j*90,43,WHITE);d.text(margin+68,1244+j*90,label,43)
    elif i==1:d.text(margin,1240,'Contractor expectation.\nClient payment review.',49,width=W-2*margin,leading=67)
    else:d.text(margin,1240,'If activities appear behind schedule,\nwhat supports the payment review?',47,width=W-2*margin,leading=64)
    d.text(margin,1700,'Fictional illustration, not HarbourLink footage or payment evidence.',34,col=STEEL,width=W-2*margin,leading=45)
    d.text(margin,1810,'Payment authorization remains with the client.',34,True,width=W-2*margin)
   else:
    pw,ph=round(W*z),round(H*z);pic=photo.resize((pw,ph),Image.Resampling.LANCZOS);d=Draw(W,H,pic.crop(((pw-W)//2,(ph-H)//2,(pw+W)//2,(ph+H)//2)))
    overlay=Image.new('RGBA',(W,H));od=ImageDraw.Draw(overlay);od.rectangle((0,0,W*.445,H),fill=(18,26,46,244));d.im=Image.alpha_composite(d.im.convert('RGBA'),overlay).convert('RGB');d.d=ImageDraw.Draw(d.im)
    d.brand(margin,50,31);d.text(margin,126,'ILLUSTRATIVE MONTH-END SCENARIO',24,True,CL)
    titles=['Month-end.\nFour views\nto reconcile.','Payment requests\nneed a clear\nreview basis.','Are we reviewing\nthe same work?']
    d.text(margin,230,titles[i],70,True,width=720,leading=81)
    if i==0:
     for j,(glyph,label) in enumerate([('schedule','Schedule'),('cost','Cost / Forecast'),('packages','Work Packages'),('wbs','Owner WBS')]):icon(d,glyph,margin,560+j*76,36,WHITE);d.text(margin+57,563+j*76,label,34)
    elif i==1:d.text(margin,600,'Contractor expectation.\nClient payment review.',42,width=700,leading=58)
    else:d.text(margin,595,'An executive question\nbefore payment sign-off.',42,width=700,leading=58)
    d.rect(0,H-70,W,70,N);d.text(margin,H-51,'Fictional illustration, not HarbourLink footage or payment evidence. Payment authorization remains with the client.',24,col=STEEL,width=W-2*margin)
  elif i==4:
   scene2(d,0,0,W,H,min(t,8.8),m['coverage']['branches'],mobile=phone)
  else:
   d.brand(margin,55,38 if phone else 32);d.text(margin,121 if phone else 105,'APPROVED SYNTHETIC HARBOURLINK  /  EXPLANATORY EXHIBIT',26 if phone else 24,True,CL,width=W-2*margin)
   if i==3:
    d.text(margin,205 if phone else 178,'Different records.\nDifferent structures.' if phone else 'Different records. Different structures.',66 if phone else 64,True,width=W-2*margin,leading=75)
    specs=[('schedule','Schedule Source','SCH-05-001','WBS Code = 1.5.1'),('cost','Cost / Forecast','CST-06-001','Cost Account = CA-6001; WBS Code = 1.6.1'),('packages','Work Packages','60 current relationships','59 related; 1 unresolved')]
    for j,(glyph,title,key,assertion) in enumerate(specs):
     amount=ease((t-j*.75)/1.2);offset=(1-amount)*150
     x=margin if phone else margin+j*590;yy=(470+j*330 if phone else 390+j*45)+offset;ww=W-2*margin if phone else 555;hh=275 if phone else 355
     d.rect(x,yy,ww,hh,PAPER);icon(d,glyph,x+30,yy+30,42,COG);d.text(x+100,yy+35,title,43 if phone else 40,True,N,width=ww-125)
     d.line(x+30,yy+110,x+ww-30,yy+110,LIGHT,2);d.text(x+30,yy+140,key,43 if phone else 36,True,N,width=ww-60)
     d.text(x+30,yy+215,assertion,38 if phone else 34,col=GREY,width=ww-60,leading=48)
    d.text(margin,1630 if phone else 915,'Each record keeps its identity. A shared code alone does not settle the relationship.',42 if phone else 35,width=W-2*margin,leading=55)
   elif i==5:
    d.text(margin,205 if phone else 176,'Testing and\nCommissioning' if phone else 'Testing and Commissioning',66 if phone else 64,True,width=W-2*margin,leading=75)
    d.text(margin,386 if phone else 282,'OWNER WBS 1.5',34 if phone else 28,True,CL)
    yy=500 if phone else 380;ww=W-2*margin if phone else 815;hh=275 if phone else 330
    for j in [0,1]:
     x=margin if phone else margin+j*925;y=yy+j*330 if phone else yy;d.rect(x,y,ww,hh,PAPER);icon(d,'schedule' if j==0 else 'cost',x+30,y+28,43,COG)
     if j==0:d.text(x+100,y+40,'180',106,True,N);d.text(x+34,y+188,'schedule relationships',45 if phone else 39,col=N,width=ww-68)
     elif t>1.4:
      shift=(1-ease((t-1.4)/1.1))*70;d.text(x+100,y+45+shift,'ABSENT',90,True,COG,width=ww-135);d.text(x+34,y+188,'Cost relationships for this work area',40 if phone else 36,col=N,width=ww-68)
    end=1220 if phone else 785;d.text(margin,end,'264 relationships remain unresolved overall.',45 if phone else 39,True,width=W-2*margin)
    d.text(margin,end+90,'Use only conclusions that do not depend on these unresolved relationships.',43 if phone else 36,width=W-2*margin,leading=56)
    d.text(margin,1725 if phone else 1000,'An absent relationship is not zero project cost or evidence of payment entitlement.',34 if phone else 27,col=STEEL,width=W-2*margin,leading=44)
   elif i==6:
    d.text(margin,205 if phone else 176,'A precise Action.\nAn evidence path.' if phone else 'A precise Action. An evidence path.',66 if phone else 64,True,width=W-2*margin,leading=75)
    if phone:
     y=470;d.rect(margin,y,W-2*margin,520,MID);d.text(margin+32,y+30,'EXACT PROFESSIONAL ACTION',31,True,CL,width=W-2*margin-64);d.text(margin+32,y+103,action,58,True,width=W-2*margin-64,leading=76)
     pic=contained(report,350,500);d.im.paste(pic,(margin,1100));d.d=ImageDraw.Draw(d.im)
     d.text(455,1120,'Original assertion',40,True,CL,width=550);d.text(455,1210,'WBS Code = 1.5.1',43,True,width=550);d.text(455,1325,'Source assignment, not individually reviewed.',39,width=550,leading=51)
     d.text(margin,1660,'F-0611c8162d / SCH-05-001\nWhole-version approval remains separate.',34,col=STEEL,width=W-2*margin,leading=46)
    else:
     pic=contained(report,430,660);xx=margin-45*(1-ease(t/2));d.im.paste(pic,(round(xx),350));d.d=ImageDraw.Draw(d.im)
     x=590;d.text(x,355,'EXACT PROFESSIONAL ACTION',28,True,CL);d.text(x,430,action,62,True,width=1240,leading=79)
     d.line(x,755,1830,755,STEEL,1);d.text(x,795,'Original assertion: WBS Code = 1.5.1',38,True,width=1240)
     d.text(x,872,'F-0611c8162d / SCH-05-001\nSource assignment, not individually reviewed.',31,col=STEEL,width=1240,leading=44)
   else:
    d.text(margin,205 if phone else 185,'From the question\nto the evidence.',70,True,width=W-2*margin,leading=83)
    d.text(margin,450 if phone else 420,'Follow the source, the review\nand the separate approval.',46 if phone else 43,width=(W-2*margin if phone else 780),leading=62)
    pic=contained(actuals[phone],W-2*margin if phone else 930,600 if phone else 420);x=margin if phone else 910;y=760 if phone else 455;d.im.paste(pic,(x,round(y-35*ease(t/4))));d.d=ImageDraw.Draw(d.im)
    d.text(margin,1530 if phone else 850,'Video 2 follows the governed HarbourLink workflow.',45 if phone else 36,width=W-2*margin,leading=58)
    d.text(margin,1745 if phone else 1000,'Payment authorization remains the client’s process.',34 if phone else 27,col=STEEL,width=W-2*margin)
  return d

 if inspect_only:
  for phone in [False,True]:
   tag='phone' if phone else 'landscape';folder=work/'composition-check'/tag;folder.mkdir(parents=True,exist_ok=True)
   for i,s in enumerate(SCENES):
    d=frame(i,s[1]*.6,phone);d.im.save(folder/f'scene-{i+1:02d}.png')
  print('Internal production composition check rendered. No customer package or design-approval cycle.');return
 # Produce the soundtrack from already licensed recordings. No synthetic noise bed or speech.
 rate=48000;music=HERE.parent/'natural-audio/assets/advertime.mp3';raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(music),'-t','60','-ar',str(rate),'-ac','2','-f','f32le','-']);x=np.frombuffer(raw,'<f4').reshape(-1,2).copy();x*=.30;events=[]
 for name,start,gain in [('paper.ogg',.65,.13),('paper.ogg',6.55,.16),('paper.ogg',20.15,.10),('mouseclick.wav',29.5,.13),('mouseclick.wav',31,.13),('mouseclick.wav',32.5,.13),('paper.ogg',44.4,.11)]:
  src=HERE.parent/'natural-audio/assets'/name;sound=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-ar',str(rate),'-ac','2','-f','f32le','-']),'<f4').reshape(-1,2);count=min(len(sound),int(.65*rate));part=sound[:count].copy();part*=gain/max(.001,float(np.abs(part).max()));at=round(start*rate);x[at:at+count]+=part;events.append({'asset':name,'at':start,'duration':count/rate,'gain':gain,'reason':'Paper/folder or independent graphic reference reveal, designed Foley, not location sound.'})
 x[:rate]*=np.linspace(0,1,rate)[:,None];x[-rate*2:]*=np.linspace(1,0,rate*2)[:,None];wav=work/'designed-soundtrack.wav'
 with wave.open(str(wav),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(rate);w.writeframes((np.clip(x,-.98,.98)*32767).astype('<i2').tobytes())
 audio=work/'film1-final-audio.aac';subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-af','loudnorm=I=-21:TP=-2:LRA=8','-c:a','aac','-b:a','192k',str(audio)],check=True)
 for phone in [False,True]:
  W,H=(1080,1920) if phone else (1920,1080);tag='phone' if phone else 'landscape';folder=work/tag;folder.mkdir(exist_ok=True);picture=folder/'picture.mp4'
  proc=subprocess.Popen(['ffmpeg','-nostdin','-v','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-pix_fmt','yuv420p',str(picture)],stdin=subprocess.PIPE)
  prior_end=None
  try:
   for i,(_,duration,_) in enumerate(SCENES):
    for tick in range(duration*FPS):
     t=tick/FPS;d=frame(i,t,phone);im=d.im
     if prior_end is not None and tick<8:im=Image.blend(prior_end,im,ease((tick+1)/8))
     if tick in [0,round(duration*FPS/2),duration*FPS-1]:
      im.save(folder/f'scene-{i+1:02d}-{tick:03d}.png');records.append({'composition':tag,'scene':i+1,'scene_second':t,'text':d.records})
     proc.stdin.write(im.tobytes())
    prior_end=im;print('ENCODED FILM1',tag,'scene',i+1,flush=True)
  finally:proc.stdin.close()
  assert proc.wait()==0
  name='wbslink-video-1-challenge'+('-phone' if phone else '')+'.mp4';out=VIDEO/name
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(picture),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-c','copy','-t','60','-movflags','+faststart',str(out)],check=True);outputs.append({'file':name,'bytes':out.stat().st_size,'sha256':sha(out),'width':W,'height':H})
 def stamp(t):return f'00:{int(t)//60:02d}:{int(t)%60:02d}.000'
 at=0;vtt='WEBVTT\n\n'
 for i,(_,dur,caption) in enumerate(SCENES):vtt+=f'{i+1}\n{stamp(at)} --> {stamp(at+dur)}\n'+('[Instrumental music and designed paper/interface cues; no spoken narration]\n' if i==0 else '')+caption+'\n\n';at+=dur
 for name in ['wbslink-video-1-cinematic.vtt','wbslink-video-1-challenge-phone.vtt']:(VIDEO/name).write_text(vtt)
 (work/'TEXT_LAYOUT.json').write_text(json.dumps(records,indent=2));(work/'PROVENANCE.json').write_text(json.dumps({'source_model_sha256':sha(model),'actual_report_opening_sha256':sha(report_path),'actual_source_components':custody,'scenes':[{'scene':i+1,'title':s[0],'duration':s[1],'caption':s[2]} for i,s in enumerate(SCENES)],'opening_assets':[{'name':n.name,'sha256':sha(n),'kind':'Generated fictional illustration, not actual footage, source evidence or a portrait of a recorded approver'} for n in ART.glob('*.png')],'authority':'Management payment question is hypothetical; product relates scope evidence and does not authorize payments. Original assertions, professional decisions and whole-version approval remain separate.','outputs':outputs,'audio_events':events,'licensed_music':{'asset':'Advertime by Rafael Krux, retained FreePD CC0 source','sha256':sha(music)},'human_continuous_watching_listening':'NOT VERIFIED','narration':'Caption-led; no spoken narration or synthetic voice claimed.'},indent=2)+'\n')
 print('BUILT full Film1 landscape and phone, 8 scenes /60 seconds, with audio and matching captions.',flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--model',required=True);p.add_argument('--report',required=True);p.add_argument('--proof',required=True);p.add_argument('--work',required=True);p.add_argument('--inspect-only',action='store_true');a=p.parse_args();build(a.model,a.report,a.proof,a.work,a.inspect_only)
