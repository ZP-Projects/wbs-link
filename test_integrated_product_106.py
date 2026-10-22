"""Isolated integrated candidate, preserving every frozen website assertion."""
from pathlib import Path
from hashlib import sha256
import json,re

ROOT=Path(__file__).parent/'docs/research/integrated-product-106'

def data():
 return json.loads(re.search(r'<script[^>]*id="workspace-data"[^>]*>(.*?)</script>',(ROOT/'00_START_HERE.html').read_text(),re.S)[1])

def test_same_product_source_and_all_generated_website_members():
 receipt=json.loads((ROOT/'BUILD.json').read_text());p=data()
 assert receipt['product_source_sha']==p['product_source_sha']=='9321a8485a554149e451b4bc7d4188aadae88d2c'
 for f in receipt['files']:assert (ROOT/f['path']).stat().st_size==f['bytes'] and sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256']
 assert p['mode']=='integrated' and len(p['cases'])==6

def test_actual_fictional_scope_values_are_not_concept_board_inventions():
 p=data();home=p['cases'][0]['snapshot'];north=p['cases'][1]['snapshot'];multi=p['cases'][2]['snapshot']
 assert len(home['nodes'])==5 and len(home['relationships'])==10
 assert next(r for r in home['relationships'] if r['source_record_id']=='H-C01')['raw']['Amount']=='42000'
 assert next(r for r in home['relationships'] if r['source_record_id']=='H-M02')['raw']['Amount']=='18000'
 assert {r['raw']['Finish'] for r in north['relationships'] if r['source_record_id']=='N-S01'}=={'2026-08-21','2026-09-04'}
 assert len(multi['relationships'])==1 and len(multi['relationships'][0]['targets'])==2
 assert all(c['snapshot']['authority']['version_status']=='UNAPPROVED' for c in p['cases'][:4])

def test_commercial_candidate_routes_to_actual_selected_context():
 s=(ROOT/'Website/index.html').read_text()
 for ref in ['../00_START_HERE.html','../00_START_HERE.html#HOME-12/H12.20/schedule','../00_START_HERE.html#HOME-12/H12.20/cost','../00_START_HERE.html#HOME-12/H12.20/package','../00_START_HERE.html#HARBOURLINK-C2/1.5/findings']:assert 'href="'+ref+'"' in s
 assert 'CAD 42,000' in s and 'separate CAD 18,000 conditional payment is not a budget variance' in s
 assert 'No live folder connected' in s and 'Missing cost is never zero' in s
