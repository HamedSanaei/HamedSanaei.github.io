$ErrorActionPreference = "Stop"

Write-Host "Publishing HamedSanaei.github.io..." -ForegroundColor Cyan

# Make sure Git is initialized
if (-not (Test-Path ".git")) {
    git init
}

# Stage all files
git add .

# Commit changes
git commit -m "feat: publish personal portfolio"

if ($LASTEXITCODE -ne 0) {
    Write-Host "No new changes to commit, continuing..." -ForegroundColor Yellow
}

# Ensure main branch
git branch -M main

# Configure origin
$remotes = git remote

if ($remotes -notcontains "origin") {
    git remote add origin https://github.com/HamedSanaei/HamedSanaei.github.io.git
}
else {
    git remote set-url origin https://github.com/HamedSanaei/HamedSanaei.github.io.git
}

# Push to GitHub
git push -u origin main

Write-Host ""
Write-Host "Done." -ForegroundColor Green
Write-Host "Your site should be available at:" -ForegroundColor Green
Write-Host "https://hamedsanaei.github.io/"
