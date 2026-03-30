#!/bin/bash

echo "Downloading latest SOB..."
curl -L -o sob.zip https://github.com/TAMAGO55123/SOB/releases/latest/download/sob.zip

echo "Extracting..."
unzip -o sob.zip

echo "Python Package Installing..."
python -m pip install -r requirements.txt

echo "Starting bot..."
python main.py
