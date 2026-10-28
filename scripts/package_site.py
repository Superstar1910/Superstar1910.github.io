#!/usr/bin/env python3
"""Publish only public assets/pages; exclude imports, source scripts and templates."""
import shutil,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];out=R/'_site'
if out.exists():shutil.rmtree(out)
out.mkdir()
dirs=['about','connect','disclaimer','financial-literacy','privacy','projects','research','sitemap','static','terms','work','writing']
for name in dirs:shutil.copytree(R/name,out/name)
for name in ['index.html','404.html','favicon.ico','about.html','projects.html','writing.html','archive.html','CNAME','.nojekyll','robots.txt','sitemap.xml']:
 shutil.copy2(R/name,out/name)
assert not (out/'imports').exists()
print('Packaged public-only static artifact in _site/')
