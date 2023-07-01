# foodify-django
django multi vendor food ecommerce project


# Dependency packages
- pip install python-decouple
- pip install simplejson
- pip install psycopg2
- pip install pillow

# Setup Process
- clone the project
- copy env-sample file and rename it to env and enter all the setup credentials
-  create virtual environment python -m venv environment-name (eg python -m venv env)
-  activate - ( & path/env/Scripts/Activate.ps1)  -- this will activate your virtual environment
-  in case of window (Set-ExecutionPolicy Unrestricted -Scope Process) execute this command before activating virtual env
-  install django and dependency packages
-  run (python manage.py runserver)
-  in case of error check the dependency to be installed and install them

# Setup database
- install postagres sql and pgadmin
- create a database
- setup the db credentials in env file
- run migration (python manage.py makemigrations) and (python manage.py migrate)
- if migration is successfull  create a superuser first( python manage.py createsuperuser)
- now you should be able to use the app
