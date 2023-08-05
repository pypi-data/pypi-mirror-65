from sqlalchemy import func

from . import db


class Hole(db.Model):
    __tablename__ = "gw_hole"

    hole_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('gw_golf_course.course_id'))
    zone = db.Column(db.String(length=20), nullable=False)
    alias = db.Column(db.String(length=20), nullable=False)
    deleted = db.Column(db.Boolean, default=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now())

