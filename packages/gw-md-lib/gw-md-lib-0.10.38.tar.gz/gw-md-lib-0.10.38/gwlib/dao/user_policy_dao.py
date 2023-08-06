from gwlib.base.base_dao import BaseDAO
from gwlib.models import UserTypePolicy


class UserPolicyDAO(BaseDAO):
    model = UserTypePolicy

    def get_permissions_by_resource(self, type_id, resource_id):
        print("dao")
        user_type_policy = self.get(**{"type_id": type_id, "resource_id": resource_id})  # type: UserTypePolicy
        print("user", user_type_policy)
        return user_type_policy
