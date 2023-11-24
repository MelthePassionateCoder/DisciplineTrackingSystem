@echo off
set DJANGO_SETTINGS_MODULE=lumbiaNHS_2.settings
project_lnhs\Scripts\gunicorn lumbiaNHS_2.wsgi:application -b 0.0.0.0:8000