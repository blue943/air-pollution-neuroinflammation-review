#!/usr/bin/env python3
"""Read-only validation of safely reduced keyword-only PubMed CiteSpace GraphML files.
Network metrics Q and S, and GUI link counts, are transcribed from final image, not recomputed.
"""
from pathlib import Path
import xml.etree.ElementTree as ET
base=Path(__file__).resolve().parent
ns='{http://graphml.graphdrawing.org/xmlns}'
def load(file):
    root=ET.parse(base/file).getroot()
    graph=root.find(ns+'graph')
    nodes=graph.findall(ns+'node')
    edges=graph.findall(ns+'edge')
    labels={}
    for node in nodes:
        row={d.get('key'):d.text or '' for d in node.findall(ns+'data')}
        labels[row['name']]=int(row['freq'])
    return nodes,edges,labels
old_n,old_e,old=load('PubMed_275_previous_sanitized.graphml')
new_n,new_e,new=load('PubMed_279_final_sanitized.graphml')
assert (len(old_n),len(old_e),len(new_n),len(new_e))==(275,538,279,546)
assert len(old.keys() & new.keys())==273
assert (len(old.keys()-new.keys()),len(new.keys()-old.keys()))==(2,6)
assert [old[x] for x in ['blood-brain barrier','blood–brain barrier','blood brain barrier']]==[9,5,3]
assert new['blood-brain barrier']==17
assert 'blood–brain barrier' not in new and 'blood brain barrier' not in new
print('PASS PubMed previous N275/GraphML E538; final N279/GraphML E546; 273 shared labels; BBB 9+5+3 -> 17.')
print('FINAL GUI reported separately: N279/E550/Q0.6225/S0.863; TimeSpan 2015–2025 (source image).')
