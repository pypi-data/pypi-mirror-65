from sqlalchemy import func

from gwlib.models import db
from .model_json import ModelJson


class Resource(db.Model, ModelJson):
    __tablename__ = "gw_resource"

    resource_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now())
