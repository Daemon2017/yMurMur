Invoke-WebRequest "https://master.dl.sourceforge.net/project/phylomurka/murka/murka-1.4.1/murka-1.4.1-win64.zip?viasf=1" -OutFile "murka-1.4.1-win64.zip"
Expand-Archive "murka-1.4.1-win64.zip" -DestinationPath "murka-1.4.1-win64"
Move-Item -Path "./murka-1.4.1-win64/murka-1.4.1-win64" -Destination "./murka" -force
Remove-Item -Path "./murka-1.4.1-win64.zip"
Remove-Item -Path "./murka-1.4.1-win64"