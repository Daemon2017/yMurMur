#!/bin/bash
set -e
add-apt-repository ppa:deadsnakes/ppa -y
apt-get update
apt-get install -y \
    python3.8 \
    python3.8-distutils \
    python3-pip \
    python3-markupsafe
python3.8 -m pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    python3.8 -m pip install --no-cache-dir -r requirements.txt
else
    echo "requirements.txt not found, skipping pip install"
fi
rm -rf /var/lib/apt/lists/*
