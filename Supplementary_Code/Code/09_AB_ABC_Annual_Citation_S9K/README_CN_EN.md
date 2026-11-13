# Supplementary Table S9 Panel K — October AB/ABC annual and citation sensitivity

**Scope / 范围.** Paired October 2026 database snapshots only; publication years 2015–2025. Within WoSCC: AB n=519, ABC n=318 (source TXT had 526/321 including PY2026). Within Scopus: AB n=711, ABC n=420. These datasets do **not** replace the frozen June 2026 primary 540-record corpus. Scopus citations are **Scopus Cited by** and WoSCC citations are **WoSCC TC**, with no cross-database addition.

## Files

- `S9K_annual_counts_2015_2025.csv`: aggregated annual counts for the two queries in both databases.
- `S9K_comparison_summary.csv` and `S9K_expected_summary.json`: Pearson annual-output correlations and Top10/Top20 membership overlaps.
- `S9K_citation_ranked_top20_identity_hashes.csv`: compact ranked identity hashes (first 24 hex chars of SHA256 over database+normalized unique record ID) and snapshot citation counts. Titles, abstracts, bibliographic exports and local computer paths are **not** released.
- `verify_public_s9k.py`: recomputes correlations and overlap **from the released aggregate and hashed ranking evidence**; Python standard library only.
- `reproduce_s9k_from_local_exports.py`: re-generates all S9K reference outputs from paired licensed WoSCC full-record TXT and Scopus CSV input files using normalized UT/EID IDs. No source file is modified.
- `01_INPUT_LOCAL/README.txt`, `01_RUN_WITH_LOCAL_EXPORTS.ps1`: instructions and Windows one-shot local re-analysis. Outputs are created in a new timestamped folder (never overwrites sources).

## Public validation / 无需原始文献数据的核查

```powershell
python .\09_AB_ABC_Annual_Citation_S9K\verify_public_s9k.py
```

Or use the top-level `00_RUN_PUBLIC_SELFTEST_PLUS_S9J_S9K.ps1` to verify the full release.

## Numerical results / 核对结果

| Result | WoSCC | Scopus |
|---|---:|---:|
| AB / ABC eligible records | 519 / 318 | 711 / 420 |
| Pearson r across 2015–2025 annual counts | 0.9525 | 0.9797 |
| Citation Top10 membership overlap | 8/10 | 7/10 |
| Citation Top20 membership overlap | 14/20 | 14/20 |

**Caveat / 限制.** This is an analysis of retrieval specification. High annual correlation does not imply stable citation rankings or fine-scale network clusters. A separate CiteSpace AB/ABC keyword network comparison is provided in module 08 and Supplementary Table S9 Panel J. The public-only test verifies that released derived summaries are internally consistent, not that a licensed source export has been independently reacquired or that the entire historical workflow has been re-run.

**中文：** 年度相关、引文Top10/Top20重合均按同库、同批次、2015–2025 年份计算；不与6月冻结540篇的跨库TC混用。公开结果包括逐年计数和脱敏后排名标识，仅支持公开汇总的复核；合法取得的原始检索记录需在作者本地通过脚本重算。