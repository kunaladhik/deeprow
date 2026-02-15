@echo off
REM =====================================================
REM DataFlow AI - Setup & Run Script
REM =====================================================

:start
cls
echo.
echo ============================================
echo   DataFlow AI - Setup & Run
echo ============================================
echo.
echo Checking for Node.js...
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Node.js is NOT installed!
    echo.
    echo Please download and install Node.js LTS from:
    echo https://nodejs.org/
    echo.
    echo After installation:
    echo 1. Restart your computer
    echo 2. Run this script again
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
    echo ✅ Node.js found: !NODE_VERSION!
)

echo.
echo Checking for npm...
echo.

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  npm is NOT installed!
    echo Please reinstall Node.js from: https://nodejs.org/
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('npm --version') do set NPM_VERSION=%%i
    echo ✅ npm found: !NPM_VERSION!
)

echo.
echo ============================================
echo Ready to install dependencies!
echo ============================================
echo.
echo This will install all required packages.
echo First-time installation may take 5-10 minutes.
echo.
pause

cd /d "C:\Users\kunal\OneDrive\Desktop\DeepRow UI"

echo.
echo Installing dependencies... This may take a few minutes.
echo.

npm install

if errorlevel 1 (
    echo.
    echo ❌ Installation failed!
    echo Please try again or check the error messages above.
    pause
    exit /b 1
)

echo.
echo ✅ Dependencies installed successfully!
echo.
echo ============================================
echo Starting development server...
echo ============================================
echo.
echo The app will open at: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server.
echo.
pause

npm run dev

pause
