import os

class Config(object):
    SECRET_KEY=os.environ.get("SECRET_KEY") or "secret_string"
    MONGODB_SETTINGS = { 'db' : 'MY_BANK' ,'host' : os.environ["DB_PORT_27017_TCP_ADDR"] , 'port': 27017}
