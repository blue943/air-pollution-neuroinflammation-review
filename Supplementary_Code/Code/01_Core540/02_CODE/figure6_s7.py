# -*- coding: utf-8 -*-
"""Figure 6 / Supplementary S4 & S7, FINAL corrected term matching.
Scope: the existing 540-record WoS-style corpus. Never modifies its input or the figure.
Usage: python AirPollution_Figure6_S4_S7_540_recompute_FINAL.py --input PATH --outdir PATH
Note: Matching definitions are text occurrence indicators, not evidence of mechanism activity.
"""
import re, csv, argparse
from pathlib import Path

FIELDS = ('TI', 'AB', 'DE', 'ID')
PERIODS = ((2015,2017,76),(2018,2020,117),(2021,2023,185),(2024,2025,162))
PATTERNS = [
 ('Neuroinflammation', r'\bneuroinflammat\w*', 'Stem match'),
 ('Microglia', r'\bmicroglia\w*', 'Stem match'),
 ('Cytokines', r'\bcytokines?\b', 'Singular/plural'),
 ('IL-1β', r'\b(?:il|interleukin)[\s-]?1[\s-]?(?:β|beta)\b', 'Includes IL-1 beta/interleukin-1 beta; not bare IL1b'),
 ('IL-6', r'\b(?:il[\s-]?6|interleukin[\s-]?6)\b', 'Abbreviation/full name'),
 ('TNF-α', r'\b(?:tnf[\s-]?(?:α|alpha|a)|tumou?r necrosis factor[\s-]?(?:α|alpha|a))\b', 'Includes TNF-a and TNF-alpha'),
 ('TLR4', r'\b(?:tlr[\s-]?4|toll.like receptor[\s-]?4)\b', 'Abbreviation/full name'),
 ('NF-κB', r'\b(?:nf[\s-]?(?:κb|kb|kappa[\s-]?b)|nuclear factor[\s-]?kappa[\s-]?b)\b', 'Selected lexical variants'),
 ('NLRP3', r'\b(?:nlrp3(?:[\s-]+inflammasome)?|nalp3(?:[\s-]+inflammasome)?)\b', 'Any NLRP3 mention; does not require inflammasome'),
 ('Oxidative stress', r'\boxidative[\s-]+stress\b', 'Phrase match'),
 ('Mitochondrial dysfunction', r'\bmitochondrial[\s-]+dysfunction\b', 'Phrase match'),
 ('Blood–brain barrier', r'\b(?:blood[\s\-–—‑−]+brain[\s\-–—‑−]+barrier|bbb)\b', 'Includes unicode dash variants and BBB'),
 ('Autophagy', r'\bautophag\w*', 'Stem match'),
 ('Mitophagy', r'\bmitophag\w*', 'Stem match'),
 ('Ferroptosis', r'\bferroptos\w*', 'Stem match'),
 ('α-synuclein', r'\b(?:α[\s-]?synuclein|alpha[\s-]?synuclein)\b', 'Greek/Latin alphabet variant'),
 ('Dopaminergic neuron', r'\bdopaminergic[\s-]+neurons?\b', 'Singular/plural'),
]


def parse(path):
    src = Path(path).read_text(encoding='utf-8-sig')
    records = []
    for blk in re.split(r'(?m)^ER\s*$', src):
        if not re.search(r'(?m)^PT\s', blk):
            continue
        d = {}; k = None
        for line in blk.splitlines():
            if re.match(r'^[A-Z0-9]{2} ', line):
                k = line[:2]; d[k] = d.get(k, '') + ' ' + line[3:].strip()
            elif line.startswith('   ') and k:
                d[k] = d.get(k, '') + ' ' + line.strip()
        if d.get('PY','').strip().isdigit():
            records.append(d)
    if len(records) != 540:
        raise ValueError(f'Expected 540 records; read {len(records)}')
    actual = [sum(a <= int(r['PY']) <= b for r in records) for a,b,_ in PERIODS]
    assert actual == [n for _,_,n in PERIODS], f'Period denominators differ: {actual}'
    return records


def run(records):
    output=[]
    for term,pattern,rule in PATTERNS:
        rg=re.compile(pattern,re.I)
        cnt=[]
        for a,b,n in PERIODS:
            cnt.append(sum(a<=int(rec['PY'])<=b and bool(rg.search(' '.join(rec.get(k,'') for k in FIELDS))) for rec in records))
        output.append((term,pattern,rule,cnt))
    assert {term:cnt for term,_,_,cnt in output}['IL-1β'] == [7,12,23,12]
    assert {term:cnt for term,_,_,cnt in output}['TNF-α'] == [16,14,23,16]
    assert {term:cnt for term,_,_,cnt in output}['Blood–brain barrier'] == [20,28,41,49]
    return output


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True)
    ap.add_argument('--outdir',required=True)
    a=ap.parse_args()
    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    data=run(parse(a.input))
    p4=out/'AirPollution_S4_17_term_dictionary_FINAL_540.csv'
    with p4.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['Term','Regex (ignore case)','Matching rule','Fields'])
        w.writerows((term,patt,rule,'TI + AB + DE + ID') for term,patt,rule,_ in data)
    p7=out/'AirPollution_S7_540_可复现术语频率.csv'
    with p7.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f)
        w.writerow(['Term','Regex','2015-2017 count','2015-2017 per 100','2018-2020 count','2018-2020 per 100','2021-2023 count','2021-2023 per 100','2024-2025 count','2024-2025 per 100'])
        for term,patt,rule,cnt in data:
            fields=[v for n,(_,_,den) in zip(cnt,PERIODS) for v in (n,round(100*n/den,2))]
            w.writerow([term,patt,*fields])
    print('Source records 540; years [76,117,185,162]')
    for term,_,_,cnt in data: print(f'{term}: {cnt}')
    print('Saved:',p4,p7,sep='\n')
if __name__=='__main__':main()
