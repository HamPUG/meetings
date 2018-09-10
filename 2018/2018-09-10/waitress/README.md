# Set up virtual environment

* initialize

  ```
  virtualenv -p /usr/bin/python3.5 venv
  ```

* install django and waitress

  ```
  venv/bin/pip install django waitress
  ```

# Create django example project

* Taken from here: 

  https://docs.djangoproject.com/en/2.1/intro/tutorial01/

* Generate project

  ```
  venv/bin/django-admin startproject mysite
  ```

* create *polls* app

  ```
  cd mysite
  ../venv/bin/python manage.py startapp polls
  ```

* add to `polls/views.py`

  ```python
  from django.http import HttpResponse


  def index(request):
      return HttpResponse("Hello, world. You're at the polls index.")  
  ```

* add code to `polls/urls.py`

  ```python
  from django.urls import path

  from . import views

  urlpatterns = [
      path('', views.index, name='index'),
  ]
  ```

* edit `mysite/urls.py`, add entry for *polls*, update imports (*import include*)

  ```python
  from django.contrib import admin
  from django.urls import include, path

  urlpatterns = [
      path('polls/', include('polls.urls')),
      path('admin/', admin.site.urls),
  ]  
  ```

* migrate database settings (we leave it at sqlite), from mysite directory

  ```
  ../venv/bin/python manage.py migrate  
  ```

* the following steps are used to have a data model that can be
  accessed via django's admin interface

* add view for polls

  ```python
  from django.db import models


  class Question(models.Model):
      question_text = models.CharField(max_length=200)
      pub_date = models.DateTimeField('date published')


  class Choice(models.Model):
      question = models.ForeignKey(Question, on_delete=models.CASCADE)
      choice_text = models.CharField(max_length=200)
      votes = models.IntegerField(default=0)
  
  ```

* add app to `mysite/settings.py`

  ```python
  INSTALLED_APPS = [
      'polls.apps.PollsConfig',
      ...
      ]
  ```

* update database

  ```
  ../venv/bin/python manage.py makemigrations polls
  ../venv/bin/python manage.py migrate
  ```

* make polls accessible in admin interface, edit `polls/admin.py`

  ```python
  from django.contrib import admin

  from .models import Question

  admin.site.register(Question)
  ```
  

* create admin user

  ```
  ../venv/bin/python manage.py createsuperuser
  ```

* run development server and open in browser (http://localhost:8000/polls/)

  ```
  ../venv/bin/python manage.py runserver
  ```

# Configure waitress

* based on this: 

  https://stackoverflow.com/questions/21081491/hosting-django-app-with-waitress#38943785

* create `server.py` in `mysite` directory

  ```python
  from waitress import serve

  from mysite.wsgi import application

  if __name__ == '__main__':
      serve(application, port='8000')  
  ```

* start server with 

  ```
  ../venv/bin/python server.py
  ```


# Moving to production

* during development, django can serve static files (`DEBUG=True` in settings.py),
  but this is considered insecure

* usually, you run django as WSGI application and let static files being 
  served by Apache or nginx

* Python alternative: [white-noise](http://whitenoise.evans.io/en/stable/)

  ```
  ../venv/bin/pip install whitenoise
  ```

* adapt your `settings.py`, adding the white-noise middleware after the `SecurityMiddleware`:

  ```python
  ...
  'django.middleware.security.SecurityMiddleware',
  'whitenoise.middleware.WhiteNoiseMiddleware',
  ...
  ```

* disable debugging in `settings.py`

  ```python
  DEBUG = False
  ```

* allow all hosts

  ```python
  ALLOWED_HOSTS = ['*']
  ```

* add root for static files in `settings.py`

  ```python
  STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
  ```

* collect static files

  ```
  ../venv/bin/python manage.py collectstatic
  ```


# Serving via https

* in an exposed system, you really don't want to use http

* use nginx as reverse proxy, taken from here: 

  https://www.digitalocean.com/community/tutorials/how-to-configure-nginx-with-ssl-as-a-reverse-proxy-for-jenkins

* nginx *waitress* configuration (`/etc/nginx/sites-available/waitress`)

  ```nginx
  server {
      listen 80;
      return 301 https://$host$request_uri;
  }

  server {
      listen 443;
      server_name localhost;

      ssl_certificate           /etc/nginx/cert.crt;
      ssl_certificate_key       /etc/nginx/cert.key;

      ssl on;
      ssl_session_cache  builtin:1000  shared:SSL:10m;
      ssl_protocols  TLSv1.2;
      ssl_ciphers HIGH:!aNULL:!eNULL:!EXPORT:!CAMELLIA:!DES:!MD5:!PSK:!RC4;
      ssl_prefer_server_ciphers on;

      location / {

        proxy_set_header        Host $host;
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header        X-Forwarded-Proto $scheme;

        # Fix the “It appears that your reverse proxy set up is broken" error.
        proxy_pass          http://localhost:8000;
        proxy_read_timeout  90;

        proxy_redirect      http://localhost:8000 https://localhost/;
      }

  }
  ```

# Bonus

* use [grip](http://github.com/joeyespo/grip) for rendering markdown via
  a mini webserver

* *grip* automatically refreshes the view if the file changes - handy for
  live editing/previewing

