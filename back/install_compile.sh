#!/bin/bash
set -e
wget -O murka-1.4.1-src.tar.gz https://master.dl.sourceforge.net/project/phylomurka/murka/murka-1.4.1/murka-1.4.1-src.tar.gz?viasf=1
rm -rf murka
tar -zxvf murka-1.4.1-src.tar.gz
rm murka-1.4.1-src.tar.gz
mv murka-1.4.1-src murka
cd murka || exit
echo "42" > murka.rs
./configure
make -j$(nproc) || true
cd murka || exit
g++ -w -O2 -g0 -s -o murka murka.o nwerr.o args.o getopt.o misc.o nwclient_s.o nwclient_l.o nwclient.o nwst.o fformat.o -pthread -ldl
cd ..
make -j$(nproc) || true
cd prepare || exit
g++ -w -O2 -g0 -s ../murka/misc.o ../murka/getopt.o -o prepare prepare.o preperr.o prepargs.o convert.o -pthread -ldl
cd ../..
