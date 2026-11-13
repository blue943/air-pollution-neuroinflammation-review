$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$py=if(Get-Command python -ErrorAction SilentlyContinue){'python'}else{'py'}
$prefix=if($py -eq 'py'){@('-3')}else{@()}
& $py @prefix (Join-Path $root 'verify_package.py')
if($LASTEXITCODE -ne 0){throw 'Package hash verification failed'}
& $py @prefix (Join-Path $root '03_CiteSpace_Keyword_Comparison/reproduce_cluster_metrics.py')
if($LASTEXITCODE -ne 0){throw 'Cluster comparison failed; check Python 3 and the retained input tables'}
& $py @prefix (Join-Path $root '03_CiteSpace_Keyword_Comparison/validate_focused374_graphml.py')
if($LASTEXITCODE -ne 0){throw 'Focused 374 native GraphML evidence verification failed'}
& $py @prefix (Join-Path $root '06_Record_QC_Summary/validate_audit_A.py')
if($LASTEXITCODE -ne 0){throw 'Audit A crosswalk validation failed'}
& $py @prefix (Join-Path $root '04_CiteSpace_PubMed/validate_pubmed_keyword_graphs.py')
if($LASTEXITCODE -ne 0){throw 'PubMed keyword-only GraphML verification failed'}
Write-Host 'PASS: integrity, 540/374 derived clusters, Audit A crosswalk, focused 374 native GraphML, and PubMed 2015-2025 network metadata checks.' -ForegroundColor Green
