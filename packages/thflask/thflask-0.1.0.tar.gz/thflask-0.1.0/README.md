# Flask Application

A simple Flask Restful application that is using flask and flask-restful for creating the APIs and uWSGI as web server

## Requirements

* python >= 3.7
* pip3.7

## Install and run
### 1. Github
```
# Download the repository
git clone https://github.com/themisAnagno/th-flask.git
cd th-flask
# Install required modules and binaries
pip install .
# Run the application
thflask
```

### 2. PyPI
* Install from PyPI
```
pip install thflask
```
* Create the `uwsgi.ini` file:
```
[uwsgi]
http-socket = :$(PORT)
stats = :$(STATSPORT)
master = true
die-on-term = true
module = thflask.app:app
memory-report = true
```
* Run the application:
`uwsgi uwsgi.ini`
