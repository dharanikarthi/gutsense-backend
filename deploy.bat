@echo off
echo Committing backend changes...
git add .
git commit -m "Fix Vercel crash: simplified backend without database dependencies"
git push
echo Done!