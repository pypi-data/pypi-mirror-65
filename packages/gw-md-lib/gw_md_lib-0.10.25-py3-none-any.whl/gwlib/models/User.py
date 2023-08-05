from sqlalchemy import func
from sqlalchemy.orm import relationship

from gwlib.utils.helper import Helper
from . import db, user_golf_course
from .model_json import ModelJson


class User(db.Model, ModelJson):
    __tablename__ = "gw_user"

    user_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('gw_user_type.type_id'))
    name = db.Column(db.String(length=50), nullable=False)
    last_name = db.Column(db.String(length=50), nullable=False)
    email = db.Column(db.String(length=100), nullable=False, unique=True)
    password = db.Column(db.String(length=100), nullable=False)
    phone = db.Column(db.String(length=13), nullable=False)
    status = db.Column(db.String(length=10), nullable=False)
    logo_url = db.Column(db.String(length=250))
    deleted = db.Column(db.Boolean, default=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now())

    golf_courses = db.relationship(
        "User",
        secondary=user_golf_course,
        passive_deletes=True,
        backref="golf_course_user")

    user_type = relationship("UserType", back_populates="users")

    def validate_password(self, password):
        print("valida pass")
        return Helper.verify_crypt(password, self.password)

    def set_password(self, passowrd):
        self.password = Helper.set_crypt(passowrd)
