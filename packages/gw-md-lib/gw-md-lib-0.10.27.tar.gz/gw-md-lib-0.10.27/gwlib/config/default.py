import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # JWT CONF
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET', "039urfjd9sf8usdf9ijdsf;lsdlf23/;el23p")
    JWT_ALGORITHM = "HS256"
    MYSQL_DB = os.environ.get('MYSQL_DB', "db")
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    # DATABASE
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass