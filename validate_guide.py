"""Offline structural/privacy checks for the public guide (not a secret-scanner replacement)."""
from pathlib import Path
from html.parser import HTMLParser
import collections, ipaddress, re, subprocess

root=Path(__file__).resolve().parent
errors=[]
files=[p for p in root.iterdir() if p.is_file() and p.suffix in {'.md','.txt','.html','.py'}]
allowed={'127.0.0.1','192.0.2.21'}
for p in files:
    s=p.read_text(encoding='utf-8')
    for value in re.findall(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])',s):
        try: ipaddress.ip_address(value)
        except ValueError: continue
        if value not in allowed: errors.append(f'{p.name}: non-example IP address')
    # Known key/token formats; prose about secrets is allowed.
    if re.search(r'-----BEGIN (?:OPENSSH|RSA|EC|DSA|PRIVATE).*KEY-----',s):errors.append(f'{p.name}: private key marker')
    if re.search(r'\b(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[A-Z0-9]{16})\b',s):errors.append(f'{p.name}: token pattern')
    if re.search(r'[\u3040-\u30ff]',s):errors.append(f'{p.name}: unexpected Japanese text')
    if p.suffix=='.md':
        if len(re.findall(r'^```',s,re.M))%2:errors.append(f'{p.name}: unclosed code block')
        for link in re.findall(r'\]\(([^)]+)\)',s):
            if not link.startswith(('https://','http://','#')) and not (root/link.split('#')[0]).exists():errors.append(f'{p.name}: broken link {link}')

class Check(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.refs=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a' and a.get('href','').startswith('#'):self.refs.append(a['href'][1:])

c=Check();c.feed((root/'index.html').read_text(encoding='utf-8'))
for key,count in collections.Counter(c.ids).items():
    if count>1:errors.append('duplicate HTML id: '+key)
for ref in c.refs:
    if ref not in c.ids:errors.append('broken HTML anchor: '+ref)
if (root/'index.html').read_bytes()!=(root/'OpenHPC-Guide.html').read_bytes():errors.append('HTML outputs differ')
print('Checked',len(files),'public text/source files;',len(c.ids),'HTML IDs')
for e in errors:print('FAIL:',e)
if errors:raise SystemExit(1)
print('PASS: example IPs only; no key/token markers; Markdown links/fences and HTML anchors valid')
