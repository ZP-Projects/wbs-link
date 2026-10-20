"""Freeze matching production reports, movie posters/captions and source custody.
No service activation or runtime-data write. Existing four answer-led charts retained.
"""
from pathlib import Path
import json,hashlib,shutil,argparse,subprocess
p=argparse.ArgumentParser();p.add_argument('--product',required=True);p.add_argument('--work',required=True);a=p.parse_args();P=Path(a.product);R=Path(a.work);D=Path(__file__).resolve().parents[1]/'docs';edition='full-suite-production-2026-v5';sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
product_sha=subprocess.check_output(['git','-C',str(P),'rev-parse','HEAD'],text=True).strip()
for c in [1,2]:
 for n in ['Integrated_Management_Report.html','Integrated_Management_Report_Print.pdf','report-content.json','Premium_Workbook.xlsx']:
  shutil.copyfile(P/'wbslink/assets/approved_harbourlink/versions'/edition/f'cycle{c}'/n,D/f'examples/harbourlink/cycle{c}'/n)
images={'executive-briefing-cycle2.png':'page-01.png','executive-briefing-detail.png':'page-02.png','coverage-finding-15.png':'page-05.png','executive-decisions-cycle2.png':'page-05.png','movement-detail.png':'page-03.png'}
for n,q in images.items():shutil.copyfile(R/'rendered/reports/cycle2'/q,D/'assets/flagship'/n)
f=D/'assets/flagship/chart-data.json';j=json.loads(f.read_text());j.update(source_product_sha=product_sha,presentation_edition=edition);f.write_text(json.dumps(j,indent=2)+'\n')
p=D/'index.html';s=p.read_text().replace("The owner's common list of project work","The owner’s hierarchy of project work")
s=s.replace('src="videos/wbslink-video-1-challenge.mp4" aria-label','src="videos/wbslink-video-1-challenge.mp4" data-phone-src="videos/wbslink-video-1-challenge-phone.mp4" aria-label')
s=s.replace('From fragmented control views to an evidence-led management question: the gap, Owner WBS, professional decisions and separate approvals.','Month-end pressure. Different control views. A leadership question about the evidence behind payment review. See how Owner WBS helps relate the work—without authorizing payment.')
s=s.replace('Original custom graphics and actual HarbourLink report evidence. Licensed instrumental music; no spoken narration. Enable matching captions through CC.','Fictional cinematic illustrations, original motion graphics and actual HarbourLink report evidence. Licensed music and picture-matched Foley; no spoken narration or recorded site sound. Matching captions are available through CC.')
s=s.replace('Actual HarbourLink Cycle 2 report whole-population and separately labelled detail scale: 1,613 carried forward, 1 revalidated, 4 changed, 4 new and 3 retired','Complete actual HarbourLink Cycle 2 report comparison: 1,613 carried forward, 1 revalidated, 4 changed, 4 new and 3 retired')
p.write_text(s)
for n in ['wbslink-video-1-challenge','wbslink-video-2-how-it-works']:
 subprocess.run(['ffmpeg','-v','error','-y','-ss','2','-i',str(D/'videos'/f'{n}.mp4'),'-frames:v','1','-q:v','2',str(D/'videos'/f'{n}.jpg')],check=True)
source=D/'videos/source/full_suite_production_73';proof=source/'report-captures';proof.mkdir(exist_ok=True)
for q in (R/'proof').iterdir():
 if q.is_file():shutil.copyfile(q,proof/q.name)
for c in [1,2]:shutil.copyfile(R/f'film{c}/PROVENANCE.json',source/f'FILM_{c}_PROVENANCE.json')
art=[]
for n,role in [('01_controls_manager.png','Black male owner controls manager'),('02_contractor_lead.png','Black woman contractor commercial lead'),('03_ceo_question.png','Latina CEO')]:
 q=source/'art'/n;art.append({'file':'art/'+n,'sha256':sha(q),'bytes':q.stat().st_size,'casting_direction':role,'provenance':'Original generated fictional cinematic illustration, made for this production; not documentary client footage, a real person, testimonial or payment evidence. Casting intent does not establish actual heritage. No association with Maya Chen.'})
(source/'ART_PROVENANCE.json').write_text(json.dumps({'created_UTC':'2026-10-19','method':'OpenAI image generation, original custom commission, unchanged original PNG files retained','continuity':'One fictional warm contemporary infrastructure office / month-end context','third_party_stock':False,'assets':art},indent=2)+'\n')
prior=D/'videos/source/PO_CORRECTIONS_PROVENANCE.json';tracked=list(json.loads(prior.read_text())['files'])
files=set(tracked)|{'videos/'+n for n in ['wbslink-video-1-challenge-phone.mp4','wbslink-video-1-challenge-phone.vtt','wbslink-video-2-how-it-works-phone.mp4','wbslink-video-2-how-it-works-phone.vtt']}
for q in source.rglob('*'):
 if q.is_file() and q != source/'PROVENANCE.json' and '__pycache__' not in str(q):files.add(str(q.relative_to(D)))
provenance={'source_product_sha':product_sha,'presentation_edition':edition,'hosted_parity':'NOT VERIFIED; corrected source undeployed','film1':'Eight distinct scenes /60s WHY: fictional cinematic month-end context, original animated evidence exhibits, exact Action, graceful Film2 bridge. Payment authorization external.','film2':'Accepted80s HOW: matching current actual report components and approved shared-reference vector; retained original instrumental AAC packets. Not a performed application transaction. Actual practice workflow is separately executed and evidenced.','source_database_opened':False,'human_listening_native_Office_physical_phone':'NOT VERIFIED','files':{n:sha(D/n) for n in sorted(files)}}
prior.write_text(json.dumps(provenance,indent=2)+'\n')
(source/'PROVENANCE.json').write_text(json.dumps({'source_product_sha':product_sha,'edition':edition,'source_model_sha256':sha(P/'wbslink/assets/approved_harbourlink/versions'/edition/'cycle2/report-content.json'),'report_images':{n:sha(D/'assets/flagship'/n) for n in images},'all_actual_component_capture_receipts':json.loads((R/'proof/PROVENANCE.json').read_text()),'files':provenance['files'],'synthetic_only':True,'hosted_parity':'NOT VERIFIED'},indent=2)+'\n')
print('Synchronized production source: reports, authentic captures, both orientations and matching captions. No deployment.')
