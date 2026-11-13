#!/usr/bin/env python3
"""Read-only WoSCC / Scopus paired AB/ABC yearly and citation comparison.
Python stdlib only; never edits licensed source data.
"""
import argparse,csv,hashlib,json,re,math
from collections import Counter
from pathlib import Path

YEARS=list(range(2015,2026))

def parse_wos(p):
    rows=[]; cur=None; active=None
    with open(p,encoding='utf-8-sig',errors='replace') as f:
        for line in f:
            line=line.rstrip('\r\n')
            if line.startswith('PT '):
                if cur is not None: rows.append(cur)
                cur={};active='PT';cur[active]=line[3:].strip();continue
            if line.strip()=='ER':
                if cur is not None:rows.append(cur)
                cur=None;active=None;continue
            if cur is None:continue
            m=re.match(r'^([A-Z][A-Z0-9]) (.*)$',line)
            if m:
                active=m.group(1);cur[active]=((cur.get(active,'')+' ') if active in cur else '')+m.group(2).strip()
            elif line.startswith('   ') and active:
                cur[active]=cur.get(active,'')+' '+line.strip()
    if cur is not None:rows.append(cur)
    result=[]
    for r in rows:
        try:year=int(r.get('PY','0'))
        except ValueError:year=0
        if year not in YEARS: continue
        token=(r.get('UT') or '').strip().lower()
        if not token: raise ValueError('Missing WoSCC UT in eligible publication')
        cited=r.get('TC','').replace(',','').strip()
        if not cited.isdigit():raise ValueError('Invalid WoSCC TC')
        result.append((year,token,int(cited)))
    return result,len(rows)

def parse_scopus(p):
    result=[];raw=0
    with open(p,encoding='utf-8-sig',newline='') as f:
        rd=csv.DictReader(f)
        for r in rd:
            if not any((v or '').strip() for v in r.values()):continue
            raw+=1
            year=int(r['Year'].strip())
            if year not in YEARS:continue
            token=(r.get('EID') or '').strip().lower()
            if not token:raise ValueError('Missing Scopus EID in eligible publication')
            cited=(r.get('Cited by') or '').replace(',','').strip()
            if not cited.isdigit():raise ValueError('Invalid Scopus Cited by')
            result.append((year,token,int(cited)))
    return result,raw

def pearson(a,b):
    mean_a=sum(a)/len(a);mean_b=sum(b)/len(b)
    aa=[v-mean_a for v in a];bb=[v-mean_b for v in b]
    return sum(u*v for u,v in zip(aa,bb))/math.sqrt(sum(v*v for v in aa)*sum(v*v for v in bb))

def hashid(db,token):
    return hashlib.sha256((db+'|'+token).encode('utf8')).hexdigest()[:24]

def ranks(db,rows,strategy):
    # Deterministic tie-breaking by normalized identifier; handles duplicated ranks consistently.
    return [dict(database=db,strategy=strategy,rank=i,record_sha256_prefix=hashid(db,t),citation_count=cited)
        for i,(year,t,cited) in enumerate(sorted(rows,key=lambda v:(-v[2],v[1]))[:20],1)]

def csvwrite(p,keys,data):
    with open(p,'w',newline='',encoding='utf-8-sig') as f:
        wr=csv.DictWriter(f,fieldnames=keys);wr.writeheader();wr.writerows(data)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--wos-ab',required=True);ap.add_argument('--wos-abc',required=True)
    ap.add_argument('--scopus-ab',required=True);ap.add_argument('--scopus-abc',required=True)
    ap.add_argument('--out',required=True)
    args=ap.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    sets={};counts={}
    for db,prefix,fn in [('WoSCC','wos',parse_wos),('Scopus','scopus',parse_scopus)]:
        for strat in ['AB','ABC']:
            rows,raw=fn(getattr(args,prefix+'_'+strat.lower()))
            names=[r[1] for r in rows]
            if len(names)!=len(set(names)):
                raise ValueError(f'Duplicate IDs {db} {strat}')
            sets[(db,strat)]=rows;counts[(db,strat)]=(raw,len(rows))
    annual=[];year_counts={}
    for db in ['WoSCC','Scopus']:
        for st in ['AB','ABC']:
            hist=Counter(y for y,_,_ in sets[(db,st)])
            year_counts[(db,st)]=[hist[y] for y in YEARS]
    for i,y in enumerate(YEARS):
        annual.append({'year':y,'WoSCC_AB':year_counts['WoSCC','AB'][i],'WoSCC_ABC':year_counts['WoSCC','ABC'][i],
                       'Scopus_AB':year_counts['Scopus','AB'][i],'Scopus_ABC':year_counts['Scopus','ABC'][i]})
    csvwrite(out/'S9K_annual_counts_2015_2025.csv',list(annual[0]),annual)
    top=[];summary={};overlaps=[]
    for db in ['WoSCC','Scopus']:
        ab=sets[(db,'AB')];abc=sets[(db,'ABC')]
        akeys=set(r[1] for r in ab);ckeys=set(r[1] for r in abc)
        if not ckeys <= akeys:raise ValueError(f'{db}: ABC not subset AB')
        for st in ['AB','ABC']:
            top.extend(ranks(db,sets[db,st],st))
        ra=ranks(db,ab,'AB');rc=ranks(db,abc,'ABC')
        overlap10=len(set(x['record_sha256_prefix'] for x in ra[:10])&set(x['record_sha256_prefix'] for x in rc[:10]))
        overlap20=len(set(x['record_sha256_prefix'] for x in ra[:20])&set(x['record_sha256_prefix'] for x in rc[:20]))
        r=pearson(year_counts[db,'AB'],year_counts[db,'ABC'])
        summary[db]={'AB_records':len(ab),'ABC_records':len(abc),'AB_original_records':counts[db,'AB'][0],
                     'ABC_original_records':counts[db,'ABC'][0], 'ABC_subset_AB':True,
                     'Pearson_annual_r':round(r,6),'Top10_overlap':overlap10,'Top20_overlap':overlap20}
        overlaps.append({'database':db,'AB_n':len(ab),'ABC_n':len(abc),
                          'pearson_annual_r':round(r,6),'top10_overlap':overlap10,'top20_overlap':overlap20})
    csvwrite(out/'S9K_citation_ranked_top20_identity_hashes.csv',list(top[0]),top)
    csvwrite(out/'S9K_comparison_summary.csv',list(overlaps[0]),overlaps)
    (out/'S9K_expected_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
