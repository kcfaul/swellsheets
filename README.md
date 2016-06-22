# Set Up Environment
create your virtual env, and database.  In this example database is named conawaypay_dev but you can name it whatever you like

then run the following
```
export APP_SETTINGS=dev
export DATABASE_URL="postgresql://localhost/conawaypay_dev/"
python manage.py db init
python manage.py db migrate
python manage.py runserver
```
