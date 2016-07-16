#!/bin/bash
export APP_SETTINGS=dev
export DATABASE_URL="postgresql://postgres@localhost/conawaypay_dev"
python manage.py db init
python manage.py db migrate
