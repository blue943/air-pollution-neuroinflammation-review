$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$py=if(Get-Command python -ErrorAction SilentlyContinue){'python'}else{'py'}
$prefix=if($py -eq 'py'){@('-3')}else{@()}
$base=Join-Path $root '01_Core540'
$inp=Join-Path $base '01_INPUT_LOCAL'
$fp=Join-Path $root '02_Focused374/01_INPUT_LOCAL'
$files=@((Join-Path $inp 'Final540_WoSPriority.txt'),(Join-Path $inp 'WoSCC_AB_526_FullRecord.txt'),(Join-Path $inp 'WoSCC_ABC_321_FullRecord.txt'),(Join-Path $fp 'Frozen540_WoS_priority_TC.txt'),(Join-Path $fp 'Focused375_CiteSpace.txt'))
foreach($f in $files){if(-not(Test-Path -LiteralPath $f)){throw "Missing licensed input file: $f"}}
$results=Join-Path $root 'LOCAL_RESULTS_DO_NOT_UPLOAD'
if(Test-Path $results){throw 'Refusing to overwrite LOCAL_RESULTS_DO_NOT_UPLOAD; archive existing results before re-running'}
& $py @prefix (Join-Path $base '02_CODE/read_only_input_qc.py') --input (Join-Path $inp 'Final540_WoSPriority.txt')
if($LASTEXITCODE -ne 0){throw 'Input 540 QC failed'}
& $py @prefix (Join-Path $base '02_CODE/woscc_ab_abc_keyword.py') --ab (Join-Path $inp 'WoSCC_AB_526_FullRecord.txt') --abc (Join-Path $inp 'WoSCC_ABC_321_FullRecord.txt') --check-only
if($LASTEXITCODE -ne 0){throw 'AB/ABC source QC failed'}
New-Item -ItemType Directory -Path $results | Out-Null
& $py @prefix (Join-Path $base '02_CODE/figure6_s7.py') --input (Join-Path $inp 'Final540_WoSPriority.txt') --outdir (Join-Path $results 'Figure6_S7')
if($LASTEXITCODE -ne 0){throw 'Figure6/S7 failed'}
& $py @prefix (Join-Path $base '02_CODE/woscc_ab_abc_keyword.py') --ab (Join-Path $inp 'WoSCC_AB_526_FullRecord.txt') --abc (Join-Path $inp 'WoSCC_ABC_321_FullRecord.txt') --out (Join-Path $results 'WoSCC_AB_ABC')
if($LASTEXITCODE -ne 0){throw 'AB/ABC experiment failed'}
& $py @prefix (Join-Path $root '02_Focused374/verify_focused374.py') --full540 (Join-Path $fp 'Frozen540_WoS_priority_TC.txt') --historical375 (Join-Path $fp 'Focused375_CiteSpace.txt') --output (Join-Path $results 'Focused374')
if($LASTEXITCODE -ne 0){throw 'Focused374 comparison failed'}
Write-Host 'PASS: licensed local workflows completed. Keep LOCAL_RESULTS_DO_NOT_UPLOAD private.' -ForegroundColor Green
