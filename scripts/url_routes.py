"""Compatibility redirects for a static GitHub Pages deployment.

GitHub Pages does not offer custom HTTP 301/308 rules. These documents supply a
canonical link, no-JS refresh/fallback and same-origin JS preserving URL state.
"""
import html,json
from pathlib import Path

def redirects(root):
    return json.loads((root/'static/data/url-redirects.json').read_text())

def file_for(root,url):
    return root/url.lstrip('/')/ 'index.html' if url.endswith('/') else root/url.lstrip('/')

def alias_files(root):
    return {file_for(root,u).relative_to(root).as_posix() for u in redirects(root)}

def redirect_document(target):
    safe=html.escape(target,quote=True)
    canonical=html.escape('https://legesi.xyz'+target,quote=True)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page moved — Legesi.xyz</title><link rel="canonical" href="{canonical}"><meta http-equiv="refresh" content="0;url={safe}"></head><body><p>This page has moved. <a id="redirect-target" href="{safe}">Continue to Legesi.xyz →</a></p><script src="/static/js/url-redirect.js"></script></body></html>'''

def write_redirects(root):
    for source,target in redirects(root).items():
        if source==target:raise ValueError('Self redirect: '+source)
        path=file_for(root,source);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(redirect_document(target))
