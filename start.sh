# Activate the virtual environment if applicable
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Navigate to your Django project directory
cd /

# Run migrations
echo "Applying migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the server with gunicorn
echo "Starting the server..."
gunicorn api.wsgi:application --bind 0.0.0.0:$PORT

# If you want to run the Django development server instead, uncomment the following line:
# python manage.py runserver 0.0.0.0:$PORT