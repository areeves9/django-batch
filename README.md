# django-auth-bootstrap4
A simple Django project comprised of a single custom authentication app, Accounts, to be used for any app requiring user email based authentication.

# Why This Project Exist
The idea is I wanted a reusable auth app that used the default Django authentication backend but with a custom auth user model, SiteUser, 
with email set to username. The Accounts app also contain custom views, such as an Activate view with will send a newly registered user an 
activation URL via email. The Forms Django provides in django.contrib.auth have also been overriden for styling and functional purposes.

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
