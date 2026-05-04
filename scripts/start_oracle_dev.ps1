param(
    [int]$TimeoutSeconds = 120
)

$ErrorActionPreference = 'Stop'

Write-Host 'Reiniciando OracleServiceORCL...'
Restart-Service -Name OracleServiceORCL -Force

$deadline = (Get-Date).AddSeconds($TimeoutSeconds)
while ((Get-Date) -lt $deadline) {
    $status = lsnrctl status 2>&1 | Out-String
    if ($status -match 'El servicio "orclpdb"' -and $status -match 'estado READY') {
        Write-Host 'Oracle listo: orclpdb esta registrado y READY.'
        exit 0
    }

    Write-Host 'Esperando orclpdb en el listener...'
    Start-Sleep -Seconds 5
}

Write-Error "Oracle no registro orclpdb en $TimeoutSeconds segundos. Ejecuta: lsnrctl status"
exit 1
