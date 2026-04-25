# 35.ps1 - ProDig Diamond Report
# Super compatible version

Write-Host "`n----------------------------------------------" -ForegroundColor Cyan
Write-Host "    REPORTE DIAMANTE: PRODIG ANALYTICS"
Write-Host "----------------------------------------------`n"

# 1. Total Events
$resTotal = npx @insforge/cli db query "SELECT count(*) FROM prodig_telemetry;" | Out-String
$total = 0
$cleanTotal = $resTotal -replace "`e\[[0-9;]*m", ""
if ($cleanTotal -match "(\d+)") { $total = [int]$matches[1] }

# 2. International Traffic
$intlRaw = npx @insforge/cli db query "SELECT user_lang, count(*) FROM prodig_telemetry WHERE user_lang NOT ILIKE 'es%' GROUP BY user_lang ORDER BY 2 DESC LIMIT 3;" | Out-String
Write-Host "[TRAFICO INTERNACIONAL]" -ForegroundColor Yellow
if ($total -gt 0 -and ($intlRaw -match "\|")) {
    $rows = $intlRaw -split "`n"
    foreach ($line in $rows) {
        if ($line -match "([a-zA-Z-]+)\s+\|\s+(\d+)") {
            $lang = $matches[1]
            $cnt = $matches[2]
            $p = [math]::Round(([int]$cnt / $total) * 100, 1)
            Write-Host "- ${lang}: ${p}% (${cnt} eventos)"
        }
    }
} else {
    Write-Host "- Sin trafico internacional detectado o datos insuficientes."
}

# 3. Security
$secRaw = npx @insforge/cli db query "SELECT count(*) FROM prodig_telemetry WHERE (url ~* '<script' OR metadata::text ~* '<script') AND timestamp > now() - interval '24 hours';" | Out-String
$alerts = 0
$cleanSec = $secRaw -replace "`e\[[0-9;]*m", ""
if ($cleanSec -match "(\d+)") { $alerts = [int]$matches[1] }

Write-Host "`n[SEGURIDAD]" -ForegroundColor Red
if ($alerts -gt 0) {
    Write-Host "- ALERTA: ${alerts} eventos sospechosos detectados en 24h."
} else {
    Write-Host "- STATUS: Limpio."
}

Write-Host "`n----------------------------------------------`n" -ForegroundColor Cyan
