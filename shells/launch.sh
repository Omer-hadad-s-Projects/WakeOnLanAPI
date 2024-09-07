source .venv/bin/activate

if [ -f .env ]; then
    export $(cat .env | xargs)
fi

gunicorn --workers 3 -b 0.0.0.0:$APP_PORT app:app
