# SSZ φ-Spiral Metric - Installation Script for Windows
# © 2025 Carmen Wrede & Lino Casu
# Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "SSZ φ-Spiral Metric - Installation (Windows)" -ForegroundColor Cyan
Write-Host "v1.0.0 FINAL - Complete & Validated" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
    
    # Extract version number
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 10)) {
            Write-Host "✗ ERROR: Python 3.10+ required, found $pythonVersion" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "✗ ERROR: Python not found. Please install Python 3.10 or later." -ForegroundColor Red
    Write-Host "  Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
Write-Host "  • numpy" -ForegroundColor White
Write-Host "  • scipy" -ForegroundColor White
Write-Host "  • sympy" -ForegroundColor White
Write-Host "  • matplotlib" -ForegroundColor White
Write-Host ""

$packages = @("numpy", "scipy", "sympy", "matplotlib")

foreach ($package in $packages) {
    Write-Host "Installing $package..." -ForegroundColor Gray
    python -m pip install --upgrade $package --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ $package installed" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Failed to install $package" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "✓ All dependencies installed successfully!" -ForegroundColor Green

Write-Host ""

# Ask if user wants to run tests
Write-Host "================================================================" -ForegroundColor Cyan
$runTests = Read-Host "Run validation tests? (y/n)"

if ($runTests -eq "y" -or $runTests -eq "Y") {
    Write-Host ""
    Write-Host "Running validation tests..." -ForegroundColor Yellow
    Write-Host ""
    
    python tests/test_validation_ssz_calibrated.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✓ All tests passed!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "✗ Some tests failed. Check output above." -ForegroundColor Red
    }
}

Write-Host ""

# Ask if user wants to generate validation report
Write-Host "================================================================" -ForegroundColor Cyan
$genReport = Read-Host "Generate complete validation report? (y/n)"

if ($genReport -eq "y" -or $genReport -eq "Y") {
    Write-Host ""
    Write-Host "Generating validation report..." -ForegroundColor Yellow
    Write-Host "This will create:" -ForegroundColor White
    Write-Host "  • 3 plots (300 DPI)" -ForegroundColor White
    Write-Host "  • 2 certificates" -ForegroundColor White
    Write-Host "  • 1 JSON file" -ForegroundColor White
    Write-Host "  • Complete scientific report" -ForegroundColor White
    Write-Host ""
    
    python generate_validation_report.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✓ Validation report generated successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Reports available in:" -ForegroundColor White
        Write-Host "  reports/SSZ_VALIDATION_REPORT.md" -ForegroundColor Cyan
        Write-Host "  reports/SSZ_VALIDATION_REPORT.tex" -ForegroundColor Cyan
        Write-Host "  reports/SSZ_CERTIFICATE_EARTH.txt" -ForegroundColor Cyan
        Write-Host "  reports/SSZ_CERTIFICATE_SUN.txt" -ForegroundColor Cyan
        Write-Host "  reports/ssz_validation_certificate.json" -ForegroundColor Cyan
        Write-Host "  reports/figures/*.png" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "✗ Report generation failed. Check output above." -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Quick Start:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  # Run all validation tests:" -ForegroundColor White
Write-Host "  python tests/test_validation_ssz_calibrated.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "  # Run consistency validator:" -ForegroundColor White
Write-Host "  python src/ssz_metric_pure/ssz_validator.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "  # Generate complete report:" -ForegroundColor White
Write-Host "  python generate_validation_report.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "  # Compare all metric forms:" -ForegroundColor White
Write-Host "  python FINAL_COMPARISON_AND_INTERPRETATION.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "  # View final summary:" -ForegroundColor White
Write-Host "  python FINAL_SUMMARY_AND_REPORT.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Yellow
Write-Host "  • MASTER_README.md - Complete overview" -ForegroundColor White
Write-Host "  • INDEX.md - File navigation" -ForegroundColor White
Write-Host "  • reports/SSZ_VALIDATION_REPORT.md - Scientific validation" -ForegroundColor White
Write-Host ""
Write-Host "© 2025 Carmen Wrede & Lino Casu" -ForegroundColor Gray
Write-Host "Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4" -ForegroundColor Gray
Write-Host ""
Write-Host '"No Singularities. Pure Physics. φ-Driven."' -ForegroundColor Cyan
Write-Host ""
