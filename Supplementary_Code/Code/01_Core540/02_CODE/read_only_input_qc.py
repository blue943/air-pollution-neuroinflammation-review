# -*- coding: utf-8 -*-
"""Read-only sanity check for user's *local* licensed 540-record WoS-style TXT.
No output file is written and no bibliometric analysis is performed.
"""
import argparse, collections, hashlib, re
from pathlib import Path

def parse_records(raw):
    current={};tag=None
    for line in raw.splitlines():
        if line.strip() == 'ER':
            if current:
                yield {k:' '.join(v).strip() for k,v in current.items()}
            current={};tag=None
        elif re.match(r'^[A-Z0-9]{2} ',line):
            tag=line[:2]
            current.setdefault(tag,[]).append(line[3:])
        elif line.startswith('   ') and tag:
            current[tag].append(line.strip())

def main():
    a=argparse.ArgumentParser();a.add_argument('--input',required=True);p=Path(a.parse_args().input)
    raw=p.read_bytes();text=raw.decode('utf-8-sig');rs=list(parse_records(text))
    ids=[r.get('UT','') for r in rs]
    yrs=[int(r.get('PY','0')) for r in rs]
    counts=[sum(lo<=y<=hi for y in yrs) for lo,hi in ((2015,2017),(2018,2020),(2021,2023),(2024,2025))]
    tc=sum(int((r.get('TC','0') or '0').replace(',','').strip() or 0) for r in rs)
    checks={'record_count':len(rs)==540,'unique_UT':len(ids)==len(set(ids)) and all(ids),
            'TC_sum':tc==22378,'year_periods':counts==[76,117,185,162]}
    print('SOURCE SHA256:',hashlib.sha256(raw).hexdigest())
    print('N:',len(rs),'unique_UT:',len(set(ids)),'TC:',tc,'period_counts:',counts)
    for k,v in checks.items():print(k,'PASS' if v else 'FAIL')
    if not all(checks.values()):raise SystemExit('STOP: file is not the frozen final 540 WoS-priority-TC input')
    print('READ-ONLY INPUT QC PASSED; no files created or modified.')
if __name__=='__main__':main()
