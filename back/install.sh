#!/bin/sh
apt-get update
apt-get install software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa -y
apt-get update
apt-get install build-essential -y
apt-get install graphviz -y
apt-get install python3.8-distutils -y
apt-get install python3.8 -y
apt-get install python3-pip -y
apt-get install python3-markupsafe -y
apt-get install wget -y
python3.8 -m pip install -r requirements.txt
wget -O murka-1.4.1-src.tar.gz https://master.dl.sourceforge.net/project/phylomurka/murka/murka-1.4.1/murka-1.4.1-src.tar.gz?viasf=1
rm -rf murka
tar -zxvf murka-1.4.1-src.tar.gz
rm murka-1.4.1-src.tar.gz
mv murka-1.4.1-src murka
cd murka || exit
echo "42" > murka.rs
./configure
make
cd murka || exit
g++ -w -O2 -g0 -ldl -pthread -s -o murka murka.o nwerr.o args.o getopt.o misc.o nwclient_s.o nwclient_l.o nwclient.o nwst.o fformat.o
cd ..
make
cd prepare || exit
g++ -w -O2 -g0 -ldl -pthread -s ../murka/misc.o ../murka/getopt.o -o prepare prepare.o preperr.o prepargs.o convert.o
