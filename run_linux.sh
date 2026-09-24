#!/usr/bin/env bash
set -e
if [ ! -f venv/bin/python ]; then
  echo "Virtual environment not found. Run: python3 -m venv venv"
  exit 1
fi
source venv/bin/activate
python train_model.py
python run.py
