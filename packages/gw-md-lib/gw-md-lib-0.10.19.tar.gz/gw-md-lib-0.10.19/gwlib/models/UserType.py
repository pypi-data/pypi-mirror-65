from sqlalchemy.orm import relationship

from .model_json import ModelJson
from . import db


class UserType(db.Model, ModelJson):
    __tablename__ = "gw_user_type"

    type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)

    users = relationship("User", back_populates="user_type")
    user_types_policies = relationship("UserTypePolicy")

