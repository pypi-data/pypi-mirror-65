from gwlib.dao import BaseUserDAO
from gwlib.base.base_service import BaseService


class BaseUserService(BaseService):

    def __init__(self):
        super().__init__()
        self.dao = BaseUserDAO()

    def get_by_user_id(self, user_id):
        return self.dao.get(user_id=user_id)

    def get_by_username(self, username):
        return self.dao.get(username=username)
