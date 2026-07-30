@echo off
echo Starting BizLive Django Project...
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py makemigrations finance
python manage.py migrate
python manage.py runserver
pause
