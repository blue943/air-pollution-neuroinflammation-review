# Focused374 native evidence — 2 November 2026 / 374篇原生分析文件

The author supplied the native 374-record CiteSpace figure, node-summary CSV, 352-node GraphML, 340-line alias table and program snapshots. They are from the **374-record WoSCC–Scopus sensitivity analysis**, **not** the 255-record PubMed project.

**Evidence cross-checks:** Figure S4 visibly states `TimeSpan: 2015–2025`, `N=352`, GUI `E=1641`, `Q=0.4331`, weighted mean `S=0.7563`, with `g-index k=25`. The new `.signature` contains numeric `begin_year=2015` and `end_year=2025`; the alias file is byte-identical to the previously archived focused-374 alias. The new node-summary CSV agrees with the existing 352-row public keyword table for every `Label`, `Freq` and `ClusterID` value. The uploaded GraphML has 352 nodes / 1612 undirected edges. These **GraphML edges are NOT GUI links**. `validate_focused374_graphml.py` verifies these identities without external dependencies.

**Public evidence:** `Focused374_352nodes_1612GraphMLedges_keyword_only.graphml` retains keyword labels, node frequencies, graph connections and edge attributes (`weight`, `slice`, `year`) but removes redundant bibliographic placeholder/node fields. `Focused374_Native_Node_Summary_Public.csv` contains keyword-only node statistics. `Focused374_Sanitized_Evidence_Index.json` records selected, traceable figure/metadata values. The path-hidden S4 PNG already supplied in this directory is retained unchanged. This archive does not distribute raw `.signature`, `.parameters`, `.config`, or original path-bearing Figure S4.

**Historical capture caveat:** The *newly provided* `.parameters` still displays `From 2016-JAN / To 2026-DEC`, while the same project `.signature` has both numeric 2015/2025 fields and stale `beginTime`/`endTime` strings. No original evidence has been edited. We retain **2015–2025 as the author-confirmed final figure period**, not a claim that all historical saved parameter strings agree. A full independent GUI rerun from the original licensed 374-record dataset remains outside this release's validated scope.

## 中文说明

用户新上传的文件已确认属于**374篇敏感性分析**，不是PubMed网络。最终聚类图标明2015—2025、N352、软件界面E1641、Q0.4331、S0.7563。新节点表与原有352条关键词表逐条一致，别名文件字节完全一致；新GraphML为352节点、1612边，注意与界面1641连线不是同一口径。

为投稿公开，保留**脱敏后的GraphML、关键词节点表、校验证据和已有S4脱敏图片**，不公开Windows本地路径、原始内部参数快照或授权书目语料。新的参数快照仍存2016–2026字符串；但最终图片和签名数值年份字段显示2015–2025。原始冲突证据未被修改，不虚构完整CiteSpace GUI已独立复跑。
