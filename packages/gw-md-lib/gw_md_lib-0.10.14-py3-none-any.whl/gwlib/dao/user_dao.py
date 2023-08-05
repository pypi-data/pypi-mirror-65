from gwlib.base.base_dao import BaseDAO
from gwlib.models import User


class UserDAO(BaseDAO):
    model = User

    def save(self, **data):
        password = data.pop("password")
        model = self.model(**data)
        model.set_password(password)
        self.session.add(model)
        self.session.commit()
        return model.to_json()

