from sqlalchemy import func

from . import db


class Report(db.Model):
    __tablename__ = "gw_report"

    course_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    deleted = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('gw_user.user_id'))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now())

