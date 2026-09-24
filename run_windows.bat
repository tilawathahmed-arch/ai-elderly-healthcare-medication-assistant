@echo off
setlocal
if not exist venv\Scripts\python.exe (
  echo Virtual environment not found. Run: python -m venv venv
  exit /b 1
)
call venv\Scripts\activate.bat
python train_model.py
python run.py
