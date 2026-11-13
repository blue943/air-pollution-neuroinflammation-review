#!/usr/bin/env python3
"""S9 Panel K independent public-only check (no licensed source exports required)."""
from pathlib import Path
from collections import Counter
import csv,json,math
p=Path(__file__).resolve().parent

def read(name):
    with (p/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
annual=read('S9K_annual_counts_2015_2025.csv')
ranks=read('S9K_citation_ranked_top20_identity_hashes.csv')
summary=read('S9K_comparison_summary.csv')
expected=json.loads((p/'S9K_expected_summary.json').read_text(encoding='utf-8'))
assert len(annual)==11 and [int(x['year']) for x in annual]==list(range(2015,2026))
assert len(ranks)==80

def corr(a,b):
    ma=sum(a)/len(a);mb=sum(b)/len(b)
    return sum((x-ma)*(y-mb) for x,y in zip(a,b))/math.sqrt(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))
for db in ('WoSCC','Scopus'):
    ab=[int(x[db+'_AB']) for x in annual]
    abc=[int(x[db+'_ABC']) for x in annual]
    assert sum(ab)==expected[db]['AB_records']
    assert sum(abc)==expected[db]['ABC_records']
    assert round(corr(ab,abc),6)==expected[db]['Pearson_annual_r']
    rr={}
    for strat in ('AB','ABC'):
        a=sorted((x for x in ranks if x['database']==db and x['strategy']==strat),key=lambda x:int(x['rank']))
        assert len(a)==20 and [int(x['rank']) for x in a]==list(range(1,21))
        assert [int(x['citation_count']) for x in a]==sorted([int(x['citation_count']) for x in a],reverse=True)
        rr[strat]=a
    for k in (10,20):
        a={x['record_sha256_prefix'] for x in rr['AB'][:k]}
        b={x['record_sha256_prefix'] for x in rr['ABC'][:k]}
        assert len(a&b)==expected[db][f'Top{k}_overlap']
    stat=next(x for x in summary if x['database']==db)
    assert int(stat['AB_n'])==sum(ab) and int(stat['ABC_n'])==sum(abc)
    assert round(float(stat['pearson_annual_r']),6)==expected[db]['Pearson_annual_r']
    assert int(stat['top10_overlap'])==expected[db]['Top10_overlap']
    assert int(stat['top20_overlap'])==expected[db]['Top20_overlap']
print('PASS: Panel K annual series and Top10/Top20 ranked-identity overlap verified for WoSCC and Scopus (October snapshots).')
