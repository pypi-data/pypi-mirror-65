import datetime
import os

from . import default


class Config(default.Config):
    """
        development config
    """
    DEBUG = True
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=15)
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(
        os.environ.get('MYSQL_USER', "groundworx"),
        os.environ.get('MYSQL_PASS', "groundworx"),
        os.environ.get('MYSQL_HOST', "mysql"),
        os.environ.get('MYSQL_DB', "groundworx"),
    )

