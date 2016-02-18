@echo off
rem Script for run mediaportal on Sony TV

rem !!! REPLACE TO YOUR VALUES
set MEDIAPORTALPATH=C:\Program Files (x86)\Kodi
set MEDIAPORTALEXE=kodi
rem Volume for MediaPortal
set MEDIAPORTALVOLUME=50
rem HDMI4
set MEDIAPORTALINPUT=100000004

rem Check already started
tasklist /fi "IMAGENAME eq %MEDIAPORTALEXE%.exe" | find /C /I "%MEDIAPORTALEXE%" > NUL

if %ERRORLEVEL%==0 (
  echo Already running
  Exit 1
)

rem Enable TV
"python.exe" tv.py --wol
rem Waiting power on and skip power-on notify
"python.exe" tv.py --answer

rem Save current volume
"python.exe" tv.py VOLU > zvolume
if %ERRORLEVEL%==1 (
  set /p saveVol=<zvolume
) else (
  set /p saveVol=0
)

rem Save current input
"python.exe" tv.py INPT > zinput
if %ERRORLEVEL%==1 (
  set /p saveInput=<zinput
) else (
  set /p saveInput=0
)

rem Set volume to 40
"python.exe" tv.py VOLU%MEDIAPORTALVOLUME%

rem Set input to TV-PC connection
"python.exe" tv.py INPT%MEDIAPORTALINPUT%

rem Swith screen to TV
rem "DisplaySwitch.exe" /internal
"DisplaySwitch.exe" /external
timeout 4

rem Run and waiting media portal
start "Media" /B /WAIT "%MEDIAPORTALPATH%\%MEDIAPORTALEXE%"

rem Swith screen to PC
rem "DisplaySwitch.exe" /external
"DisplaySwitch.exe" /internal

rem Restore volume
if not %saveVol%==0 (
  "python.exe" tv.py VOLU%saveVol%
)

rem Restore input
if not %saveInput%==0 (
  "python.exe" tv.py INPT%saveInput%
)

rem Disable TV
"python.exe" tv.py POWR0

echo OK.