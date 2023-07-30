Invoke-WebRequest "https://master.dl.sourceforge.net/project/phylomurka/murka/murka-1.4.1/murka-1.4.1-win64.zip?viasf=1" -OutFile "murka-1.4.1-win64.zip"
Expand-Archive "murka-1.4.1-win64.zip" -DestinationPath "murka-1.4.1-win64"
Move-Item -Path "./murka-1.4.1-win64/murka-1.4.1-win64" -Destination "./murka" -force
Remove-Item -Path "./murka-1.4.1-win64.zip"
Remove-Item -Path "./murka-1.4.1-win64"
Invoke-WebRequest "https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/2.50.0/windows_10_msbuild_Release_graphviz-2.50.0-win32.zip" -OutFile "graphviz-2.50.0-win32.zip"
Expand-Archive "graphviz-2.50.0-win32.zip" -DestinationPath "graphviz-2.50.0-win32"
Move-Item -Path "./graphviz-2.50.0-win32/Graphviz" -Destination "./graphviz" -force
Remove-Item -Path "./graphviz-2.50.0-win32.zip"
Remove-Item -Path "./graphviz-2.50.0-win32"
Invoke-WebRequest "https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-win32.zip" -OutFile "python-3.10.11-embed-win32.zip"
Expand-Archive "python-3.10.11-embed-win32.zip" -DestinationPath "python"
Remove-Item -Path "./python-3.10.11-embed-win32.zip"
Invoke-WebRequest "https://bootstrap.pypa.io/get-pip.py" -OutFile "./python/get-pip.py"
./python/python.exe ./python/get-pip.py
$content=@"
python310.zip
.
Lib
Lib\site-packages
$(Get-Location)
"@
New-Item -ItemType File -Path ./python/python310._pth -Value $content -Force
./python/python.exe -m pip install -r requirements.txt