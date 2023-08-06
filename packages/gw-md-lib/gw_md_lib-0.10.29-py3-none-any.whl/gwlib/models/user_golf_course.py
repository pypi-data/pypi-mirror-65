from sqlalchemy import Table

from . import db

user_golf_course = Table('gw_user_golf_course',
                         db.Model.metadata,
                         db.Column('course_id', db.Integer, db.ForeignKey('gw_golf_course.course_id'), nullable=False),
                         db.Column('user_id', db.Integer, db.ForeignKey('gw_user.user_id'), nullable=False),
                         db.Column('deleted', db.Boolean, default=False, nullable=False)
                         )
