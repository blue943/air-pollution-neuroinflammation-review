# Read-only check; no generated outputs.
$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } else { 'py' }
$prefix = if ($python -eq 'py') { @('-3') } else { @() }
$frozen = Join-Path $root '01_INPUT_LOCAL\Final540_WoSPriority.txt'
if (-not (Test-Path -LiteralPath $frozen)) { throw "Copy your licensed final 540 input to: $frozen" }
& $python @prefix (Join-Path $root '02_CODE\read_only_input_qc.py') --input $frozen
if ($LASTEXITCODE -ne 0) {throw 'Main corpus QC failed'}
$ab = Join-Path $root '01_INPUT_LOCAL\WoSCC_AB_526_FullRecord.txt'
$abc = Join-Path $root '01_INPUT_LOCAL\WoSCC_ABC_321_FullRecord.txt'
if ((Test-Path $ab) -and (Test-Path $abc)) {
  & $python @prefix (Join-Path $root '02_CODE\woscc_ab_abc_keyword.py') --ab $ab --abc $abc --check-only
  if ($LASTEXITCODE -ne 0) {throw 'WoSCC paired export QC failed'}
} else {Write-Host 'WoSCC paired QC skipped: licensed exports not staged.'}
Write-Host 'Read-only checks completed; no analysis files generated.'
