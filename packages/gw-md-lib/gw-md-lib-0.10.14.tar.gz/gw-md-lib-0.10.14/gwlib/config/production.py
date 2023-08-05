import datetime

from . import default


class Config(default.Config):
    """
        production config
    """
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)
    SQLALCHEMY_DATABASE_URI = "mysql://admin:groundworx@database-2.cm3atlknp5l3.us-east-1.rds.amazonaws.com/groundworx"
