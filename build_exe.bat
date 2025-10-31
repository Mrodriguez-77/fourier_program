@echo off
REM Script para compilar la aplicación a ejecutable
REM Requiere PyInstaller instalado (pip install pyinstaller)

echo ================================================
echo   Compilando Solucionador de Series de Fourier
echo ================================================
echo.

REM Verificar si existe PyInstaller
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo ERROR: PyInstaller no esta instalado
    echo Instalando PyInstaller...
    pip install pyinstaller
)

echo Limpiando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist main.spec del main.spec

echo.
echo Compilando aplicacion...
echo.

pyinstaller --onefile --windowed --name="FourierSolver" --icon=assets\icon.ico main.py

if errorlevel 1 (
    echo.
    echo ERROR: La compilacion fallo
    pause
    exit /b 1
)

echo.
echo ================================================
echo   Compilacion completada exitosamente!
echo ================================================
echo.
echo El ejecutable se encuentra en: dist\FourierSolver.exe
echo.
pause
