@echo off
rem Debate plugin launcher (Windows twin of the POSIX sibling, field finding
rem F24): run the BUNDLED engine, never a PATH-installed one. Resolves the
rem plugin root from this script's own installed location, so no environment
rem variable, pip install, or network access is required. Interpreter order
rem matters: the Microsoft Store "python3" shim prints an ad and EXITS 0, so
rem it must never appear in the chain; py.exe and a real python.exe report
rem honest exit codes.
setlocal
set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "PLUGIN_ROOT=%%~fI"
set "PYTHONPATH=%PLUGIN_ROOT%\src;%PYTHONPATH%"
where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py -3 -m debate %*
) else (
  python -m debate %*
)
exit /b %ERRORLEVEL%
