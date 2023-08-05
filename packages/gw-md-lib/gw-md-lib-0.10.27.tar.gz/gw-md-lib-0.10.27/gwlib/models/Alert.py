from sqlalchemy import func

from . import db


class AlertType(db.Model):
    __tablename__ = "gw_alert_type"

    type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)


class Alert(db.Model):
    __tablename__ = "gw_alert"

    course_id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('gw_sensor.sensor_id'))
    type_id = db.Column(db.Integer, db.ForeignKey('gw_alert_type.type_id'))
    title = db.Column(db.String(length=100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    threshold = db.Column(db.Text, nullable=False)
    deleted = db.Column(db.Boolean, default=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now())
