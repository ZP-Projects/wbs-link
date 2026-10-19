"""Synchronize only approved creative presentation; no runtime or hosted activation."""
from pathlib import Path
import json,hashlib,subprocess,shutil,argparse
p=argparse.ArgumentParser();p.add_argument('--product',required=True);p.add_argument('--proof',required=True);p.add_argument('--renders',required=True);p.add_argument('--work',required=True);a=p.parse_args();P=Path(a.product);D=Path(__file__).resolve().parents[1]/'docs';R=Path(a.renders);C=Path(a.proof);W=Path(a.work)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();product_sha=subprocess.check_output(['git','-C',str(P),'rev-parse','HEAD'],text=True).strip();edition='creative-uplift-2026-v4'
# Keep the exact accepted v3 artefacts for their unchanged historical goldens.
archive=D/'archive/creative-uplift-baseline'
files=['index.html','assets/flagship/chart-data.json','downloads/HarbourLink_First_Time_Guide.html','videos/wbslink-video-1-challenge.mp4','videos/wbslink-video-1-cinematic.vtt','videos/wbslink-video-2-how-it-works.mp4','videos/wbslink-video-2-how-it-works-phone.mp4','videos/wbslink-video-2-harbourlink.vtt','videos/wbslink-video-2-how-it-works-phone.vtt']
files += [f'examples/harbourlink/cycle{i}/{name}' for i in [1,2] for name in ['Premium_Workbook.xlsx','Integrated_Management_Report.html']]
for name in files:
 dest=archive/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(subprocess.check_output(['git','show','d3cf7690913cf7cda33ef029fa3be505cf080549:docs/'+name]))
for cy in [1,2]:
 for name in ['Integrated_Management_Report.html','Integrated_Management_Report_Print.pdf','Premium_Workbook.xlsx','report-content.json']:
  shutil.copyfile(P/'wbslink/assets/approved_harbourlink/versions'/edition/f'cycle{cy}'/name,D/f'examples/harbourlink/cycle{cy}'/name)
images={'executive-briefing-cycle2.png':'page-01.png','executive-briefing-detail.png':'page-02.png','coverage-finding-15.png':'page-04.png','executive-decisions-cycle2.png':'page-04.png','movement-detail.png':'page-03.png'}
for name,page in images.items():shutil.copyfile(R/'cycle2'/page,D/'assets/flagship'/name)
meta=D/'assets/flagship/chart-data.json';j=json.loads(meta.read_text());j.update(source_product_sha=product_sha,presentation_edition=edition);meta.write_text(json.dumps(j,indent=2)+'\n')
p=D/'index.html';s=p.read_text();changes={
 "The Owner Work Breakdown Structure (Owner WBS) is the owner's common list of project work. Compare schedule, cost and work packages against it. See what needs checking, then follow the evidence.":"Find the gaps between schedule, cost and package information. WBS↔LINK relates each view through the owner’s Work Breakdown Structure (Owner WBS), so your team can focus its review and follow the original evidence.",
 'HarbourLink is a fictional, approved example. Start with a finding, inspect its source assertion, interpretation and professional decision, then compare Cycle 2.':'See it in HarbourLink, a fictional approved example. Read one gap and its exact Action, inspect its source assertion, interpretation and professional decision, then review the separate approval and compare July’s changed position.',
 'HarbourLink Cycle 2. The approved relationships locate the gaps; a professional determines what they mean.':'HarbourLink July. Testing and Commissioning lacks cost relationships; Program Management lacks schedule relationships. The approved records locate the gaps. Your team determines what they mean.',
 'See how different reporting structures complicate a single view of project delivery.':'From fragmented control views to an evidence-led management question: the gap, Owner WBS, professional decisions and separate approvals.',
 'Licensed instrumental music with restrained, picture-matched workplace and equipment sounds. Designed sound, not audio captured on the shown site. Captions are optional through CC.':'Original custom graphics and actual HarbourLink report evidence. Licensed instrumental music; no spoken narration. Enable matching captions through CC.',
 'Follow the files through source review, professional decisions, approval, reporting and the next cycle.':'Inspect the real HarbourLink report: gap, original assertion, interpretation, bounded decision scope and separate approval. Then compare the next cycle.',
 'Licensed rhythmic instrumental music beneath the evidence walkthrough. Captions are off by default; use CC to enable them.':'Current approved report components, with explanatory diagrams clearly identified. Retained licensed instrumental music; use CC for the complete caption-led story.'}
for old,new in changes.items():assert old in s or new in s,old;s=s.replace(old,new)
p.write_text(s)
for i,name in [(1,'wbslink-video-1-challenge'),(2,'wbslink-video-2-how-it-works')]:
 subprocess.run(['ffmpeg','-v','error','-y','-ss','2','-i',str(D/'videos'/f'{name}.mp4'),'-frames:v','1','-q:v','2',str(D/'videos'/f'{name}.jpg')],check=True)
provenance={'source_product_sha':product_sha,'presentation_edition':edition,'hosted_parity':'NOT VERIFIED; candidate source undeployed','film1':'New 60s custom graphic explainer expressly authorised by latest Product Owner addendum; not footage-preserved','film2':'Targeted authentic report-component replacements in existing80s story; same instrumental AAC packets','authentic_report_capture':json.loads((C/'PROVENANCE.json').read_text()),'licensed_media':'Existing Advertime/FreePD CC0 instrumental; source credit and licence retained. No new voice or third-party asset.','source_database_opened':False,'human_listening_native_Office_physical_phone':'NOT VERIFIED','files':{}}
for name in ['PO_CORRECTIONS_PROVENANCE.json','CLIENT_QUALITY_73_PROVENANCE.json']:
 prior=D/'videos/source'/name
 if name.startswith('PO_'):tracked=list(json.loads(prior.read_text())['files'])
for name in tracked+['videos/source/build_creative_story_73.py','videos/source/build_creative_explainer_73.py','videos/wbslink-video-2-how-it-works-phone.mp4','videos/wbslink-video-2-how-it-works-phone.vtt']:
 provenance['files'][name]=sha(D/name)
(D/'videos/source/PO_CORRECTIONS_PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n')
(D/'videos/source/CREATIVE_UPLIFT_73_PROVENANCE.json').write_text(json.dumps({'source_product_sha':product_sha,'model_sha256':sha(P/'wbslink/assets/approved_harbourlink/versions'/edition/'cycle2/report-content.json'),'reports':{name:sha(D/'assets/flagship'/name) for name in images},'film1':json.loads((W/'film1/PROVENANCE.json').read_text()),'film2':json.loads((W/'film2/PROVENANCE.json').read_text()),'proof':provenance['authentic_report_capture'],'licence':'Existing CC0 Advertime source; no new assets','undeployed':True},indent=2)+'\n')
print('Synchronized v4 reports and media, retained exact v3 archival tests. No deployment.')
