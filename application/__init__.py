from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
#create flask app
app = Flask(__name__)
app.config.from_object(Config)
#create mongo database
db = MongoEngine()
db.init_app(app)

from application import routes
