$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$py=if(Get-Command python -ErrorAction SilentlyContinue){'python'}elseif(Get-Command py -ErrorAction SilentlyContinue){'py'}else{throw 'Python 3 required'}
$prefix=if($py -eq 'py'){@('-3')}else{@()}
& $py @prefix (Join-Path $root 'verify_package.py')
if($LASTEXITCODE -ne 0){throw 'Package SHA256 validation failed'}
& (Join-Path $root '00_RUN_PUBLIC_SELFTEST.ps1')
if($LASTEXITCODE -ne 0){throw 'Original public self-test failed'}
& $py @prefix (Join-Path $root '08_WoSCC_AB_ABC_CiteSpace/verify_s9j_networks.py')
if($LASTEXITCODE -ne 0){throw 'S9 Panel J AB/ABC network validation failed'}
Write-Host 'PASS: baseline public self-tests + S9 Panel J CiteSpace verification' -ForegroundColor Green
