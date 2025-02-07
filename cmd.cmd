::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFDdBWg2GOW6gOpET/+b34OuDsXEURK8+fJ3eyafDdrRd40brFQ==
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSjk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJGyX8VAjFDdBWg2GOW6gOpEZ++Pv4Pq7kUIeX/FxfZfeug==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
title Bat/Tat Proxy Server va Quan Ly Bitvise + TLP

set "file_path=C:\Users\Luvideez\Desktop\ditucogivui.tlp"
set "process_name=notepad.exe"  REM *** THAY DOI TEN TIEN TRINH TAI DAY ***
set "bitvise_path=C:\Program Files (x86)\Bitvise SSH Client\BvSsh.exe"

:MENU
cls
echo --------------------------------------
:CHECK_PROXY_STATUS
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable | find "REG_DWORD" > nul
if %errorlevel% equ 0 (
    reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable | find "0x0" > nul
    if %errorlevel% equ 0 (
        echo   Hien dang TAT
        set "proxy_status=TAT"
    ) else (
        echo   Hien dang BAT
        set "proxy_status=BAT"
    )
) else (
    echo   Khong xac dinh duoc trang thai Proxy (co the chua duoc cau hinh)
    set "proxy_status=UNKNOWN"
)

echo Lua chon chuc nang:
echo 1. Bat Proxy Server (127.0.0.1:9999) va kiem tra/mo file ditucogivui.tlp
echo 2. Tat Proxy Server (127.0.0.1:9999) va dung Bitvise SSH Client
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

echo Da bat Proxy Server (127.0.0.1:9999).
echo Trang thai Proxy: BAT

REM Kiem tra file .tlp co dang chay khong
tasklist /FI "IMAGENAME eq %process_name%" /NH | find /I "%process_name%" > nul
if %errorlevel% neq 0 (
    echo File ditucogivui.tlp chua chay, dang mo...
    start "" "%file_path%"
) else (
    echo File ditucogivui.tlp da chay.
)

pause
goto MENU

:DISABLE_PROXY
cls
echo Dang tat Proxy Server (127.0.0.1:9999) va dung Bitvise SSH Client...

reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /f

echo Da tat Proxy Server (127.0.0.1:9999) va dung Bitvise SSH Client.
echo Trang thai Proxy: TAT

REM Dung Bitvise SSH Client
taskkill /F /IM BvSsh.exe

pause
goto MENU
