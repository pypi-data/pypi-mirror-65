from gwlib.base.base_service import BaseService
from gwlib.dao.holes_dao import BaseHolesDAO


class BaseHolesService(BaseService):

    def __init__(self):
        super().__init__()
        self.dao = BaseHolesDAO()

    def get_by_name(self, resource_name):
        return self.dao.get(name=resource_name)
