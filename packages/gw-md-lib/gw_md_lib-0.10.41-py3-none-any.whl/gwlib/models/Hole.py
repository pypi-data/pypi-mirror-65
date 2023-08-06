from sqlalchemy import func
from sqlalchemy.orm import relationship

from gwlib.models import ModelJson
from . import db


class Hole(db.Model, ModelJson):
    __tablename__ = "gw_hole"

    hole_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('gw_golf_course.course_id'), nullable=False)
    zone = db.Column(db.String(length=20), nullable=True)
    name = db.Column(db.String(length=20), nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    golf_course = relationship("GolfCourse")
    sensors = relationship("Sensor", lazy='dynamic')
