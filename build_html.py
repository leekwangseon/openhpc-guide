"""Build the offline guide: python -m pip install -r requirements-build.txt; python build_html.py."""
from pathlib import Path
import html
import re
import markdown

root = Path(__file__).resolve().parent
pages = [('overview', '처음 사용하기', 'customer/home.md'),
         ('access', '접속하기', 'customer/access.md'),
         ('files', '파일 주고받기', 'customer/files.md'),
         ('run', '계산 실행', 'customer/run.md'),
         ('environment', '실행 환경', 'customer/environment.md'),
         ('basics', '서버와 저장 공간', 'customer/basics.md'),
         ('optional', 'GUI와 선택 기능', 'customer/optional.md'),
         ('help', '문제 해결·문의', 'customer/help.md')]
mapping = {name: '#' + key for key, _, name in pages}
mapping.update({Path(name).name:'#'+key for key,_,name in pages})
page_ids={key for key,_,_ in pages}
sections = []
for key, label, name in pages:
    body = markdown.markdown((root/name).read_text(encoding='utf-8'), extensions=['fenced_code','tables','toc'])
    body = re.sub(r'id="([^"]+)"',lambda m: 'id="'+key+'-'+m.group(1)+'"',body)
    body = re.sub(r'href="#([^"]+)"',lambda m: 'href="#'+(m.group(1) if m.group(1) in page_ids else key+'-'+m.group(1))+'"',body)
    for source, target in mapping.items():
        body = body.replace('href="'+source+'"', 'href="'+target+'" data-section="'+target[1:]+'"')
    body = body.replace('href="delivery-email.txt"', 'href="#email" data-section="email"')
    sections.append('<section id="'+key+'" class="page" aria-label="'+label+'">'+body+'</section>')
nav = ''.join('<a href="#'+key+'" data-section="'+key+'">'+label+'</a>' for key,label,_ in pages)
template = '''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>클러스터 사용 안내</title>
<style>
:root{--navy:#132b45;--ink:#192c3e;--blue:#096baf;--line:#dce3eb;--muted:#536678}
*{box-sizing:border-box}body{margin:0;color:var(--ink);background:#f4f7fb;font:16px/1.8 system-ui,-apple-system,"Malgun Gothic",sans-serif}
header{background:var(--navy);color:white;padding:27px 38px}header strong{display:block;font-size:25px;letter-spacing:-.6px}header p{margin:4px 0 0;color:#cbd9e9;font-size:14px}
.layout{display:grid;grid-template-columns:220px minmax(0,1fr);max-width:1360px;margin:auto}nav{padding:28px 18px;position:sticky;top:0;height:100vh;overflow:auto}nav a{display:block;padding:9px 14px;margin:4px 0;border-radius:7px;text-decoration:none;color:var(--ink)}nav a[aria-current="page"]{background:var(--navy);color:#fff}nav button{margin:20px 12px;padding:8px 12px;background:white;border:1px solid var(--line);border-radius:5px;cursor:pointer}
main{background:white;padding:30px 46px 70px;min-width:0}.cards{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:20px 0 28px}.card{display:block;text-decoration:none;border:1px solid var(--line);border-radius:10px;padding:22px;color:var(--ink);background:#f8fafc}.card:hover{border-color:var(--blue);background:#eef6fc}.card strong{display:block;font-size:19px;margin-bottom:8px}.card span{font-size:14px;color:var(--muted)}.page{margin-bottom:60px}body.js .page{display:none}body.js .page.active{display:block}h1{font-size:29px;line-height:1.4;margin:8px 0 24px}h2{font-size:22px;margin:34px 0 14px;padding-top:12px;border-top:1px solid var(--line)}h3{font-size:18px;margin-top:28px}p{margin:13px 0}a{color:var(--blue);text-underline-offset:3px}li{margin:6px 0}table{border-collapse:collapse;width:100%;font-size:14px;margin:20px 0;display:block;overflow-x:auto}th,td{border:1px solid var(--line);padding:10px 12px;vertical-align:top;text-align:left}th{background:#eef3f8}code{font:14px/1.6 Consolas,monospace;background:#eef3f8;border-radius:3px;padding:2px 4px}pre{background:#122537;color:#eff6ff;padding:18px 20px;border-radius:8px;overflow:auto;font:14px/1.7 Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere}pre code{background:none;padding:0;color:inherit}footer{margin-top:36px;font-size:13px;color:var(--muted);border-top:1px solid var(--line);padding-top:16px}
@media(max-width:800px){header{padding:22px}header strong{font-size:21px}.layout{display:block}.cards{grid-template-columns:1fr}nav{position:static;height:auto;padding:12px;display:flex;flex-wrap:wrap}nav a{padding:5px 10px;font-size:14px}nav button{margin:4px 10px}main{padding:22px}h1{font-size:25px}}
@media print{body{background:white;font-size:10pt;color:#111}header{background:white;color:#111;padding:0 0 16px}header p{color:#444}.layout{display:block}nav{display:none}main{padding:0}body.js .page{display:block!important;break-before:page}.page:first-child{break-before:auto}h1,h2,h3{break-after:avoid}pre{color:#111;background:#f3f3f3;border:1px solid #ccc;font-size:9pt}table{display:table;font-size:9pt}tr{break-inside:avoid}a{color:#111}footer{display:none}@page{size:A4;margin:18mm}}
</style></head><body>
<header><strong>클러스터 사용 안내</strong><p>접속부터 계산 결과 확인까지, 필요한 순서대로 시작하세요.</p></header>
<div class="layout"><nav aria-label="사용 안내">NAV<button onclick="window.print()" type="button">사용 안내 인쇄</button></nav><main>SECTIONS<footer>접속 정보와 장비별 사용 정책은 담당자에게 받은 안내를 확인해 주세요. · <a href="admin.html">관리자 운영 안내</a></footer></main></div>
<script>
document.body.classList.add('js');
function show(){let key=location.hash.slice(1)||'overview';if(!document.getElementById(key))key='overview';document.querySelectorAll('.page').forEach(e=>e.classList.toggle('active',e.id===key));document.querySelectorAll('nav a').forEach(e=>{if(e.dataset.section===key)e.setAttribute('aria-current','page');else e.removeAttribute('aria-current')});document.title=document.querySelector('#'+key+' h1').textContent+' | OpenHPC 가이드';window.scrollTo(0,0)}
window.addEventListener('hashchange',show);show();
</script></body></html>'''
output=template.replace('NAV',nav).replace('SECTIONS','\n'.join(sections))
(root/'OpenHPC-Guide.html').write_text(output,encoding='utf-8')
# GitHub Pages serves index.html; the same file also works offline without a server.
(root/'index.html').write_text((root/'OpenHPC-Guide.html').read_text(encoding='utf-8'),encoding='utf-8')
admin_body=markdown.markdown((root/'customer/admin.md').read_text(encoding='utf-8'),extensions=['fenced_code','tables'])
admin_body=admin_body.replace('href="../index.html"','href="index.html"')
admin_page=template.replace('NAV','<a href="index.html">사용자 안내로 돌아가기</a>').replace('SECTIONS','<section class="page active" id="overview">'+admin_body+'</section>')
admin_page=admin_page.replace('<strong>클러스터 사용 안내</strong>','<strong>관리자 운영 안내</strong>').replace('접속부터 계산 결과 확인까지, 필요한 순서대로 시작하세요.','계정·계산 노드·공유 저장소를 운영하는 담당자를 위한 안내입니다.')
(root/'admin.html').write_text(admin_page,encoding='utf-8')
print('Built customer guide and separate administrator guide')
