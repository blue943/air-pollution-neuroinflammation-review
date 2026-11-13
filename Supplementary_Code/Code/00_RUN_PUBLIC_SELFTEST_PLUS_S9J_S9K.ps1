$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$py=if(Get-Command python -ErrorAction SilentlyContinue){'python'}elseif(Get-Command py -ErrorAction SilentlyContinue){'py'}else{throw 'Python 3 required'}
$prefix=if($py -eq 'py'){@('-3')}else{@()}
& $py @prefix (Join-Path $root 'verify_package.py')
if($LASTEXITCODE -ne 0){throw 'Package integrity validation failed'}
& (Join-Path $root '00_RUN_PUBLIC_SELFTEST.ps1')
if($LASTEXITCODE -ne 0){throw 'Original public self-test failed'}
& $py @prefix (Join-Path $root '08_WoSCC_AB_ABC_CiteSpace/verify_s9j_networks.py')
if($LASTEXITCODE -ne 0){throw 'S9J comparison validation failed'}
& $py @prefix (Join-Path $root '09_AB_ABC_Annual_Citation_S9K/verify_public_s9k.py')
if($LASTEXITCODE -ne 0){throw 'S9K annual/citation validation failed'}
Write-Host 'PASS: original public checks + S9J + S9K' -ForegroundColor Green
