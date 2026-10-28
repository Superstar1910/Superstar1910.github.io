#!/usr/bin/env python3
"""Bounded read-only availability checks. Never treats environment failures as proof of compromise."""
import argparse,urllib.request,urllib.error,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];parser=argparse.ArgumentParser();parser.add_argument('--base',default='https://legesi.xyz');args=parser.parse_args()
routes=['/','/work/','/writing/','/financial-literacy/','/sitemap.xml','/robots.txt','/work/africa-enduring-enterprises/','/work/africa-investability-index/','/work/mtn-uganda-stock-coverage/']
errors=[]
for route in routes:
 try:
  r=urllib.request.urlopen(args.base+route,timeout=20)
  if r.status!=200:errors.append(f'{route}: HTTP {r.status}')
 except Exception as e:errors.append(f'{route}: {e}')
for e in errors:print(e)
print(f'Checked {len(routes)} live routes; {len(errors)} failures.')
if errors:raise SystemExit(1)
