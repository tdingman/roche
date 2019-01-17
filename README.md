# roche
Web app for asynchronous roching

# Start from the beginning
* Set up DigitalOcean server
* Create user
* Set up ssh keys
* Install Python + PIP

# Booting up
* If it doesn't exist already: `pyvenv roche_env`
* `source roche_env/bin/active`
* (`deactivate` to escape)

# Starting Django
* Make sure to add `0.0.0.0` and your domain to `ALLOWED_HOSTS` in `settings.py`
* `python manage.py runserver 0:8000`
