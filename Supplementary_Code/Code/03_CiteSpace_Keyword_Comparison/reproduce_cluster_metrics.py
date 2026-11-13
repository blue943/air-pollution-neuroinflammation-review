#!/usr/bin/env python3
"""Recompute overlap and cluster agreement from sanitized node tables (stdlib only).

Does NOT recompute CiteSpace GUI Q/S or regenerate networks from bibliographic records.
"""
import csv,math
from pathlib import Path
from collections import Counter
root=Path(__file__).resolve().parent
def read(name):
 with (root/name).open(encoding='utf-8-sig',newline='') as f:rs=list(csv.DictReader(f))
 d={r['Label']:(int(float(r['Freq'])),r['ClusterID']) for r in rs}
 if len(d)!=len(rs):raise ValueError('Duplicate keyword labels')
 return d
full=read('full540_keyword_clusters.csv');focused=read('focused374_keyword_clusters.csv')
common=sorted(set(full)&set(focused));n=len(common)
j=len(common)/len(set(full)|set(focused))
a=Counter(full[k][1] for k in common);b=Counter(focused[k][1] for k in common)
c=Counter((full[k][1],focused[k][1]) for k in common)
choose=lambda z:z*(z-1)/2
allpairs=choose(n);index=sum(choose(x) for x in c.values())
sa=sum(choose(x) for x in a.values());sb=sum(choose(x) for x in b.values())
expected=sa*sb/allpairs
ari=(index-expected)/((sa+sb)/2-expected)
mi=sum((v/n)*math.log((n*v)/(a[x]*b[y])) for (x,y),v in c.items())
ha=-sum((v/n)*math.log(v/n) for v in a.values())
hb=-sum((v/n)*math.log(v/n) for v in b.values())
nmi=mi/((ha+hb)/2)
# Preserve original node-summary file order for equal-frequency cutoff, matching source audit.
rank=lambda d:sorted(d,key=lambda k:-d[k][0])
f,g=rank(full),rank(focused)
fixed=len(set(f[:20])&set(g[:20]))
fa={k for k in full if full[k][0]>=full[f[19]][0]}
fb={k for k in focused if focused[k][0]>=focused[g[19]][0]}
assert (len(full),len(focused),n,fixed,len(fa),len(fb),len(fa&fb))==(378,352,301,19,20,21,20)
assert abs(j-0.7016317016317016)<1e-9 and abs(ari-0.3109539090211276)<1e-8 and abs(nmi-0.5222401333366182)<1e-8
print(f'PASS full N=378, focused N=352, shared={n}, Jaccard={j:.7f}, ARI={ari:.7f}, NMI={nmi:.7f}, fixed Top20 shared={fixed}/20, tie-inclusive={len(fa&fb)}/{len(fa)}')
print('Note: GUI E=1641, Q=0.4331, S=0.7563 are original CiteSpace readouts; no independent GUI recomputation here.')
