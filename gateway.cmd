@echo off
rem OpenClaw Gateway (v2026.2.26)
set "TMPDIR=C:\Users\ADMINI~1\AppData\Local\Temp"
set "PATH=C:\Python314\Scripts\;C:\Python314\;C:\Program Files (x86)\ShadowBot;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Windows\System32\OpenSSH\;D:\jdk-17.0.9\bin;C:\ProgramData\chocolatey\bin;C:\Program Files\nodejs\;C:\Program Files\Qoder\bin;C:\Users\Administrator\AppData\Roaming\npm;C:\Users\Administrator\bin;C:\Users\Administrator\AppData\Roaming\Qoder\SharedClientCache\cli\bin\git\mingw64\bin;C:\Users\Administrator\AppData\Roaming\Qoder\SharedClientCache\cli\bin\git\usr\local\bin;C:\Users\Administrator\AppData\Roaming\Qoder\SharedClientCache\cli\bin\git\usr\bin;C:\Users\Administrator\AppData\Roaming\Qoder\SharedClientCache\cli\bin\git\usr\bin;C:\Users\Administrator\AppData\Roaming\Qoder\SharedClientCache\cli\bin\git\mingw64\bin;C:\Users\Administrator\AppData\Roaming\Qoder\SharedClientCache\cli\bin\git\usr\bin;C:\Users\Administrator\bin;C:\Python314\Scripts;C:\Python314;C:\Program Files (x86)\ShadowBot;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0;C:\Windows\System32\OpenSSH;D:\jdk-17.0.9\bin;C:\ProgramData\chocolatey\bin;C:\Program Files\nodejs;C:\Program Files\Qoder\bin;C:\Python314\Scripts;C:\Python314;C:\Program Files (x86)\ShadowBot;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0;C:\Windows\System32\OpenSSH;D:\jdk-17.0.9\bin;C:\ProgramData\chocolatey\bin;C:\Program Files\nodejs;C:\Program Files\Qoder\bin;C:\Program Files\nodejs;C:\Users\Administrator\AppData\Roaming\Qoder\SharedClientCache\cli\bin\git\usr\bin\vendor_perl;C:\Users\Administrator\AppData\Roaming\Qoder\SharedClientCache\cli\bin\git\usr\bin\core_perl;C:/Program Files/nodejs"
set "OPENCLAW_GATEWAY_PORT=18789"
set "OPENCLAW_GATEWAY_TOKEN=bb5ac5972b8945ad0b7222159a9a64c0905e917a7b0bd064"
set "OPENCLAW_SYSTEMD_UNIT=openclaw-gateway.service"
set "OPENCLAW_SERVICE_MARKER=openclaw"
set "OPENCLAW_SERVICE_KIND=gateway"
set "OPENCLAW_SERVICE_VERSION=2026.2.26"
set "BRAVE_API_KEY=BSAP3xm4s10rblwH8cJF8H2wfyKxze8"
"C:\Program Files\nodejs\node.exe" C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\dist\index.js gateway --port 18789
