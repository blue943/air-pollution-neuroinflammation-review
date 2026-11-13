#!/usr/bin/env python3
"""Reproduce full540 vs focused374 counts, TC, annual correlation and citation-rank overlap.

Requires *separately licensed local* frozen540 WoS-style TXT and historical focused375 TXT.
The original 374 sensitivity was obtained by omitting one historically U-coded record;
its topic classification was author-approved separately (2026-11-02). This program
verifies numerical consequences of that change; it does not conduct topic appraisal.
No bibliographic records are shipped or written by this script.
"""
from pathlib import Path
import argparse, hashlib, re, csv, json, math
from collections import Counter
SHA_540='5f9dfa5fbba89b6e0bb76cae113eda0f4423ce5b378a8d24b2cb1888dfc86f30'
SHA_375='cf0104aab67de283c4ef8a65937e0c42d778b8118a83146fe681e5ac9dff82c0'
OMITTED='WOS:000384866700009'
YEARS=tuple(range(2015,2026))
def read(path,sha_expected):
 b=Path(path).read_bytes();sha=hashlib.sha256(b).hexdigest()
 if sha!=sha_expected:raise ValueError('Input SHA256 mismatch for '+str(path))
 t=b.decode('utf-8-sig'); records={}; current={}; tag=None
 for line in t.splitlines():
  if line.strip()=='ER':
   if current:
    rec={k:' '.join(v).strip() for k,v in current.items()}
    ut=rec.get('UT')
    if not ut or ut in records:raise ValueError('Missing or duplicated UT')
    try: records[ut]=(int(rec['PY']),int(rec['TC']))
    except (KeyError,ValueError):raise ValueError('Missing/invalid PY or TC: '+ut)
   current={};tag=None
  elif re.match(r'^[A-Z0-9]{2} ',line):
   tag=line[:2];current.setdefault(tag,[]).append(line[3:])
  elif line.startswith('   ') and tag:current[tag].append(line.strip())
 return records
def pearson(a,b):
 ma=sum(a)/len(a);mb=sum(b)/len(b)
 return sum((x-ma)*(y-mb) for x,y in zip(a,b))/math.sqrt(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--full540',required=True,type=Path)
 p.add_argument('--historical375',required=True,type=Path)
 p.add_argument('--output',required=True,type=Path)
 a=p.parse_args()
 full=read(a.full540,SHA_540);old=read(a.historical375,SHA_375)
 if len(full)!=540 or len(old)!=375 or not set(old)<=set(full):raise ValueError('Source membership/count mismatch')
 if any(full[u]!=v for u,v in old.items()):raise ValueError('Source PY/TC differs')
 if OMITTED not in old or old[OMITTED]!=(2016,303):raise ValueError('Omitted record identity mismatch')
 foc={u:v for u,v in old.items() if u!=OMITTED}
 assert len(foc)==374 and sum(v[1] for v in full.values())==22378 and sum(v[1] for v in foc.values())==13249
 counts=lambda d:[sum(y==year for y,tc in d.values()) for year in YEARS]
 ann540=counts(full);ann374=counts(foc)
 rank=lambda d:sorted(d,key=lambda u:(-d[u][1],u))
 rf=rank(full);rs=rank(foc)
 summary={'full_n':540,'focused_n':374,'omitted_n':166,'full_TC':22378,'focused_TC':13249,
  'Pearson_r':pearson(ann540,ann374),'full_focused_top10_overlap':len(set(rf[:10])&set(rs[:10])),
  'full_focused_top20_overlap':len(set(rf[:20])&set(rs[:20])),
  'method':'Historical 375 member removed after separate author-approved U-to-C decision; approved category register not redistributed',
  'program_does_not':'Independently adjudicate all 540 record-level categories'}
 assert summary['full_focused_top10_overlap']==3 and summary['full_focused_top20_overlap']==11
 if a.output.exists():raise FileExistsError('Refuse to overwrite '+str(a.output))
 a.output.mkdir(parents=True)
 with (a.output/'annual_540_vs_374_aggregate.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.writer(f);w.writerow(['Year','Full540_count','Focused374_count']);w.writerows(zip(YEARS,ann540,ann374))
 (a.output/'summary_540_vs_374_aggregate.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print('PASS full540=540, focused=374, TC=13249, annual r=',round(summary['Pearson_r'],6),'Top10=',summary['full_focused_top10_overlap'],'Top20=',summary['full_focused_top20_overlap'])
if __name__=='__main__':main()
