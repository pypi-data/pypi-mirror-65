from sqlalchemy import func
from sqlalchemy.orm import relationship

from gwlib.models import db
from .model_json import ModelJson


class UserTypePolicy(db.Model, ModelJson):
    __tablename__ = "gw_user_type_policy"

    policy_id = db.Column(db.Integer, primary_key=True)
    user_type_id = db.Column(db.Integer, db.ForeignKey('gw_user_type.type_id'))
    resource_id = db.Column(db.Integer, db.ForeignKey('gw_resource.resource_id'))
    can_create = db.Column(db.Boolean, default=False)
    can_read = db.Column(db.Boolean, default=False)
    can_update = db.Column(db.Boolean, default=False)
    can_delete = db.Column(db.Boolean, default=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now())

    resource = relationship("Resource")
