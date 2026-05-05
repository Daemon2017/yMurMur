#!/bin/bash
set -e
chmod +x murka/murka
chmod +x murka/prepare/prepare
if [ -f "run.sh" ]; then
    chmod +x run.sh
fi
mkdir -p output logs data
find . -name "*.o" -type f -delete
echo "Final setup complete."
