# WoSCC-only paired keyword experiment; does not modify 540 master data.
$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$python=if(Get-Command python -ErrorAction SilentlyContinue){'python'}else{'py'}
$prefix=if($python -eq 'py'){@('-3')}else{@()}
$ab=Join-Path $root '01_INPUT_LOCAL\WoSCC_AB_526_FullRecord.txt'
$abc=Join-Path $root '01_INPUT_LOCAL\WoSCC_ABC_321_FullRecord.txt'
$out=Join-Path $root '04_OUTPUT_LOCAL\WoSCC_ABABC_Local'
if(-not((Test-Path -LiteralPath $ab) -and (Test-Path -LiteralPath $abc))){throw 'Stage both licensed WoSCC paired export TXT files in 01_INPUT_LOCAL'}
if(Test-Path -LiteralPath $out){throw "REFUSE OVERWRITE: $out"}
& $python @prefix (Join-Path $root '02_CODE\woscc_ab_abc_keyword.py') --ab $ab --abc $abc --check-only
if($LASTEXITCODE -ne 0){throw 'Read-only paired QC failed'}
& $python @prefix (Join-Path $root '02_CODE\woscc_ab_abc_keyword.py') --ab $ab --abc $abc --out $out
if($LASTEXITCODE -ne 0){throw 'Paired experiment failed'}
Write-Host "New local outputs: $out"
