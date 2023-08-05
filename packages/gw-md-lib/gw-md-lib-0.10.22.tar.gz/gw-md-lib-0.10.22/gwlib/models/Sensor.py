from sqlalchemy import func

from . import db


class Sensor(db.Model):
    __tablename__ = "gw_sensor"

    sensor_id = db.Column(db.Integer, primary_key=True)
    hole_id = db.Column(db.Integer, db.ForeignKey('gw_hole.hole_id'))
    MEID = db.Column(db.String(length=18), nullable=False)
    serial_number = db.Column(db.String(length=18), nullable=False)
    latitude = db.Column(db.DECIMAL(13, 10), nullable=True)
    longitude = db.Column(db.DECIMAL(13, 10), nullable=True)
    status = db.Column(db.String(10))
    alias = db.Column(db.String(20))
    deleted = db.Column(db.Boolean, default=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now())

