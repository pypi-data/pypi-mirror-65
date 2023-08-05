from gwlib.base.base_dao import BaseDAO
from gwlib.models import User, Resource


class UserDAO(BaseDAO):
    model = User

    def save(self, **data):
        password = data.pop("password")
        model = self.model(**data)
        model.set_password(password)
        self.session.add(model)
        self.session.commit()
        return model.to_json()

    def get_permissions_by_resource(self, user_id, resource):
        user = self.get(**{"user_id": user_id})
        resource = {
            "name": resource
        }
        self.model = Resource
        resource_obj = self.get(**resource)
        resource_policies = user.get_permission_by_resource(resource_obj)
        return resource_policies
