# Supplementary Table S9, Panel J — paired WoSCC AB vs ABC CiteSpace networks
# 补充表 S9 Panel J｜WoSCC 双模块和三模块 CiteSpace 关键词网络对照

**Added 7 November 2026.** This is an additive, public-facing evidence module for the supplement, not a change to the frozen 540-record corpus or original figures.

## Reproduce / 复核

Run from the extracted package root:

```powershell
python .\08_WoSCC_AB_ABC_CiteSpace\verify_s9j_networks.py
```

Or run `00_RUN_PUBLIC_SELFTEST_PLUS_S9J.ps1` to run all existing public tests plus this new one. **Only Python standard library is required.** The verifier is read-only. It independently recalculates keyword-node overlap, shared-node edge overlap, Jaccard, ARI and NMI from released keyword-only evidence; it does not regenerate the CiteSpace projects or their native GUI Q/S.

## Origin / 来源

- Authors' supplied `AB.zip` and `ABC.zip` were inspected as sources but are **not** shipped here because they contain full WoSCC bibliographic records and identifying local computer paths.
- `AB_keyword_only.graphml` and `ABC_keyword_only.graphml` are privacy-minimized exports containing the original keyword labels, frequencies, GraphML edges, edge weights and years; bibliographic metadata fields are excluded. No alias remapping and no new clustering are applied.
- `AB_native_cluster_labels.csv` and `ABC_native_cluster_labels.csv` retain only the original CiteSpace keyword label, frequency and native ClusterID from `network_summary_table.csv`.
- `AB_GUI_metrics_path_redacted.png` and `ABC_GUI_metrics_path_redacted.png` retain original CiteSpace network figures and metric captions; the personal input-directory string in the top-left text is replaced with a redaction. No plots were re-run.
- `S9J_GUI_READOUTS.csv/.json` transcribe native GUI network metrics. These are not derived from the GraphML edges.
- `S9J_DERIVED_EXPECTED.json` is the numeric test target for the verifier.

## Analytical period and parameters / 时间与参数

The author confirms that both final CiteSpace analyses used **2015–2025** (one-year slices), and both exported images report this range. The original input exports have 526 AB records (7 dated 2026) and 321 ABC records (3 dated 2026); the 2015–2025 eligible subsets are 519 AB and 318 ABC. The analysis applies keyword nodes, CiteSpace 6.4.R1 Advanced, g-index k=25, LRF=2.5, L/N=10, LBY=5, pruning None. **No synonymous or orthographic keyword merging or alias standardization** was performed in either comparison project. This AB/ABC pair must not be conflated with the separate full-540/focused-374 keyword analysis which uses its own alias procedure.

For provenance: legacy string fields in the project `.parameters`/`.signature` capture show 2016–2026, conflicting with the author-confirmed final 2015–2025 period, native screenshot, and numeric signature years. The authors attribute this string discrepancy to the software. Unedited raw configuration files containing those strings and local paths are excluded from the public release. This package **does not claim independently to diagnose the reason or to rerun the entire GUI analysis**.

## Core results / 核心结果

| Measure | AB | ABC |
|---|---:|---:|
| Native CiteSpace nodes (N) | 394 | 342 |
| Native GUI links (E) | 2,082 | 1,652 |
| Native Q | 0.3945 | 0.4193 |
| Native weighted silhouette (S) | 0.7084 | 0.7469 |
| Distinct GraphML edges | 2,040 | 1,620 |

Exact-label shared keyword nodes = **266**; node Jaccard = **0.5660**. Shared-node subgraph edges: AB **1,398**, ABC **1,292**, intersection **876**, edge Jaccard **0.4829**. Native ClusterID agreement on the 266 common keyword labels: ARI **0.1532**, NMI **0.3195**.

**Interpretation:** Broad themes remain visible under both retrieval definitions, while individual nodes and fine-scale cluster assignments are sensitive to corpus scope. The within-network modularity Q and silhouette S do not measure agreement between networks. The 42/32 difference between GUI E and GraphML edges reflects differences in exported representation; report GUI E for original CiteSpace network summary and GraphML edge counts for reproducible pairwise edge comparison.

**中文：** 使用匿名化GraphML和仅含Label/Freq/ClusterID的表，复算两组共享关键词、共现边Jaccard及ARI/NMI；保留原生截图的N/E/Q/S，不擅自以GraphML边数代替CiteSpace界面连线数。两组均为作者确认的2015–2025关键词网络、未做同义词或拼写合并。源ZIP不公开原始WoSCC全文书目。该核验不代表重跑CiteSpace GUI。
