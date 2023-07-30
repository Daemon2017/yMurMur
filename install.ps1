Invoke-WebRequest "https://master.dl.sourceforge.net/project/phylomurka/murka/murka-1.4.1/murka-1.4.1-win64.zip?viasf=1" -OutFile "murka-1.4.1-win64.zip"
Expand-Archive "murka-1.4.1-win64.zip" -DestinationPath "murka-1.4.1-win64"
Move-Item -Path "./murka-1.4.1-win64/murka-1.4.1-win64" -Destination "./murka" -force
Remove-Item -Path "./murka-1.4.1-win64.zip"
Remove-Item -Path "./murka-1.4.1-win64"
Invoke-WebRequest "https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-win32.zip" -OutFile "python-3.10.11-embed-win32.zip"
Expand-Archive "python-3.10.11-embed-win32.zip" -DestinationPath "python"
Remove-Item -Path "./python-3.10.11-embed-win32.zip"
Invoke-WebRequest "https://bootstrap.pypa.io/get-pip.py" -OutFile "./python/get-pip.py"
./python/python.exe ./python/get-pip.py
$content=@'
python310.zip
.
Lib
Lib\site-packages
'@
New-Item -ItemType File -Path ./python/python310._pth -Value $content -Force
./python/python.exe -m pip install -r requirements.txt