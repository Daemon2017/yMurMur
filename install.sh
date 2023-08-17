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
python3.8 -m pip install -r requirements.txt
wget -O murka-1.4.1-src.tar.gz https://master.dl.sourceforge.net/project/phylomurka/murka/murka-1.4.1/murka-1.4.1-src.tar.gz?viasf=1
tar -zxvf murka-1.4.1-src.tar.gz
rm murka-1.4.1-src.tar.gz
mv murka-1.4.1-src murka
cd murka || exit
./configure
make
