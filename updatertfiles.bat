@echo off
robocopy realtime_data\masks C:\Code\zeepheru-github-pages\files /E
copy realtime_data\config.json C:\Code\zeepheru-github-pages\files

cd C:\Code\zeepheru-github-pages
git init
git add .
git commit -m "rt config update"
git push origin main
cd C:\Code\py-bigmistake