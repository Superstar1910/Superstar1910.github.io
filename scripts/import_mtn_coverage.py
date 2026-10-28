#!/usr/bin/env python3
"""Import reviewed MTN generator output from a local checkout, then build_site.py.

No network fetch or automatic publication. Run build_reports.py in the source
checkout first. Canonical snapshots are versioned alongside the public site.
"""
import argparse,html,json,re,subprocess
from pathlib import Path
from urllib.parse import urljoin,urlsplit,urlunsplit
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('source',type=Path);args=p.parse_args()
source=args.source.resolve();folder=source/'canonical'
if not folder.is_dir():raise SystemExit('Run source scripts/build_reports.py before importing.')
redirects=json.loads((R/'static/data/url-redirects.json').read_text())
for name in ('index.html','valuation.html','ownership.html','substack.html'):
    old='/mtn-uganda-stock-coverage/'+name;target=redirects[old]
    text=(folder/name).read_text()
    def rewrite(m):
        raw=html.unescape(m[3]);u=urlsplit(urljoin('https://legesi.xyz'+old,raw))
        if u.netloc!='legesi.xyz' or not u.path.startswith('/mtn-uganda-stock-coverage/'):return m[0]
        path=redirects.get(u.path,u.path)
        return m[1]+'='+m[2]+html.escape(urlunsplit(('', '', path, u.query,u.fragment)),quote=True)+m[2]
    text=re.sub(r'\b(href|src)=("|\x27)(.*?)\2',rewrite,text)
    dest=R/target.strip('/')/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(text)
sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()
(R/'docs/MTN_SOURCE.json').write_text(json.dumps({'repository':'https://github.com/Superstar1910/mtn-uganda-stock-coverage','sourceCommit':sha,'generator':'scripts/build_reports.py','publicationRoot':'/work/mtn-uganda-stock-coverage/','note':'Versioned public research snapshot. Re-run importer and build_site.py after reviewing generator changes.'},indent=2)+'\n')
print('Imported four MTN coverage pages from source commit '+sha)
