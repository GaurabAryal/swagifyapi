Make sure you export these two env vars:

```
export SECRET_KEY="foobar"
export DATABASE_URL="postgresql://localhost/swagify"
```

To run the api server, use the following command:

```
python manage.py runserver
```


To perform DB migrations:

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
