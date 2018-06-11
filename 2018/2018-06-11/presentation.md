
class: middle, center
name: intro

```text
  ___________________        
< Cowsay as a Service >      
  -------------------        
         \   ^__^            
           \  (oo)\________    
              (__)\        )\/\
                 ||----w |  
               ||     ||
```




Andreas Löf

---

# Outline

1. Introduction to web services
2. Building a basic web service
3. Dockerising it
4. Deploying using Heroku
5. A Slack Application written in Flask

---



# What's a Web service?

* A service offered by an electronic device to another electronic device, using HTTP
* Supplies an API (SOAP, **REST**)
* Fundamental building blocks in a service based architecture

---

# REST (REpresentational State Transfer)

* Builds on top of HTTP
* Stateless operations
* URL driven
    * Uses HTTP Keywords (POST, GET, PUT, DELETE)
    * CRUD
    * Status Codes (2xx, 3xx 4xx, 5xx)
* Content negotiation
    * **JSON**
    * XML

???

2xx - Success
200 - Ok
201 - Created
202 - Accepted

3xx - Redirects

4xx - User error
400 - Bad Request
401 - Unauthorized
404 - Not found
405 - Method not allowed
409 - Conflict

5xx - Server Error



---

# HTTP Request

```http
GET /say/hello HTTP/1.1
Host: cowsay.io
User-Agent: Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Upgrade-Insecure-Requests: 1
DNT: 1
Cache-Control: max-age=0
```
---

# HTTP Response

```http
HTTP/1.1 200 OK
Connection: keep-alive
Server: gunicorn/19.8.1
Date: Sat, 09 Jun 2018 00:38:54 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 1140
Via: 1.1 vegur

<!DOCTYPE html>
<html>
snip!
</html>

```

---

# Building the Simplest Web Service in Flask


* Flask
    * Lightweight
    * Web applications or services
    * Jinja2 templates
    * Lots of examples
    * Python 2 and 3
* pip3 install Flask

Hello world:
 ```python
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run()
```

---

# Adding Content Negotiation

pip3 install flask-accept

```python
from flask import Flask, jsonify
from flask_accept import accept
app = Flask(__name__)

@app.route('/')
@accept('text/html')
def hello_world():
    return 'Hello World!'

@hello_world.support('application/json')
def hello_world_json():
    return jsonify(result="Hello World!")

if __name__ == '__main__':
    app.run()
```
---

class: center, middle

# Cowsay Codebase

https://github.com/aginor/cowsay-as-a-service

---

class: center, middle

# Content Negotiation Demo

---

# Production Environments

* **Flask's built in server is not production grade**
* **Make sure the Flask debugger is disabled**
* **Manage credentials and secret keys securely**
* Serve static content from a proper webserver
    * No need to waste extra CPU-cycles in Flask
    * Apache or nginx will do it much more efficiently
* WSGI interfaces
    * Gunicorn
    * uwsgi
    * mod_wsgi (Apache)
* Deployment options
    * Virtual environments
    * Docker containers

---

class: center, middle

# Never Commit a Key or Password


---
#Docker

* Containerises applications
    * Not a VM!
* Allows for shipping of application with dependencies
* Separate the application from the system and vice-versa
* Relies on kernel namespaces and control groups for security


```dockerfile
# For debugging, gives 1 GB image
FROM python:3.6 
# For smaller images, ~ 90MB
#FROM python:3.6-alpine 

COPY requirements.txt /
RUN pip3 install --no-cache-dir -r /requirements.txt

COPY cowsay /cowsay
WORKDIR /
EXPOSE 8000

CMD gunicorn cowsay.app:app --bind=0.0.0.0 --workers=1 --log-file -
```

---

# cowsay.io setup

* Heroku for web hosting
    * Free plan
* Cloudflare for DNS hosting
    * Could use caching but haven't enabled it
    * Supports rootless domains
    * Free plan

---

# Deploying on Heroku

* Platform as a Service (PaaS)
    * One of the first if not the first
    * Runs on top of AWS (ie, more expensive than plain AWS)
    

* Comes with cli-tool for managing the application
* Deploy by pushing to a git remote

```bash
git push heroku master
```

---

class: center, middle

# Slack Application Consuming cowsay.io

https://github.com/aginor/cowbot

---

# Further Reading:

* http://flask.pocoo.org/
* https://pypi.org/project/flask_accept/
* https://gist.github.com/alexserver/2fcc26f7e1ebcfc9f6d8
* https://devcenter.heroku.com/start