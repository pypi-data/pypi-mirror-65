from sqlalchemy import func

from gwlib.models.user_golf_course import user_golf_course
from . import db


class GolfCourse(db.Model):
    __tablename__ = "gw_golf_course"

    course_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    email = db.Column(db.String(length=100), nullable=False)
    website = db.Column(db.String(length=250), nullable=True)
    deleted = db.Column(db.Boolean, default=False)
    logo_url = db.Column(db.String(length=250))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now())

    users = db.relationship(
        "User",
        secondary=user_golf_course,
        passive_deletes=True,
        backref="user_golf_course")