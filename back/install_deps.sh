#!/bin/bash
set -e
apt-get update
apt-get install -y \
    software-properties-common \
    build-essential \
    graphviz \
    wget \
    curl \
    git
rm -rf /var/lib/apt/lists/*
