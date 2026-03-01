# Generate and optimize SVG files
# Usage: .\generate-optimized.ps1

$python = "C:\Users\Liam Scrase\AppData\Local\Microsoft\WindowsApps\python.exe"

# Blue
Write-Host "Generating dither-blue.svg..." -ForegroundColor Cyan
& $python generate_dither_svg-blue.py | Out-File -Encoding UTF8 -NoNewline dither-blue-temp.svg
Write-Host "Optimizing dither-blue.svg..." -ForegroundColor Cyan
npx -y svgo dither-blue-temp.svg -o dither-blue.svg
Remove-Item dither-blue-temp.svg

# Blue Horizontal
Write-Host "`nGenerating dither-blue-horizontal.svg..." -ForegroundColor Cyan
& $python generate_dither_svg-horizontal-blue.py | Out-File -Encoding UTF8 -NoNewline dither-blue-horizontal-temp.svg
Write-Host "Optimizing dither-blue-horizontal.svg..." -ForegroundColor Cyan
npx -y svgo dither-blue-horizontal-temp.svg -o dither-blue-horizontal.svg
Remove-Item dither-blue-horizontal-temp.svg

# Green
Write-Host "`nGenerating dither-green.svg..." -ForegroundColor Cyan
& $python generate_dither_svg-green.py | Out-File -Encoding UTF8 -NoNewline dither-green-temp.svg
Write-Host "Optimizing dither-green.svg..." -ForegroundColor Cyan
npx -y svgo dither-green-temp.svg -o dither-green.svg
Remove-Item dither-green-temp.svg

# Green Horizontal
Write-Host "`nGenerating dither-green-horizontal.svg..." -ForegroundColor Cyan
& $python generate_dither_svg-horizontal-green.py | Out-File -Encoding UTF8 -NoNewline dither-green-horizontal-temp.svg
Write-Host "Optimizing dither-green-horizontal.svg..." -ForegroundColor Cyan
npx -y svgo dither-green-horizontal-temp.svg -o dither-green-horizontal.svg
Remove-Item dither-green-horizontal-temp.svg

# Blue Large
Write-Host "`nGenerating dither-blue-large.svg..." -ForegroundColor Cyan
& $python generate_dither_svg-blue-large.py | Out-File -Encoding UTF8 -NoNewline dither-blue-large-temp.svg
Write-Host "Optimizing dither-blue-large.svg..." -ForegroundColor Cyan
npx -y svgo dither-blue-large-temp.svg -o dither-blue-large.svg
Remove-Item dither-blue-large-temp.svg

# Green Large
Write-Host "`nGenerating dither-green-large.svg..." -ForegroundColor Cyan
& $python generate_dither_svg-green-large.py | Out-File -Encoding UTF8 -NoNewline dither-green-large-temp.svg
Write-Host "Optimizing dither-green-large.svg..." -ForegroundColor Cyan
npx -y svgo dither-green-large-temp.svg -o dither-green-large.svg
Remove-Item dither-green-large-temp.svg

Write-Host "`nDone! File sizes:" -ForegroundColor Green
Get-ChildItem dither-*.svg | Select-Object Name, @{Name='Size (KB)';Expression={[math]::Round($_.Length/1KB, 2)}} | Sort-Object Name | Format-Table -AutoSize
