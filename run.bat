@echo off
REM =====================================================
REM DataFlow AI - React Application Quick Commands
REM =====================================================

:menu
cls
echo.
echo ============================================
echo   DataFlow AI - Quick Commands Menu
echo ============================================
echo.
echo 1. Install Dependencies (npm install)
echo 2. Start Development Server (npm run dev)
echo 3. Build for Production (npm run build)
echo 4. Preview Production Build (npm run preview)
echo 5. Run Linter (npm run lint)
echo 6. Open Project in VS Code
echo 7. Open Browser
echo 8. Check Node Version
echo 9. Clear node_modules & Reinstall
echo 10. Exit
echo.

set /p choice="Enter your choice (1-10): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto dev
if "%choice%"=="3" goto build
if "%choice%"=="4" goto preview
if "%choice%"=="5" goto lint
if "%choice%"=="6" goto vscode
if "%choice%"=="7" goto browser
if "%choice%"=="8" goto node_version
if "%choice%"=="9" goto reinstall
if "%choice%"=="10" goto end

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto menu

:install
echo.
echo Installing dependencies...
echo.
cd /d "C:\Users\kunal\OneDrive\Desktop\DeepRow UI"
npm install
echo.
echo Installation complete!
pause
goto menu

:dev
echo.
echo Starting development server...
echo Server will open at http://localhost:3000
echo.
cd /d "C:\Users\kunal\OneDrive\Desktop\DeepRow UI"
npm run dev
pause
goto menu

:build
echo.
echo Building for production...
echo.
cd /d "C:\Users\kunal\OneDrive\Desktop\DeepRow UI"
npm run build
echo.
echo Build complete! Output in dist/ folder.
pause
goto menu

:preview
echo.
echo Previewing production build...
echo.
cd /d "C:\Users\kunal\OneDrive\Desktop\DeepRow UI"
npm run preview
pause
goto menu

:lint
echo.
echo Running linter...
echo.
cd /d "C:\Users\kunal\OneDrive\Desktop\DeepRow UI"
npm run lint
echo.
echo Linting complete!
pause
goto menu

:vscode
echo.
echo Opening project in VS Code...
echo.
cd /d "C:\Users\kunal\OneDrive\Desktop\DeepRow UI"
code .
goto menu

:browser
echo.
echo Opening browser to localhost:3000...
echo.
start http://localhost:3000
goto menu

:node_version
echo.
node --version
npm --version
echo.
pause
goto menu

:reinstall
echo.
echo This will delete node_modules and reinstall packages.
set /p confirm="Are you sure? (y/n): "
if /i "%confirm%"=="y" (
    cd /d "C:\Users\kunal\OneDrive\Desktop\DeepRow UI"
    echo Removing node_modules...
    rmdir /s /q node_modules
    echo Installing dependencies...
    npm install
    echo Complete!
) else (
    echo Cancelled.
)
echo.
pause
goto menu

:end
echo.
echo Exiting...
exit /b 0
