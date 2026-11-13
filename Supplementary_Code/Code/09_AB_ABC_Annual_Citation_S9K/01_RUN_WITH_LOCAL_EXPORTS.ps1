$ErrorActionPreference='Stop'
$here=$PSScriptRoot
$inp=Join-Path $here '01_INPUT_LOCAL'
$req=@('WoSCC_AB_526_FullRecord.txt','WoSCC_ABC_321_FullRecord.txt','Scopus_AB_Full.csv','Scopus_ABC_Full.csv')
foreach($f in $req){$p=Join-Path $inp $f;if(!(Test-Path -LiteralPath $p -PathType Leaf)){throw ('Missing licensed local input: '+$p)}}
$py=if(Get-Command py -ErrorAction SilentlyContinue){'py'}elseif(Get-Command python -ErrorAction SilentlyContinue){'python'}else{throw 'Python 3 required'}
$prefix=if($py -eq 'py'){@('-3')}else{@()}
$out=Join-Path $here ('OUTPUT_LOCAL_'+(Get-Date -Format 'yyyyMMdd_HHmmss'))
if(Test-Path -LiteralPath $out){throw ('Output already exists: '+$out)}
New-Item -ItemType Directory -Path $out -ErrorAction Stop | Out-Null
& $py @prefix (Join-Path $here 'reproduce_s9k_from_local_exports.py') --wos-ab (Join-Path $inp $req[0]) --wos-abc (Join-Path $inp $req[1]) --scopus-ab (Join-Path $inp $req[2]) --scopus-abc (Join-Path $inp $req[3]) --out $out
if($LASTEXITCODE -ne 0){throw 'S9K local source comparison failed'}
Write-Host ('PASS: outputs in '+$out) -ForegroundColor Green
