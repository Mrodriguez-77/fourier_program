@echo off
REM Script de instalación y configuración
REM Solucionador Educativo de Series de Fourier

echo ========================================================
echo   Instalacion - Solucionador de Series de Fourier
echo ========================================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.8 o superior desde:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado
python --version
echo.

REM Verificar versión de Python
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"
if errorlevel 1 (
    echo ERROR: Se requiere Python 3.8 o superior
    pause
    exit /b 1
)

echo [OK] Version de Python compatible
echo.

REM Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip
echo.

REM Instalar dependencias
echo Instalando dependencias...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Hubo un problema instalando las dependencias
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================================
echo   Instalacion completada exitosamente!
echo ========================================================
echo.
echo Para ejecutar la aplicacion:
echo   python main.py
echo.
echo Para compilar a ejecutable:
echo   build_exe.bat
echo.
pause
