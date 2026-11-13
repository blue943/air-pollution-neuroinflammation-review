# Supplementary Code: Air Pollution–Associated Neuroinflammation (540 primary / 374 focused)

**Submission-oriented code-only companion; generated 2026-11-02.** This archive contains custom analysis scripts, selected derived outputs, record-identifier-only Audit Attachment A, figure-output evidence and a repeatable integrity test. The original internal archive is retained separately and unchanged. **Do not upload the internal archive.**

## Contents / 内容

| Folder | Purpose | Reproducibility scope |
|---|---|---|
| `01_Core540` | Source 540 input QC, Figure 6/S7 term frequencies, within-WoSCC AB/ABC keyword comparison; selected aggregate reference outputs | Re-run locally with licensed input data, Python standard library |
| `02_Focused374` | Verify the 540 vs 374 annual, TC and citation-rank comparison from exact frozen 540 and historical 375 locally licensed inputs | Standard library; numerical 375→374 check only |
| `03_CiteSpace_Keyword_Comparison` | Source keyword-label frequency/cluster tables (bibliographic fields stripped), Jaccard/ARI/NMI check, path-hidden Figure S4, newly supplied keyword-only 352-node GraphML (1,612 exported edges), native node-summary cross-check | Recomputes derived-table comparison and validates released GraphML vs 352 source rows; not CiteSpace GUI E/Q/S |
| `04_CiteSpace_PubMed` | Targeted 12-entry alias, high-level QC and software provenance | 2015–2025 final Figure 7 metadata and keyword-only earlier/final GraphML, with read-only validation; CiteSpace-only |
| `05_Burst_20_Term_Audit` | Aggregated Figure 5B 20-term source-field audit (Audit Attachment B) | Descriptive keyword fields, not CiteSpace burst reconstruction |
| `06_Record_QC_Summary` | **Audit Attachment A**: 217 record-identifier pairs, seven QC exclusions plus one residual duplicate, derived audit note and standalone crosswalk verifier | Verifiable file-level pair/removal summaries; does not replay the historic deduplication execution |
| `07_Figure4_Plotting_Reference` | Historical plotting reference, with `--top-n 25 --label-n 8` arguments | Not certified to regenerate the exact final Figure 4 |

## Minimal verification / 最小运行

On a Windows machine with Python 3 installed, open PowerShell in this folder and run the **one command**:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\00_RUN_PUBLIC_SELFTEST.ps1
```

It verifies the cryptographic package manifest, recomputes the keyword-cluster comparison metrics, and checks the 217-pair/8-removal Audit A crosswalk using only the Python standard library; no pip installation or licensed source records are required. Alternatively run `python verify_package.py`, then `python 03_CiteSpace_Keyword_Comparison/reproduce_cluster_metrics.py`.

To re-run all local input-dependent workflows, stage your **own legally obtained** files as specified in `01_Core540/01_INPUT_LOCAL/README.txt` and `02_Focused374/01_INPUT_LOCAL/README.txt`, then run the **single** `00_RUN_WITH_LICENSED_INPUTS.ps1` command. This writes only local outputs, never modifies the inputs, and refuses to overwrite existing output directories. Some outputs include bibliographic record-level content; do not submit those local outputs without authorization.

## Key numeric outputs

- Main bibliometric corpus 540, citation sum 22,378, publication years 2015–2025.
- Author-approved focused subset 374 (A175+B199), citation sum 13,249; Pearson r 0.9660, Top10 overlap 3/10, Top20 overlap 11/20.
- Focused CiteSpace GUI N352, E1641, Q0.4331, weighted S0.7563 (GUI readouts, not recomputed here); 301 common labels with full corpus; Jaccard 0.7016; ARI 0.3110; NMI 0.5222.
- PubMed CiteSpace (final 2015–2025) N279, GUI E550, Q0.6225, weighted S0.863; final sanitized GraphML N279/E546; separate from WoSCC–Scopus 540.

## Data sharing, code scope and restrictions

**Not included:** original WoSCC/Scopus/PubMed files, 540/375/374 record-level full-text exports, category evidence registers, personal Windows paths, most historical source-code scripts not validated as the final end-to-end workflow (except a labeled Figure 4 reference), full bibliographic records underlying the public identifier-level crosswalk A, and original unredacted screenshots or path-bearing configuration snapshots. The public ZIP now includes **privacy-minimized keyword-only PubMed GraphML** with no raw bibliographic records. These materials must not be inferred to be public from their presence in the authors' internal archive. Data use is governed by applicable provider licences.

**Known limitations:** This release does not independently reproduce every Figure 1–8 or all graphical CiteSpace outputs; GUI-specific network Q/S are transcribed from saved exports and the keyword comparison is reproducible from derived keyword tables. The focused-374 newly supplied native graph/node summary are also checked as keyword-only evidence, but not an independent CiteSpace GUI rerun. The historical Figure 4 script is a plotting reference only. The final S4 output and numeric `signature` year fields support 2015–2025; a historical `.parameters` capture and string fields in that same signature display stale 2016–2026 window values. They are not distributed as final-run parameters; exact full-GUI reproducibility is not claimed (see `03_CiteSpace_Keyword_Comparison/PROVENANCE_NOTE.md`). The newly submitted PubMed parameter snapshot also shows a non-final 2016–2026 range; both final PubMed Figure 7 images confirm 2015–2025, and the two projects are documented separately. The historical deduplication execution timestamps have not been independently re-established.

**Supporting materials:** The manuscript references Supplementary Table S9 and Figure S4. **Audit Attachment A is included** under `06_Record_QC_Summary` with UT/EID identifiers and match/removal flags only, following the author’s explicit permission to share; no original licensed full bibliographic records are included. Full 20-word burst audit B is here as aggregate counts. Inclusion of this ZIP in a submission must be confirmed on the platform; this file alone does not prove upload or reviewer access.

No open-source software licence is declared by this packaging step. If the authors intend public code reuse beyond the journal supplement, select an appropriate code licence separately.

---

## 中文说明

本包是**投稿用途的公开代码候选包**，已经剔除原始书目全文记录、记录级主题分类表、Windows私人路径及未验收的历史脚本。原内部母档没有更改。文件夹01可在合法取得的540篇数据和WoSCC检索导出上重跑部分数值分析；文件夹02使用作者本地保留的原540和旧375输入核对新374数据；文件夹03不需要书目记录即可重算301个共有标签的Jaccard、ARI和NMI。图S4的Q/S只来源于CiteSpace界面，尚未独立复算。

**必须如实披露：** 最终S4截图与`signature`数值年份字段均为2015–2025；历史参数快照及其字符串年份字段残留2016–2026，与最终图件不符，未用作正式运行参数，也不声称已独立端到端复跑全部图表。Audit Attachment A已按作者分享授权加入公开ZIP，仅含217组UT/EID及7+1条移除记录标识、核验标记，不含完整受许可限制的原始书目记录。作者已在2026-11-02确认374篇分类核准，但旧内部CSV中的PENDING为历史状态，不代表现时状态。

### Additional 2015–2025 source-window verification / 补充年份证据

The author confirms the final **374-focused CiteSpace** and **255-record PubMed CiteSpace** analyses are both for **2015–2025**. Their native **final screenshots** display that range. Historical `.parameters` snapshots containing 2016–2026 text are not substituted for or silently edited into final settings; the 374 and PubMed files originate from **different project directories**. `04_CiteSpace_PubMed/` now contains privacy-minimized source GraphML for the 275-node historical and 279-node final keyword graphs, the read-only verification script, and a separate provenance note. See `04_CiteSpace_PubMed/EVIDENCE_2015_2025_CN_EN.md` and `03_CiteSpace_Keyword_Comparison/PROVENANCE_NOTE.md`.

**中文：** 用户确认最终374篇与PubMed分析均采用2015—2025年；两套最终图件也均如此标注。不同项目的参数快照各存在2016—2026的旧字符串；不把这些快照误认为最终运行条件，也不修改历史文件。新增PubMed脱敏GraphML和只读复核脚本，用于核查275→279节点、538→546条GraphML边以及BBB术语合并；GUI报告E=550另外保留。

## Focused374 additional native evidence / 374原生新证据

The 2026-11-02 author-supplied keyword-only GraphML (N352, 1612 GraphML edges), exact source node summary (352 rows), and byte-identical alias are documented under `03_CiteSpace_Keyword_Comparison/FOCUSED374_NEW_NATIVE_EVIDENCE_CN_EN.md`; run `python 03_CiteSpace_Keyword_Comparison/validate_focused374_graphml.py`. Final S4 screenshot and author confirm **2015–2025**. Historical `.parameters` window fields are not a source for the final time span; no claim of independent complete GUI replay is made.
