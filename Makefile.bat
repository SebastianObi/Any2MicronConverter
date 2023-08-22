cd any2micronconverter
py -m PyInstaller main.spec
xcopy /e /v /Y dist ..\dist\
del version.rc
cd ..