#!/usr/bin/env python3
"""Validate focused-374 native CiteSpace GraphML and keyword-only tables. Python standard library only."""
from pathlib import Path
import csv,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parent
rows=list(csv.DictReader((root/'Focused374_Native_Node_Summary_Public.csv').open(encoding='utf-8-sig',newline='')))
base=list(csv.DictReader((root/'focused374_keyword_clusters.csv').open(encoding='utf-8-sig',newline='')))
assert len(rows)==len(base)==352
assert [(x['Label'],x['Freq'],x['ClusterID']) for x in rows]==[(x['Label'],x['Freq'],x['ClusterID']) for x in base]
path=root/'Focused374_352nodes_1612GraphMLedges_keyword_only.graphml'
ns={'g':'http://graphml.graphdrawing.org/xmlns'}
rt=ET.parse(path).getroot()
keys={el.attrib['id']:el.attrib.get('attr.name','') for el in rt.findall('g:key',ns)}
nodes=rt.findall('.//g:node',ns); edges=rt.findall('.//g:edge',ns)
assert len(nodes)==352 and len(edges)==1612
nodevals={}
for node in nodes:
 d={keys[e.attrib['key']]:e.text for e in node.findall('g:data',ns)}
 assert set(d)=={'label','freq'}
 label=d['label'];freq=int(d['freq'])
 assert label not in nodevals
 nodevals[label]=freq
assert nodevals=={x['Label']:int(x['Freq']) for x in rows}
allowed_edge={'weight','slice','year'}
for edge in edges:
 assert set(keys[e.attrib['key']] for e in edge.findall('g:data',ns))==allowed_edge
print('PASS focused374 native: 352 nodes, 1612 sanitized GraphML edges, 352 exact Label/Freq/ClusterID source-table rows.')
print('CiteSpace GUI E=1641, Q=0.4331, S=0.7563 are figure readouts and NOT recomputed by this validation.')
