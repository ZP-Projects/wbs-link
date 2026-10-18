"""Synchronise the undeployed website proof with the sealed corrected customer edition.

Copies actual whole-page/range renders and exact binaries. No hosted activation.
"""
from pathlib import Path
import argparse,json,hashlib,shutil,re,subprocess
from openpyxl import load_workbook
ap=argparse.ArgumentParser();ap.add_argument('--product',required=True);ap.add_argument('--product-sha',required=True);ap.add_argument('--document-renders',required=True);ap.add_argument('--workbook-renders',required=True);ap.add_argument('--clean-proof',required=True);a=ap.parse_args();P=Path(a.product);R=Path(__file__).resolve().parents[1];D=R/'docs';E=Path(a.document_renders);W=Path(a.workbook_renders);C=Path(a.clean_proof)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert re.fullmatch('[0-9a-f]{40}',a.product_sha)
assert subprocess.check_output(['git','-C',str(P),'rev-parse','HEAD'],text=True).strip()==a.product_sha
edition=P/'wbslink/assets/approved_harbourlink/versions/client-quality-2026-v3'
for cy in [1,2]:
 for name in ['Integrated_Management_Report.html','Integrated_Management_Report_Print.pdf','Premium_Workbook.xlsx','report-content.json']:
  src=edition/f'cycle{cy}'/name;dst=D/'examples/harbourlink'/f'cycle{cy}'/name;shutil.copyfile(src,dst)
proof=D/'assets/flagship'
images={
 'executive-briefing-cycle2.png':E/'Reports/cycle2/Integrated_Management_Report_Print/page-01.png',
 'executive-briefing-detail.png':E/'Reports/cycle2/Integrated_Management_Report_Print/page-02.png',
 'coverage-finding-15.png':E/'Reports/cycle2/Integrated_Management_Report_Print/page-05.png',
 'movement-detail.png':E/'Reports/cycle2/Integrated_Management_Report_Print/page-04.png',
 'premium-executive-view.png':C/'executive.png',
 'premium-executive-detail.png':C/'executive.png'}
for i in range(1,5):images[f'chart{i}.png']=C/f'chart{i}.png'
for name,src in images.items():assert src.is_file(),src;shutil.copyfile(src,proof/name)
old=json.loads((D/'archive/client-quality-baseline/assets/flagship/chart-data.json').read_text());book=edition/'cycle2/Premium_Workbook.xlsx';wb=load_workbook(book);s=wb['03 EXECUTIVE VIEW'];charts=[]
def cells(ref):
 sheet,area=ref.rsplit('!',1);v=wb[sheet.strip("'")][area];return [v] if hasattr(v,'value') else [c for row in v for c in row]
for ch in s._charts:
 cat=ch.series[0].cat;ref=cat.strRef.f if cat.strRef else cat.numRef.f;names=[str(c.value) for c in cells(ref)]
 charts.append({'source_categories':names,'display_categories':[x.replace('Contractor Programme','Contractor Program') for x in names], 'values_by_series':[[c.value for c in cells(v.val.numRef.f)] for v in ch.series],'category_ref':ref,'series_refs':[v.val.numRef.f for v in ch.series],'management_question':''.join(r.t for p in ch.title.tx.rich.p for r in p.r)})
data=dict(old,source_product_sha=a.product_sha,presentation_edition='client-quality-2026-v3',workbook_sha256=digest(book),previous_customer_workbook_sha256=old['workbook_sha256'],charts=charts,rendering='LibreOffice actual final chart objects; not native Microsoft Excel',source_database_sha256='7f192c2226061efe7fe121a80f851668714f5daa13a1b9d41e66dafbdedfca73')
(proof/'chart-data.json').write_text(json.dumps(data,indent=2)+'\n')
subprocess.run(['python',str(R/'scripts/build_answer_led_charts_73.py'),'--model',str(edition/'cycle2/report-content.json'),'--site',str(D)],check=True)
# One authored label is corrected; governed outcome codes/numbers and original source names remain exact.
p=D/'index.html';p.write_text(p.read_text().replace('Left unresolved on purpose (UNSURE)','Unresolved (UNSURE)'))
subprocess.run(['ffmpeg','-v','error','-y','-ss','2','-i',str(D/'videos/wbslink-video-2-how-it-works.mp4'),'-frames:v','1','-q:v','2',str(D/'videos/wbslink-video-2-how-it-works.jpg')],check=True)
prior=json.loads((D/'archive/client-quality-baseline/videos/source/PO_CORRECTIONS_PROVENANCE.json').read_text());files=list(prior['files'])+['videos/wbslink-video-1-challenge.mp4','videos/wbslink-video-1-cinematic.vtt','videos/wbslink-video-2-how-it-works.mp4','videos/wbslink-video-2-harbourlink.vtt','videos/source/build_management_story_73.py','assets/fonts/DejaVuSans.ttf','assets/fonts/DejaVu-Licence.txt','downloads/harbourlink-practice-project.zip','downloads/HarbourLink_First_Time_Guide.html']
provenance={'controlling_addendum':'6237116309','source_product_sha':a.product_sha,'presentation_edition':'client-quality-2026-v3','hosted_parity':'NOT VERIFIED; candidate source is undeployed','baseline_provenance':'archive/client-quality-baseline/videos/source/PO_CORRECTIONS_PROVENANCE.json','film1':'Preserved byte for byte; SHA-256 52ebc12339d3a26b20a734835cc3a52f2042de71159f8f586b643ce3ceee6538','film2':'Full 80s landscape and 80s phone; caption-led purpose-designed evidence exhibits, retained instrumental audio; no new voice or fabricated application transaction','audio_and_media_licensing':'Original retained source and licensed-media attribution in videos/source/ATTRIBUTION.md; no new third-party dependency/media','human_native_accessibility':'NOT VERIFIED independently; software evidence is scoped separately','files':{n:digest(D/n) for n in sorted(set(files))}}
(D/'videos/source/PO_CORRECTIONS_PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n')
(D/'videos/source/CLIENT_QUALITY_73_PROVENANCE.json').write_text(json.dumps({'source_product_sha':a.product_sha,'source_model_sha256':digest(edition/'cycle2/report-content.json'),'source_workbook_sha256':digest(book),'renders':{n:{'source':('document-render/'+str(p.relative_to(E)) if p.is_relative_to(E) else 'clean-workbook-proof/'+p.name),'sha256':digest(p)} for n,p in images.items()},'Film1_unchanged':digest(D/'videos/wbslink-video-1-challenge.mp4'),'undeployed':True},indent=2)+'\n')
print('Synchronized exact corrected files, complete actual proof pages/eight chart evidence and media provenance. No deployment.')
