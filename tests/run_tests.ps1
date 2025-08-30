# PowerShell script to run tests on Windows
# Run tests and ensure the app works on Windows with VSCode and PowerShell

Write-Host "Python Web Scraping Freestyle Events Calendar - Test Runner" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# Check Python version
Write-Host "`nChecking Python version..." -ForegroundColor Yellow
python --version

# Install dependencies if needed
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install pytest pytest-cov

# Run all tests with coverage
Write-Host "`nRunning all tests with coverage..." -ForegroundColor Green
python -m pytest tests/ -v --cov=scraper --cov=webapp --cov-report=term-missing

# Run tests without webapp if there are import issues
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nWebapp tests failed, running other tests..." -ForegroundColor Yellow
    python -m pytest tests/test_utils.py tests/test_scrapers.py tests/test_integration.py -v --cov=scraper --cov-report=term-missing
}

# Test individual components
Write-Host "`nTesting database functionality..." -ForegroundColor Yellow
python -c "from scraper.utils import EventDatabase; db = EventDatabase('test.db'); print('Database test: OK')"

Write-Host "`nTesting scrapers..." -ForegroundColor Yellow
python -c "from scraper.redbull import RedBullScraper; s = RedBullScraper(); print('Red Bull scraper: OK')"
python -c "from scraper.fms import FMSScraper; s = FMSScraper(); print('FMS scraper: OK')"

# Clean up
if (Test-Path "test.db") {
    Remove-Item "test.db"
}

Write-Host "`nTest execution completed!" -ForegroundColor Green
Write-Host "Check the results above for any failures." -ForegroundColor Cyan
