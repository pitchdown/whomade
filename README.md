whomade is a web-based application that challenges users to guess the artist who created an album based on its cover art.

To get the application up and running, follow these steps:

Start the Backend Server:

```bash
python manage.py runserver
```

Start the Celery Worker:

```bash
celery -A whomade worker --loglevel=info
```

Start the Redis Server:

```bash
redis-server
```

You can also fetch album data directly from the Spotify API and save it to your database.

Note: Make sure you're logged in and have a valid Spotify API token before running the command.

```bash
python manage.py fetch_data
```
