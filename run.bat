@echo off
REM Script de inicio rápido
REM Ejecuta la aplicación directamente

echo ========================================================
echo   Solucionador Educativo de Series de Fourier
echo ========================================================
echo.
echo Iniciando aplicacion...
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ERROR: No se pudo ejecutar la aplicacion
    echo.
    echo Asegurate de haber instalado las dependencias:
    echo   install.bat
    echo.
    pause
)
