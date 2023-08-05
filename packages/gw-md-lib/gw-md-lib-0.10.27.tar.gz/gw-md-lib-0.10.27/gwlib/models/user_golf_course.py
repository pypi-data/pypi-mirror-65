from sqlalchemy import Table

from . import db

user_golf_course = Table('gw_user_golf_course',
                         db.Model.metadata,
                         db.Column('course_id', db.Integer, db.ForeignKey('gw_golf_course.course_id')),
                         db.Column('user_id', db.Integer, db.ForeignKey('gw_user.user_id')),
                         db.Column('deleted', db.Boolean)
                         )
