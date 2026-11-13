#!/usr/bin/env python3
"""Standard-library SHA256 manifest check, no network or private data required."""
from pathlib import Path
import csv,hashlib,sys
root=Path(__file__).resolve().parent
manifest=root/'MANIFEST_SHA256.csv'
with manifest.open(encoding='utf-8',newline='') as f:items=list(csv.DictReader(f))
listed=set()
for r in items:
 rel=r['path'];p=root/rel
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=r['sha256'] or p.stat().st_size!=int(r['bytes']):
  raise SystemExit('FAIL: missing/corrupt file: '+rel)
 listed.add(rel)
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST_SHA256.csv'}
if actual!=listed:raise SystemExit('FAIL: manifest file list mismatch '+repr(actual^listed))
print(f'PASS: {len(items)} files, SHA256 and size verified; no network or licensed input needed.')
