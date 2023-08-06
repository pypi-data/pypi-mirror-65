from gwlib.base.base_dao import BaseDAO
from gwlib.models import User


class BaseUserDAO(BaseDAO):
    model = User

