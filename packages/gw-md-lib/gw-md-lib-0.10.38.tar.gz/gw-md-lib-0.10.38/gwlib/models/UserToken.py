from sqlalchemy import func
from sqlalchemy.orm import relationship

from gwlib.models import ModelJson
from . import db


class UserToken(db.Model, ModelJson):
    __tablename__ = "gw_user_token"

    token_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('gw_user.user_id'), nullable=False)
    token = db.Column(db.String(length=40), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
