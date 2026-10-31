#!/usr/bin/env python3
"""Validate public Visual Library metadata and source files."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
catalog=json.loads((root/'static/data/visual-library.json').read_text())
assert catalog['schema_version']=='1.0.0'
ids=set();paths=set()
required={'id','title','file','alt','category','project','tags','version','approval_status','source_reference','rights_status'}
for asset in catalog['assets']:
    assert required<=asset.keys(),f"Missing fields: {asset.get('id')}"
    assert asset['approval_status'] in {'published-existing','approved'},asset['id']
    assert asset['id'] not in ids and asset['file'] not in paths,asset['id']
    assert asset['file'].startswith('/static/img/'),asset['file']
    assert asset['category'] in {'photography','research'},asset['id']
    assert isinstance(asset['tags'],list) and asset['tags'],asset['id']
    assert (root/asset['file'].lstrip('/')).is_file(),asset['file']
    if asset.get('thumbnail'):
        assert (root/asset['thumbnail'].lstrip('/')).is_file(),asset['thumbnail']
    ids.add(asset['id']);paths.add(asset['file'])
print(f"Visual catalogue: {len(ids)} unique approved assets, all paths valid.")
