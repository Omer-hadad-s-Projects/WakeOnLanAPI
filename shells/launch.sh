if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Increase worker timeout to 60 seconds to handle long-running wake operations
gunicorn --workers 3 --timeout 60 -b 0.0.0.0:$APP_PORT app:app
