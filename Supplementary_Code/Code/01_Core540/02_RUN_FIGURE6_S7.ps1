# Explicit user-initiated local output; refuses overwrite.
$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$python=if(Get-Command python -ErrorAction SilentlyContinue){'python'}else{'py'}
$prefix=if($python -eq 'py'){@('-3')}else{@()}
$inp=Join-Path $root '01_INPUT_LOCAL\Final540_WoSPriority.txt'
$out=Join-Path $root '04_OUTPUT_LOCAL\Figure6_S7_Local'
if(-not(Test-Path -LiteralPath $inp)){throw "Missing licensed input: $inp"}
if(Test-Path -LiteralPath $out){throw "REFUSE OVERWRITE: $out"}
& $python @prefix (Join-Path $root '02_CODE\read_only_input_qc.py') --input $inp
if($LASTEXITCODE -ne 0){throw 'Input QC failed'}
& $python @prefix (Join-Path $root '02_CODE\figure6_s7.py') --input $inp --outdir $out
if($LASTEXITCODE -ne 0){throw 'Figure6/S7 run failed'}
Write-Host "Outputs are in $out. Verify against 03_REFERENCE_OUTPUTS before manuscript use."
