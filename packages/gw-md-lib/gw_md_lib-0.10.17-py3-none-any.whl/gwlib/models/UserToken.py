from sqlalchemy import func

from . import db


class UserToken(db.Model):
    __tablename__ = "gw_user_token"

    token_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('gw_user.user_id'))
    token = db.Column(db.String(length=40), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
