# Audit Attachment A — 217 duplicate pairs and 8 subsequent removals

**Public derived record-identity crosswalk, included with author permission (2 November 2026).**

- `Audit_Attachment_A_217_Pairs.csv`: 217 paired WoSCC UT and Scopus EID identifiers, matching basis, DOI-string equality, normalized-title equality, year equality, and checks against the 548/540-stage membership snapshots. The 217 paired Scopus copies are absent from the 548-record post-deduplication file; all WoSCC counterparts were present at that stage. **One** WoS counterpart was excluded at a later QC stage, so **216**, not 217, are present in the final 540 file.
- `Audit_Attachment_A_8_Removals.csv`: seven subsequent exclusions between 548 and 541 (4 indexed 2026; 2 non-English; 1 retracted) plus the final residual duplicate between 541 and 540, with record identifiers and removal reason.
- `Audit_A_Validation_Summary.json`: values checked from the two tables; `validate_audit_A.py` reproduces these checks from the public crosswalk.

First-stage match categories: 215 exact original DOI strings; 2 title/year matches with DOI-string variations. **One** of the 215 DOI-exact pairs had a difference in the source publication-year field; this is retained in `Year_Match=NO`, not silently converted to a full match.

**Provenance scope:** These are derived record-identity decision summaries, not licensed abstracts, article texts, or full database exports. The original 2026-11-01 internal file included an administrative `Author_Approval_Status=PENDING` column. Only that historical administrative column has been omitted in the public copy; every other data field has been kept. The author's separately confirmed approval of the **374-paper topical classification** does not imply separate sign-off of each deduplication pair. Crosswalk identity checks do not establish the historical time when the original deduplication script was run, and this public archive does not independently rerun original source matching.

## 中文说明

本附件由内部母档中的217组WoSCC UT/Scopus EID配对和7+1条后续移除记录派生。仅删除与科研判断无关的旧管理列`Author_Approval_Status`，保留匹配方式、DOI/题名/年份是否一致、以及548和540阶段的成员状态。215组DOI原始字符串相同，2组为DOI变体，另有1组虽DOI相同但年份字段不同；这三条特殊记录仍可在表中找到。217个WoSCC原始配对记录均在548阶段保留，其中1条后来在QC中排除，因此最终540阶段仅有216条。作者已允许共享这些记录标识符对照，但374篇主题分类已核准不代表去重配对逐条签认；本核验也不代表历史运行时间戳已被独立复核。
