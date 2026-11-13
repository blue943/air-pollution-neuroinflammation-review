#!/usr/bin/env python3
"""Standard-library, read-only verification of author-supplied CiteSpace AB/ABC keyword networks.
No bibliographic inputs, packages, internet or GUI needed. Does not re-run CiteSpace or recalc its Q/S.
Usage: python 08_WoSCC_AB_ABC_CiteSpace/verify_s9j_networks.py
"""
import csv,json,math,xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
root=Path(__file__).resolve().parent
N=lambda k:'{http://graphml.graphdrawing.org/xmlns}'+k

def read(code):
    rt=ET.parse(root/f'{code}_keyword_only.graphml').getroot()
    g=rt.find(N('graph'))
    assert g is not None
    nodes={};labels=[]
    for n in g.findall(N('node')):
        d={x.get('key'):(x.text or '') for x in n.findall(N('data'))}
        nodes[n.get('id')]=d['label']; labels.append(d['label'])
        assert set(d).issubset({'label','freq'})
    if len(set(labels))!=len(labels):raise ValueError('Duplicate keyword labels')
    edges=set()
    for e in g.findall(N('edge')):
        u,v=nodes[e.get('source')],nodes[e.get('target')]
        assert u!=v
        edges.add(frozenset([u,v]))
        d={x.get('key'):(x.text or '') for x in e.findall(N('data'))}
        assert set(d).issubset({'weight','year'})
    with (root/f'{code}_native_cluster_labels.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
    cl={r['Label']:r['ClusterID'] for r in rows}
    if len(cl)!=len(rows) or set(labels)!=set(cl):raise ValueError('Cluster label-to-graph mismatch')
    return set(labels),edges,cl

def choose2(v):return v*(v-1)/2

def partition_agreement(common,ca,cb):
    n=len(common)
    a=Counter(ca[x] for x in common);b=Counter(cb[x] for x in common)
    c=Counter((ca[x],cb[x]) for x in common)
    total=choose2(n)
    idx=sum(choose2(x) for x in c.values());sa=sum(choose2(x) for x in a.values());sb=sum(choose2(x) for x in b.values())
    exp=sa*sb/total
    denom=(sa+sb)/2-exp
    ari=(idx-exp)/denom if denom else 1.0
    mi=sum((v/n)*math.log(n*v/(a[i]*b[j])) for (i,j),v in c.items())
    ha=-sum((v/n)*math.log(v/n) for v in a.values())
    hb=-sum((v/n)*math.log(v/n) for v in b.values())
    nmi=mi/((ha+hb)/2) if ha+hb else 1.0
    return ari,nmi

def verify():
    aa,ae,ac=read('AB');ba,be,bc=read('ABC')
    common=sorted(aa&ba);u=set(common)
    ae2={x for x in ae if x.issubset(u)};be2={x for x in be if x.issubset(u)}
    ari,nmi=partition_agreement(common,ac,bc)
    metrics={
        'AB_nodes':len(aa),'ABC_nodes':len(ba),
        'AB_graphml_edges':len(ae),'ABC_graphml_edges':len(be),
        'shared_labels':len(u),'AB_only':len(aa-ba),'ABC_only':len(ba-aa),
        'node_jaccard':len(u)/len(aa|ba),
        'AB_edges_within_shared_nodes':len(ae2),'ABC_edges_within_shared_nodes':len(be2),
        'shared_edges':len(ae2&be2),'edge_jaccard':len(ae2&be2)/len(ae2|be2),
        'ari':ari,'nmi':nmi,
        'AB_cluster_ids':len(set(ac.values())),'ABC_cluster_ids':len(set(bc.values()))
    }
    want=json.loads((root/'S9J_DERIVED_EXPECTED.json').read_text(encoding='utf-8'))
    for k,w in want.items():
        got=metrics[k]
        if isinstance(w,float):
            if not math.isclose(got,w,abs_tol=1e-10,rel_tol=1e-9):raise SystemExit(f'FAIL {k}: got {got} expected {w}')
        elif got!=w:raise SystemExit(f'FAIL {k}: got {got} expected {w}')
    gui=json.loads((root/'S9J_GUI_READOUTS.json').read_text(encoding='utf-8'))
    for code in ('AB','ABC'):
        if gui[code]['N']!=metrics[code+'_nodes'] or gui[code]['GraphML_E']!=metrics[code+'_graphml_edges']:
            raise SystemExit('FAIL GUI/GraphML label count cross-check: '+code)
    print('PASS: S9 Panel J AB/ABC keyword-only networks and native ClusterID comparisons')
    print(json.dumps(metrics,ensure_ascii=False,indent=2))
    print('Scope: exact-label GraphML and native ClusterID; GUI N/E/Q/S readouts only, not reproduced.')
if __name__=='__main__':verify()
