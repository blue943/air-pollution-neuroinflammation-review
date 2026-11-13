#!/usr/bin/env python3
"""Validate submitted record-identifier crosswalk: no full licensed records required."""
from pathlib import Path
from collections import Counter
import csv,json
root=Path(__file__).resolve().parent
with (root/'Audit_Attachment_A_217_Pairs.csv').open(encoding='utf-8-sig',newline='') as f:pairs=list(csv.DictReader(f))
with (root/'Audit_Attachment_A_8_Removals.csv').open(encoding='utf-8-sig',newline='') as f:removed=list(csv.DictReader(f))
with (root/'Audit_A_Validation_Summary.json').open(encoding='utf-8') as f:ref=json.load(f)
assert len(pairs)==ref['first_pass_pairs']==217
assert len(set(x['WoS_UT'] for x in pairs))==217
assert len(set(x['Scopus_EID'] for x in pairs))==217
assert sum(x['DOI_Exact']=='YES' for x in pairs)==215
assert sum(x['DOI_Exact']=='NO' for x in pairs)==2
assert sum(x['Year_Match']=='NO' for x in pairs)==1
assert sum(x['WoS_Record_Present_in_Frozen540']=='YES' for x in pairs)==216
assert sum(x['WoS_Record_Present_in_Frozen540']=='NO (QC exclusion)' for x in pairs)==1
assert all(x['Present_in_548']=='YES' and x['Scopus_Duplicate_Absent_from_548']=='YES' for x in pairs)
assert len(removed)==8 and len(set(x['Removed_UT'] for x in removed))==8
assert Counter(x['Stage'] for x in removed)=={'548_to_541':7,'541_to_540':1}
assert dict(Counter(x['Reason'] for x in removed))==ref['removal_reason_counts']
print('PASS Audit A: 217 unique pairs (215 DOI-exact, 2 DOI variants; 1 year mismatch); 7+1 removals; 216 final WoS counterparts')
