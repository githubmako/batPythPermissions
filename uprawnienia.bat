@echo off
chcp 852 >nul
setlocal enabledelayedexpansion

set "RAWJSON=%USERPROFILE%\Desktop\uprawnienia.json"
set "FINALJSON=%USERPROFILE%\Desktop\uprawnienia_parsed.json"
set "TMPACL=%TEMP%\_acl_lines.txt"


del "%TMPACL%" "%RAWJSON%" "%FINALJSON%" 2>nul


set /p FOLDERS=Provide folder paths separated by spaces (ex: F:\ak_collection G:\test): 


echo [ > "%RAWJSON%"
set FIRSTFOLDER=1

for %%F in (%FOLDERS%) do (
    set "FOLDER=%%F"
    
    if exist "!FOLDER!" (
        echo Processing: !FOLDER!
        icacls "!FOLDER!" > "%TMPACL%"

        if !FIRSTFOLDER! equ 0 (
            echo , >> "%RAWJSON%"
        )
        set FIRSTFOLDER=0

        echo   { >> "%RAWJSON%"
        echo     "Path": "!FOLDER!", >> "%RAWJSON%"
        echo     "Acl": [ >> "%RAWJSON%"

        for /f "delims=" %%L in (%TMPACL%) do (
            echo       "%%L", >> "%RAWJSON%"
        )

        echo     ] >> "%RAWJSON%"
        echo   } >> "%RAWJSON%"
    ) else (
        echo Folder doesn't exist: %%F
    )
)

echo ] >> "%RAWJSON%"


powershell -NoProfile -Command ^
 $aclData = Get-Content -Raw -Path '%RAWJSON%' | ConvertFrom-Json; ^
 foreach ($entry in $aclData) { ^
   $entry.Acl = $entry.Acl | Where-Object { $_ -notmatch 'Successfully processed' } ^
 } ^
 $aclData | ConvertTo-Json -Depth 5 | Set-Content -Path '%FINALJSON%' -Encoding UTF8

echo.
pause
