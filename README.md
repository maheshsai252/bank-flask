# bank-flask using flask bootstrap mongodb

A basic flask web application which can perform all bank operations.


To run without docker :

change config.py to

import os

class Config(object):
    SECRET_KEY=os.environ.get("SECRET_KEY") or "secret_string"
    MONGODB_SETTINGS = { 'db' : 'MY_BANK'}


clone or download

cd <dir>

source tcs/bin/activate

flask run



#open another terminal to start mongo server

mongod



or

docker-compose build

docker-compose up
