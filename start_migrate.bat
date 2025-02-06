@echo off
python manage.py wait_for_db
python manage.py migrate