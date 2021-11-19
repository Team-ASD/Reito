# release: python script_duplicados.py
release: python manage.py makemigrations viajes reservas usuarios vehiculos
release: python manage.py migrate
# release: python script_destinos.py


web: gunicorn reito.wsgi --log-file -