#!/bin/bash

echo "Downloading latest SOB..."
curl -L -o sob.zip https://github.com/TAMAGO55123/SOB/releases/latest/download/sob.zip

echo "Downloading notupdate list..."
curl -L -o notupdate.txt https://github.com/TAMAGO55123/SOB/releases/latest/download/notupdate.txt

echo "Building exclude list..."
EXCLUDES=""
while IFS= read -r line; do
    # 空行やコメント(#)は無視
    if [[ -n "$line" && ! "$line" =~ ^# ]]; then
        EXCLUDES="$EXCLUDES --exclude='$line'"
    fi
done < notupdate.txt

echo "Extracting ZIP to temp folder..."
rm -rf _update_temp
mkdir _update_temp
unzip sob.zip -d _update_temp

echo "Copying files (excluding listed files)..."
eval rsync -av $EXCLUDES _update_temp/SOB-main/ ./

echo "Python Package Installing..."
python -m pip install -r requirements.txt

echo "Starting bot..."
python3 main.py
