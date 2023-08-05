import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # JWT CONF
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET')
    JWT_ALGORITHM = os.environ.get('JWT_SECRET', "RS256")
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)

    # DATABASE
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass