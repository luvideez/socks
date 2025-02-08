@echo off
title Bat/Tat Proxy Server, Bitvise SSH Client + TLP

set "bitvise_path=C:\Program Files (x86)\Bitvise SSH Client\BvSsh.exe"
set "file_path=C:\Users\Luvideez\Desktop\ditucogivui.tlp"
set "process_name=notepad.exe"  REM *** THAY DOI TEN TIEN TRINH TAI DAY ***

:MENU
cls
echo --------------------------------------
echo Lua chon chuc nang:
echo 1. Bat Proxy Server (127.0.0.1:9999) va kiem tra Bitvise + TLP
echo 2. Tat Proxy Server va dung Bitvise SSH Client + TLP sau 5 giay
echo 3. Thoat
echo --------------------------------------
set /p choice="Nhap lua chon cua ban: "

if "%choice%"=="1" goto ENABLE_PROXY
if "%choice%"=="2" goto DISABLE_PROXY
if "%choice%"=="3" exit

echo Lua chon khong hop le. Vui long thu lai.
pause
goto MENU

:ENABLE_PROXY
cls
echo Dang bat Proxy Server (127.0.0.1:9999)...

reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d "127.0.0.1:9999" /f

REM Kiem tra Bitvise SSH Client co dang chay khong
tasklist /FI "IMAGENAME eq BvSsh.exe" /NH | find /I "BvSsh.exe" > nul
if %errorlevel% neq 0 (
    echo Bitvise SSH Client chua chay, dang mo file ditucogivui.tlp...
    start "" "%file_path%"
) else (
    echo Bitvise SSH Client da chay.
)

goto MENU

:DISABLE_PROXY
cls
echo Dang tat Proxy Server va dung Bitvise SSH Client + TLP sau 5 giay...

reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /f

echo Dang doi 2 giay...
timeout /t 2 /nobreak > nul

REM Dung Bitvise SSH Client
taskkill /F /IM BvSsh.exe

REM Dung file TLP
taskkill /F /IM "%process_name%"

exit
