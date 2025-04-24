@echo off
chcp 852 >nul
setlocal enabledelayedexpansion

set "TMPACL=%TEMP%\_acl_lines.txt"
set "TMPGRP=%TEMP%\_grupy_all.txt"


del "%TMPACL%" "%TMPGRP%" 2>nul


set /p FOLDERS=Provide folder paths separated by spaces (ex: F:\ak_collection G:\test): 

for %%F in (%FOLDERS%) do (
    set "FOLDER=%%F"
    
    if exist "!FOLDER!" (
        echo Processing: !FOLDER!
        icacls "!FOLDER!" > "%TMPACL%"

        for /f "tokens=2 delims=\ " %%A in ('findstr /R "\\.*:" %TMPACL%') do (
            for /f "tokens=1 delims=:" %%B in ("%%A") do (
                echo %%B>>"%TMPGRP%"
            )
        )
    ) else (
        echo Folder doesn't exist: %%F
    )
)

set "LASTLINE="
set /a COUNT=0
for /f "delims=" %%L in ('sort "%TMPGRP%"') do (
    if "%%L" neq "!LASTLINE!" (
        set /a COUNT+=1
        set "GRP_!COUNT!=%%L"
        set "LASTLINE=%%L"
    )
)

echo.
echo ========== RAPORT GRUP (net group /domain) ==========
echo.

for /l %%i in (1,1,%COUNT%) do (
    call set "GROUPNAME=%%GRP_%%i%%"
    echo ---------------------------------------------
    echo [%%i] GRUPA: !GROUPNAME!
    echo ---------------------------------------------
    net group "!GROUPNAME!" /domain
    echo.
    echo.
)

pause
