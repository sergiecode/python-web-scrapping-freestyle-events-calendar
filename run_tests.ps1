# PowerShell script for running tests on Windows
# Freestyle Events Calendar - Test Suite

param(
    [string]$TestType = "all",
    [switch]$Coverage = $false,
    [switch]$Verbose = $false
)

Write-Host "🧪 Freestyle Events Calendar - Test Suite" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python detectado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python no encontrado. Asegúrate de que Python esté instalado y en el PATH." -ForegroundColor Red
    exit 1
}

# Change to project directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$projectPath = Split-Path -Parent $scriptPath
Set-Location $projectPath

Write-Host "📁 Directorio del proyecto: $projectPath" -ForegroundColor Yellow

# Install test dependencies if needed
Write-Host "🔧 Verificando dependencias de prueba..." -ForegroundColor Yellow
try {
    python -c "import pytest" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "📦 Instalando dependencias de prueba..." -ForegroundColor Yellow
        pip install pytest pytest-cov
    }
} catch {
    Write-Host "📦 Instalando dependencias de prueba..." -ForegroundColor Yellow
    pip install pytest pytest-cov
}

# Run different types of tests based on parameter
switch ($TestType.ToLower()) {
    "unit" {
        Write-Host "🔬 Ejecutando pruebas unitarias..." -ForegroundColor Blue
        if ($Coverage) {
            python -m pytest tests/test_utils.py tests/test_scrapers.py -v --cov=scraper --cov-report=html
        } else {
            python -m pytest tests/test_utils.py tests/test_scrapers.py -v
        }
    }
    
    "web" {
        Write-Host "🌐 Ejecutando pruebas de aplicación web..." -ForegroundColor Blue
        if ($Coverage) {
            python -m pytest tests/test_webapp.py -v --cov=webapp --cov-report=html
        } else {
            python -m pytest tests/test_webapp.py -v
        }
    }
    
    "integration" {
        Write-Host "🔗 Ejecutando pruebas de integración..." -ForegroundColor Blue
        python -m pytest tests/test_integration.py -v
    }
    
    "all" {
        Write-Host "🚀 Ejecutando todas las pruebas..." -ForegroundColor Blue
        if ($Coverage) {
            python -m pytest tests/ -v --cov=scraper --cov=webapp --cov-report=html --cov-report=term
        } else {
            python -m pytest tests/ -v
        }
    }
    
    "quick" {
        Write-Host "⚡ Ejecutando pruebas rápidas (excluyendo lentas)..." -ForegroundColor Blue
        python -m pytest tests/ -v -m "not slow"
    }
    
    default {
        Write-Host "❌ Tipo de prueba no válido: $TestType" -ForegroundColor Red
        Write-Host "Tipos válidos: unit, web, integration, all, quick" -ForegroundColor Yellow
        exit 1
    }
}

$testResult = $LASTEXITCODE

# Show results
Write-Host ""
Write-Host "📊 RESULTADOS DE LAS PRUEBAS" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan

if ($testResult -eq 0) {
    Write-Host "🎉 ¡Todas las pruebas pasaron exitosamente!" -ForegroundColor Green
    
    if ($Coverage -and (Test-Path "htmlcov/index.html")) {
        Write-Host "📈 Reporte de cobertura generado en: htmlcov/index.html" -ForegroundColor Yellow
        Write-Host "   Para abrir: Start-Process htmlcov/index.html" -ForegroundColor Gray
    }
} else {
    Write-Host "💥 Algunas pruebas fallaron. Revisa los detalles arriba." -ForegroundColor Red
}

# Additional system checks
Write-Host ""
Write-Host "🔍 VERIFICACIONES DEL SISTEMA" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan

# Check if application can start
Write-Host "🌐 Verificando que la aplicación web puede iniciarse..." -ForegroundColor Yellow
try {
    $job = Start-Job -ScriptBlock {
        Set-Location $using:projectPath
        python webapp/app.py
    }
    
    Start-Sleep -Seconds 3
    
    if ($job.State -eq "Running") {
        Write-Host "✅ Aplicación web inicia correctamente" -ForegroundColor Green
        Stop-Job $job
        Remove-Job $job
    } else {
        Write-Host "❌ La aplicación web no pudo iniciarse" -ForegroundColor Red
        Receive-Job $job
        Remove-Job $job
    }
} catch {
    Write-Host "❌ Error al verificar la aplicación web: $_" -ForegroundColor Red
}

# Check database file
if (Test-Path "data/eventos.db") {
    Write-Host "✅ Base de datos encontrada: data/eventos.db" -ForegroundColor Green
} else {
    Write-Host "⚠️  Base de datos no encontrada. Ejecuta el scraper primero." -ForegroundColor Yellow
}

# Check CSV export
if (Test-Path "data/eventos.csv") {
    Write-Host "✅ Archivo CSV encontrado: data/eventos.csv" -ForegroundColor Green
} else {
    Write-Host "⚠️  Archivo CSV no encontrado." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🏁 Pruebas completadas" -ForegroundColor Cyan

exit $testResult
