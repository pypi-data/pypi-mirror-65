from gwlib.base.base_service import BaseService
from gwlib.dao.user_policy_dao import UserPolicyDAO
from gwlib.services.base_resource import BaseResourceService


class BasePolicyService(BaseService):

    def __init__(self):
        super().__init__()
        self.dao = UserPolicyDAO()

    def get_policy(self, resource_id, type_id):
        return self.dao.get(resource_id=resource_id, type_id=type_id)

    def get_resource_permissions(self, type_id, resource_name):
        resource_service = BaseResourceService()
        resource = resource_service.get_by_name(resource_name=resource_name)
        print("aqui resource perm", resource)
        return self.dao.get_permissions_by_resource(type_id=type_id,
                                                    resource_id=resource.resource_id).to_json()







