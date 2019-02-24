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

# Adding packages
* Note: install these while in the venv!
* python-decouple
* django-sendgrid-v5

# Starting Django
* Make sure to add `0.0.0.0` and your domain to `ALLOWED_HOSTS` in `settings.py`
* `python manage.py runserver 0:8000

# Editing Django settings
* Set time zone in `roche/settings.py`
* Create admin (`python manage.py createsuperuser`)
* Add environment variables to .env in root directory
* Edit settings.py to change or add environment variables: LOGIN_REDIRECT_URL, EMAIL_BACKEND, SENDGRID_API_KEY, DEFAULT_FROM_EMAIL

# Adding apps
* Add to `INSTALLED_APPS` in the `settings.py` file for the project (not any one of the apps)

# django-twilio
* Need to `pip install` two other packages: `phonenumbers` and `wheel`
* Add `export TWILIO_ACCOUNT_SID=xxx` and `export TWILIO_AUTH_TOKEN=yyy` to `/bin/activate.sh` of the virtual environment (while in the virtual environment)
