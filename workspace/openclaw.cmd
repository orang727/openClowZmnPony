@echo off
REM Wrapper to block dangerous openclaw commands from agent

set "args=%*"

REM Check for forbidden commands
echo %args% | findstr /i "gateway daemon node reset uninstall" >nul
if %errorlevel%==0 (
    echo ERROR: This command is blocked for safety reasons.
    echo The agent cannot run openclaw gateway/daemon/node/reset/uninstall commands.
    echo These commands would crash the runtime environment.
    exit /b 1
)

REM Pass through to real openclaw
"C:\Users\Administrator\AppData\Roaming\npm\openclaw.cmd" %*
