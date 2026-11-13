#!/usr/bin/env python3
"""Reproducible within-WoSCC AB vs ABC keyword sensitivity analysis.

Uses fixed 2026-10-24 WoSCC Full Record downloads; standard library only.
No files in 01_INPUTS are edited; 540 corpus is neither opened nor changed.
"""
import argparse, collections, csv, hashlib, json, re, sys, unicodedata
from pathlib import Path

YEAR_MIN, YEAR_MAX = 2015, 2025
TOP_N=20
SEED='20261026_KeywordMini_V1'
C_PATTERNS=[r'\bnlrp3\b',r'\btlr4\b',r'\bnf\s*kappa\s*b\b',r'\bnf\s*kb\b',
            r'\bcytokines?\b',r'\binflammasomes?\b',r'\boxidative\s+stress\b',r'\bmitochondrial\s+dysfunction\b']

def records(path):
    text=path.read_text(encoding='utf-8-sig')
    curr={}; tag=None
    for line in text.splitlines():
        if line == 'ER':
            if curr: yield {k:' '.join(v).strip() for k,v in curr.items()}
            curr={}; tag=None;continue
        if re.match(r'^[A-Z0-9]{2} ',line):
            tag=line[:2];curr.setdefault(tag,[]).append(line[3:])
        elif line.startswith('   ') and tag:
            curr[tag].append(line.strip())

def load(path):
    found={}; total=0; outside=collections.Counter()
    for r in records(path):
        total+=1; yr=r.get('PY','').strip()
        if not yr.isdigit(): raise ValueError('Missing/noninteger PY for '+r.get('UT','unknown'))
        y=int(yr)
        if not YEAR_MIN<=y<=YEAR_MAX:
            outside[y]+=1;continue
        ut=r.get('UT','').strip()
        if not ut: raise ValueError('Missing UT')
        if ut in found:raise ValueError('Duplicate UT: '+ut)
        found[ut]=r
    return found,total,outside

def norm_term(s):
    s=unicodedata.normalize('NFKC',s).casefold().strip()
    s=s.replace('κ','kappa').replace('–','-').replace('—','-').replace('−','-')
    s=s.replace('&',' and ')
    s=re.sub(r'[-_/]+',' ',s)
    s=re.sub(r'[^\w\s]+',' ',s)
    s=re.sub(r'\s+',' ',s)
    return s.strip()

def is_C(term):
    return any(re.search(p,term) for p in C_PATTERNS)

def kws(r):
    return {norm_term(k) for k in r.get('DE','').split(';') if norm_term(k)}

def counts(recs,without_c=False):
    c=collections.Counter()
    for r in recs.values():
        for k in kws(r):
            if not without_c or not is_C(k):c[k]+=1
    return c

def ranks(c):
    return {k:i+1 for i,(k,_) in enumerate(sorted(c.items(),key=lambda x:(-x[1],x[0])))}

def write_csv(path,head,rows):
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(head);w.writerows(rows)

def top(c,n=TOP_N):return sorted(c.items(),key=lambda x:(-x[1],x[0]))[:n]

def overlap(c1,c2):
    t1={k for k,_ in top(c1)};t2={k for k,_ in top(c2)}
    return {'shared':len(t1&t2),'union':len(t1|t2),'jaccard':round(len(t1&t2)/len(t1|t2),4),'intersection':sorted(t1&t2),
            'ABC_only_top20':sorted(t1-t2),'AB_only_top20':sorted(t2-t1)}

def tie_inclusive_overlap(c1,c2):
    d1,d2=sorted(c1.values(),reverse=True),sorted(c2.values(),reverse=True)
    cut1=d1[TOP_N-1] if len(d1)>=TOP_N else (d1[-1] if d1 else 0)
    cut2=d2[TOP_N-1] if len(d2)>=TOP_N else (d2[-1] if d2 else 0)
    a={k for k,v in c1.items() if v>=cut1};b={k for k,v in c2.items() if v>=cut2}
    return {'ABC_cutoff':cut1,'AB_cutoff':cut2,'ABC_terms':len(a),'AB_terms':len(b),
            'shared':len(a&b),'union':len(a|b),'jaccard':round(len(a&b)/len(a|b),4)}

def rank_rows(ca,cb,co,na,nb,no,exclude):
    ra=ranks(ca);rb=ranks(cb)
    allterms=set(k for k,_ in top(ca))|set(k for k,_ in top(cb))
    # Include all focal C terms if present for an interpretable C-linked effects table
    allterms|={k for k in ca if is_C(k) and ca[k]>=4 and not exclude}
    rows=[]
    for k in sorted(allterms,key=lambda x:(ra.get(x,100000),rb.get(x,100000),x)):
        a,b,o=ca.get(k,0),cb.get(k,0),co.get(k,0)
        rows.append([k,int(is_C(k)),a,round(a/na*100,2),ra.get(k,''),b,round(b/nb*100,2),rb.get(k,''),o,round(o/no*100,2),round((a/na-b/nb)*100,2)])
    return rows

def sample(recs,n=30):
    # Stratification by publication period; deterministic SHA-256 seed-based ordering
    bins={'2015-17':[],'2018-20':[],'2021-23':[],'2024-25':[]}
    for ut,r in recs.items():
        y=int(r['PY']);period='2015-17' if y<=2017 else '2018-20' if y<=2020 else '2021-23' if y<=2023 else '2024-25'
        bins[period].append((ut,r))
    raw={k:len(v)*n/len(recs) for k,v in bins.items()}
    alloc={k:int(v) for k,v in raw.items()}
    left=n-sum(alloc.values())
    order=sorted(bins,key=lambda k:(-(raw[k]-alloc[k]),k))
    for k in order[:left]:alloc[k]+=1
    chosen=[]
    for b, vals in bins.items():
        ordered=sorted(vals,key=lambda p:hashlib.sha256((SEED+'|'+p[0]).encode()).hexdigest())
        chosen.extend([(b,ut,r) for ut,r in ordered[:alloc[b]]])
    return chosen,alloc,{k:len(v) for k,v in bins.items()}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--ab',required=True,type=Path)
    ap.add_argument('--abc',required=True,type=Path)
    ap.add_argument('--out',type=Path)
    ap.add_argument('--check-only',action='store_true')
    a=ap.parse_args()
    ab,abraw,about=load(a.ab);abc,abcraw,abcout=load(a.abc)
    only={k:v for k,v in ab.items() if k not in abc}
    if not set(abc).issubset(ab):
        raise ValueError('FAIL: ABC records are not all exact UT members of AB')
    if (len(ab),len(abc),len(only),abraw,abcraw)!=(519,318,201,526,321):
        raise ValueError(f'Unexpected counts (AB,ABC,AB-only,AB-export,ABC-export): {len(ab),len(abc),len(only),abraw,abcraw}')
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    print(f'PASS WoSCC within-date UT matching: AB={len(ab)}, ABC={len(abc)}, AB-only={len(only)}; out-of-year={dict(about)}')
    print('Input SHA256 AB:',sha(a.ab));print('Input SHA256 ABC:',sha(a.abc))
    print('DE availability:',sum('DE' in r for r in ab.values()),'/',len(ab),'AB;',sum('DE' in r for r in abc.values()),'/',len(abc),'ABC')
    if a.check_only:
        print('READ-ONLY QC COMPLETED. No files created.');return
    if a.out is None:raise ValueError('--out is required for analysis')
    if a.out.exists():raise FileExistsError('Refuse to overwrite existing output folder: '+str(a.out))
    a.out.mkdir(parents=True)
    N={'ABC':len(abc),'AB':len(ab),'AB-only':len(only)}
    raw={label:counts(rs,False) for label,rs in [('ABC',abc),('AB',ab),('AB-only',only)]}
    exc={label:counts(rs,True) for label,rs in [('ABC',abc),('AB',ab),('AB-only',only)]}
    summ={'scope':'WoSCC only, 2015-2025 publications, October 2026 paired search exports',
          'counts':N,'DE_present':{k:sum(bool(v.get('DE')) for v in rs.values()) for k,rs in [('ABC',abc),('AB',ab),('AB-only',only)]},
          'input_SHA256':{'AB':sha(a.ab),'ABC':sha(a.abc)},'top20_all':overlap(raw['ABC'],raw['AB']),
          'top20_excluding_C_term_matches':overlap(exc['ABC'],exc['AB']),
          'tie_inclusive_all':tie_inclusive_overlap(raw['ABC'],raw['AB']),
          'tie_inclusive_excluding_C':tie_inclusive_overlap(exc['ABC'],exc['AB']),
          'warnings':['Keyword outcomes are descriptive and search-conditioned, not independent causal proof.',
                       'AB-only necessarily lacks exact C-search matches in WoSCC topic search; do not interpret this as biological absence.',
                       'DE is author keywords only; ID/Keywords Plus not mixed with DE.',
                       'One database (WoSCC), not a combined WoSCC/Scopus comparison.',
                       'Keyword normalization limited to case, punctuation and spacing; not synonym collapsing.',
                       'No AB-only records are automatically adjudicated as eligible or ineligible.']}
    headers=['Keyword_DE_normalized','Matches_C_module','ABC_records','ABC_per100','ABC_rank','AB_records','AB_per100','AB_rank','AB_only_records','AB_only_per100','ABC_minus_AB_pp']
    for tag,d in [('ALL_DE',raw),('EXCL_C_DE',exc)]:
        write_csv(a.out/f'{tag}_Top20_union_comparison.csv',headers,
                  rank_rows(d['ABC'],d['AB'],d['AB-only'],N['ABC'],N['AB'],N['AB-only'],tag=='EXCL_C_DE'))
        for dataset in ('ABC','AB','AB-only'):
            write_csv(a.out/f'{tag}_{dataset}_Top20.csv', ['Rank','Keyword_DE_normalized','Count','Per100_records'],
                      [[i,k,c,round(c/N[dataset]*100,2)] for i,(k,c) in enumerate(top(d[dataset]),1)])
    sm,al,bs=sample(only)
    summ['sample']={'seed':SEED,'n':len(sm),'allocation':al,'period_sizes':bs}
    write_csv(a.out/'AB_ONLY_stratified30_FOR_AUTHOR_REVIEW.csv',
              ['SampleID','Period','UT','PY','TI','DI','DE','AB','Primary_air_pollution_exposure_A','CNS_neuroimmune_relation_B','Title_Retraction_Flag','Decision_Focused_Contextual_Offtopic_Uncertain','Evidence_detail_or_fulltext','Reviewer','Review_date'],
              [[f'W{i:02d}',period,ut,r.get('PY',''),r.get('TI',''),r.get('DI',''),r.get('DE',''),r.get('AB',''),'','','YES' if 'retract' in r.get('TI','').lower() else '','','','',''] for i,(period,ut,r) in enumerate(sm,1)])
    (a.out/'summary.json').write_text(json.dumps(summ,indent=2,ensure_ascii=False),encoding='utf-8')
    print('RESULT Top20 all DE: ',summ['top20_all']['shared'],'/20 shared; Jaccard',summ['top20_all']['jaccard'])
    print('RESULT Top20 excluding C-matched DE:',summ['top20_excluding_C_term_matches']['shared'],'/20 shared; Jaccard',summ['top20_excluding_C_term_matches']['jaccard'])
    print('RESULT stratified sample:',len(sm),al)
    print('Saved new outputs at',a.out)

if __name__=='__main__':
    try:main()
    except Exception as e:
        print('ERROR:',e,file=sys.stderr);sys.exit(2)
