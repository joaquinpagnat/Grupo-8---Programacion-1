@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul
if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
    "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -X utf8 main.py
    goto fin
)
where py >nul 2>nul
if not errorlevel 1 (
    py -3 -X utf8 main.py
    goto fin
)
where python >nul 2>nul
if not errorlevel 1 (
    python -X utf8 main.py
    goto fin
)
echo No se encontro Python. Instala Python 3.9 o posterior y volve a abrir este archivo.
:fin
echo.
pause
endlocal
