from gwlib.base.base_service import BaseService
from gwlib.dao import BaseResourceDAO


class BaseResourceService(BaseService):

    def __init__(self):
        super().__init__()
        self.dao = BaseResourceDAO()

    def get_by_name(self, resource_name):
        return self.dao.get(name=resource_name)
