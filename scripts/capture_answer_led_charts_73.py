"""Actual HTTP/DOM captures; original-resolution evidence, not native Office proof."""
import argparse
import hashlib
import json
import math
from PIL import Image
from pathlib import Path
from playwright.sync_api import sync_playwright


CONTRAST_JS = r"""root=>{
 const rgba=c=>{const m=c.match(/[\d.]+/g).map(Number);return [m[0],m[1],m[2],m.length>3?m[3]:1]};
 const blend=(top,base)=>top.slice(0,3).map((v,i)=>v*top[3]+base[i]*(1-top[3]));
 const lum=c=>c.map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4}).reduce((a,v,i)=>a+v*[.2126,.7152,.0722][i],0);
 const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);let n,results=[];
 while(n=walker.nextNode()){
  if(!n.textContent.trim())continue;const e=n.parentElement,s=getComputedStyle(e);
  if(!e.getClientRects().length||s.visibility==='hidden')continue;
  let chain=[],ancestor=e;while(ancestor){chain.unshift(ancestor);ancestor=ancestor.parentElement}
  let bg=[255,255,255];for(const item of chain)bg=blend(rgba(getComputedStyle(item).backgroundColor),bg);
  const fg=blend(rgba(s.color),bg),a=lum(fg),b=lum(bg),ratio=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);
  const px=parseFloat(s.fontSize),bold=parseInt(s.fontWeight)>=700,required=px>=24||(bold&&px>=18.666)?3:4.5;
  results.push({text:n.textContent.trim().slice(0,90),ratio:Math.round(ratio*1000)/1000,required,font_px:px,color:s.color,background:bg});
 }
 return results;
}"""

def capture(url, output):
    output.mkdir(parents=True, exist_ok=True)
    receipt=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True)
        for width in (1440,390):
            page=browser.new_page(viewport={'width':width,'height':1000},device_scale_factor=1)
            response=page.goto(url,wait_until='networkidle')
            assert response and response.status==200
            assert page.locator('h1').inner_text()=='Different views.\nOne Owner WBS.'
            assert page.locator('.analytical-details').count()==1
            assert not page.locator('.analytical-details').evaluate('(e)=>e.open')
            primary=page.locator('[data-chart="1"]')
            assert primary.is_visible()
            page.locator('.analytical-details>summary').focus()
            page.keyboard.press('Enter')
            assert page.locator('.analytical-details').evaluate('(e)=>e.open')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),width
            # Capture the unchanged complete document from its actual top. Element
            # screenshots scroll sticky navigation across tall figures and obscure text.
            page.evaluate('scrollTo(0,0)')
            page.wait_for_timeout(200)
            full_name=f'website-full-{width}.png'
            page.screenshot(path=str(output/full_name),full_page=True)
            full_image=Image.open(output/full_name)
            for number in range(1,5):
                figure=page.locator(f'[data-chart="{number}"]')
                assert figure.is_visible()
                assert figure.locator('.chart-question').inner_text().endswith('?')
                link=figure.locator('.chart-next')
                # Exercise keyboard focus without changing the authored page.
                link.focus()
                page.keyboard.press('Shift+Tab')
                page.keyboard.press('Tab')
                assert link.evaluate('(e)=>e===document.activeElement')
                focus=link.evaluate('(e)=>{let s=getComputedStyle(e);return {style:s.outlineStyle,width:parseFloat(s.outlineWidth)}}')
                assert focus['style']!='none' and focus['width']>=2,focus
                contrast=figure.evaluate(CONTRAST_JS)
                assert contrast and all(r['ratio']+0.01>=r['required'] for r in contrast),[r for r in contrast if r['ratio']+0.01<r['required']]
                # Keyboard navigation may scroll; return to the original screenshot origin.
                page.evaluate('scrollTo(0,0)')
                destination=link.get_attribute('href')
                probe=page.request.get(url.rsplit('/',1)[0]+'/'+destination.split('#')[0])
                assert probe.status==200,(number,destination)
                assert f'id="{destination.split("#")[1]}"' in probe.text()
                name=f'website-figure-{number}-{width}.png'
                dims=figure.bounding_box()
                assert page.evaluate('scrollY')==0
                bounds=(math.floor(dims['x']),math.floor(dims['y']),math.ceil(dims['x']+dims['width']),math.ceil(dims['y']+dims['height']))
                full_image.crop(bounds).save(output/name)
                receipt.append({'file':name,'width':width,'http_status':response.status,'figure':number,'destination':destination,'sha256':hashlib.sha256((output/name).read_bytes()).hexdigest(),'actual_css_dimensions':dims,'capture_method':'unmodified full-page browser screenshot; original-resolution figure crop','whole_page_source':full_name,'crop_bounds':bounds,'text_contrast':contrast,'keyboard_focus':focus})
            page.close()
        browser.close()
    (output/'chart-browser-evidence.json').write_text(json.dumps(receipt,indent=2)+'\n')

if __name__=='__main__':
    cli=argparse.ArgumentParser();cli.add_argument('--url',required=True);cli.add_argument('--out',type=Path,required=True)
    args=cli.parse_args();capture(args.url,args.out)
