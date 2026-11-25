"""Build the offline guide: python -m pip install -r requirements-build.txt; python build_html.py."""
from pathlib import Path
import html
import re
import markdown

root = Path(__file__).resolve().parent
pages = [('overview', '시작하기', 'README.md'), ('common', '공통 안내', 'common.md'),
         ('user', '사용자 안내', 'user.md'), ('admin', '관리자 안내', 'admin.md'),
         ('site', '현장별 양식', 'site-template.md'), ('refs', '참고 자료', 'references.md')]
mapping = {name: '#' + key for key, _, name in pages}
sections = []
for key, label, name in pages:
    body = markdown.markdown((root/name).read_text(encoding='utf-8'), extensions=['fenced_code','tables','toc'])
    body = re.sub(r'id="([^"]+)"',lambda m: 'id="'+key+'-'+m.group(1)+'"',body)
    body = re.sub(r'href="#([^"]+)"',lambda m: 'href="#'+key+'-'+m.group(1)+'"',body)
    for source, target in mapping.items():
        body = body.replace('href="'+source+'"', 'href="'+target+'" data-section="'+target[1:]+'"')
    body = body.replace('href="delivery-email.txt"', 'href="#email" data-section="email"')
    sections.append('<section id="'+key+'" class="page" aria-label="'+label+'">'+body+'</section>')
sections.append('<section id="email" class="page" aria-label="완료 메일"><h1>완료보고 메일 양식</h1><pre>'+html.escape((root/'delivery-email.txt').read_text(encoding='utf-8'))+'</pre></section>')
nav = ''.join('<a href="#'+key+'" data-section="'+key+'">'+label+'</a>' for key,label,_ in pages)
nav += '<a href="#email" data-section="email">완료 메일</a>'
template = '''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>OpenHPC 클러스터 사용·운영 가이드</title>
<style>
:root{--navy:#132b45;--ink:#192c3e;--blue:#096baf;--line:#dce3eb;--muted:#536678}
*{box-sizing:border-box}body{margin:0;color:var(--ink);background:#f4f7fb;font:16px/1.8 system-ui,-apple-system,"Malgun Gothic",sans-serif}
header{background:var(--navy);color:white;padding:27px 38px}header strong{display:block;font-size:25px;letter-spacing:-.6px}header p{margin:4px 0 0;color:#cbd9e9;font-size:14px}
.layout{display:grid;grid-template-columns:220px minmax(0,1fr);max-width:1360px;margin:auto}nav{padding:28px 18px;position:sticky;top:0;height:100vh;overflow:auto}nav a{display:block;padding:9px 14px;margin:4px 0;border-radius:7px;text-decoration:none;color:var(--ink)}nav a[aria-current="page"]{background:var(--navy);color:#fff}nav button{margin:20px 12px;padding:8px 12px;background:white;border:1px solid var(--line);border-radius:5px;cursor:pointer}
main{background:white;padding:30px 46px 70px;min-width:0}.page{margin-bottom:60px}body.js .page{display:none}body.js .page.active{display:block}h1{font-size:29px;line-height:1.4;margin:8px 0 24px}h2{font-size:22px;margin:34px 0 14px;padding-top:12px;border-top:1px solid var(--line)}h3{font-size:18px;margin-top:28px}p{margin:13px 0}a{color:var(--blue);text-underline-offset:3px}li{margin:6px 0}table{border-collapse:collapse;width:100%;font-size:14px;margin:20px 0;display:block;overflow-x:auto}th,td{border:1px solid var(--line);padding:10px 12px;vertical-align:top;text-align:left}th{background:#eef3f8}code{font:14px/1.6 Consolas,monospace;background:#eef3f8;border-radius:3px;padding:2px 4px}pre{background:#122537;color:#eff6ff;padding:18px 20px;border-radius:8px;overflow:auto;font:14px/1.7 Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere}pre code{background:none;padding:0;color:inherit}footer{margin-top:36px;font-size:13px;color:var(--muted);border-top:1px solid var(--line);padding-top:16px}
@media(max-width:800px){header{padding:22px}header strong{font-size:21px}.layout{display:block}nav{position:static;height:auto;padding:12px;display:flex;flex-wrap:wrap}nav a{padding:5px 10px;font-size:14px}nav button{margin:4px 10px}main{padding:22px}h1{font-size:25px}}
@media print{body{background:white;font-size:10pt;color:#111}header{background:white;color:#111;padding:0 0 16px}header p{color:#444}.layout{display:block}nav{display:none}main{padding:0}body.js .page{display:block!important;break-before:page}.page:first-child{break-before:auto}h1,h2,h3{break-after:avoid}pre{color:#111;background:#f3f3f3;border:1px solid #ccc;font-size:9pt}table{display:table;font-size:9pt}tr{break-inside:avoid}a{color:#111}footer{display:none}@page{size:A4;margin:18mm}}
</style></head><body>
<header><strong>OpenHPC 클러스터 사용·운영 가이드</strong><p>사용자와 관리자를 위한 범용 안내 · v1.0 · 2026-11-25</p></header>
<div class="layout"><nav aria-label="문서 탐색">NAV<button onclick="window.print()" type="button">전체 안내 인쇄</button></nav><main>SECTIONS<footer>공개 범용 문서입니다. 실제 접속 정보와 운영 정책은 현장별 내부 안내서에서 확인하세요.</footer></main></div>
<script>
document.body.classList.add('js');
function show(){let key=location.hash.slice(1)||'overview';if(!document.getElementById(key))key='overview';document.querySelectorAll('.page').forEach(e=>e.classList.toggle('active',e.id===key));document.querySelectorAll('nav a').forEach(e=>{if(e.dataset.section===key)e.setAttribute('aria-current','page');else e.removeAttribute('aria-current')});document.title=document.querySelector('#'+key+' h1').textContent+' | OpenHPC 가이드';window.scrollTo(0,0)}
window.addEventListener('hashchange',show);show();
</script></body></html>'''
(root/'OpenHPC-Guide.html').write_text(template.replace('NAV',nav).replace('SECTIONS','\n'.join(sections)),encoding='utf-8')
# GitHub Pages serves index.html; the same file also works offline without a server.
(root/'index.html').write_text((root/'OpenHPC-Guide.html').read_text(encoding='utf-8'),encoding='utf-8')
print('Built offline guide and index.html')
