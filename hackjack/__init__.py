from flask import Flask
from flask.ext.mongoengine import MongoEngine
from pymongo import read_preferences
from mongoengine import connect


app = Flask(__name__)

mongolab_uri = environ.get('MONGOLAB_URI')
if mongolab_uri:
    url = urlparse.urlparse(mongolab_uri)
    self.app.config.setdefault('MONGODB_USER', url.username)
    self.app.config.setdefault('MONGODB_PASSWORD', url.password)
    self.app.config.setdefault('MONGODB_HOST', url.hostname)
    self.app.config.setdefault('MONGODB_PORT', url.port)
    self.app.config.setdefault('MONGODB_DB', url.path[1:])
# app.config["MONGODB_SETTINGS"] = {'read_preference': read_preferences.ReadPreference.PRIMARY}
# app.config["SECRET_KEY"] = "KeepThisS3cr3t"

# app.config["MONGODB_HOST"] = 'ds061691.mongolab.com'
# app.config["MONGODB_PORT"] = 61691
# app.config["MONGODB_USERNAME"] = 'heroku_app35754647'
# app.config["MONGODB_PASSWORD"] = 'im670d7fgb25cq1363ti2stguk'
# app.config["MONGODB_DB"] = 'heroku_app35754647'

db = MongoEngine(app)

if __name__ == '__main__':
    app.run()