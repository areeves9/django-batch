# django-auth-bootstrap4
A simple Django project comprised of a single custom authentication app, Accounts, to be used for any app requiring user email based authentication.

# Project Background
I wanted a reusable auth app that used the default Django authentication backend but with a custom auth user model, SiteUser, 
with email set to username. 

The Accounts app also contain custom views, such as an Activate view with will send a newly registered user an 
activation URL via email. 

Some of the default auth_views from django.contrib.auth have been overriden and have a new url in Accounts. 

The Forms Django provides in django.contrib.auth have also been overriden for styling and functional purposes.

# Code Style
This project attempts to adhere to the requirements of PEP8 and was developed with flake8 styling linter installed in the code editior.

# Tech/Frameworks
* Django
* PostgreSQL
* Flake8
* Pytest-Django
* Mixer
* Bootstrap4
* Django-Crispy-Forms
* Conda

# Quick Start
1. Clone or download the repo.
2. Install package dependencies localted in requirements.txt or package-list.txt.
3. Run python manage.py makemigrations.
4. Run python manage.py migrate.
