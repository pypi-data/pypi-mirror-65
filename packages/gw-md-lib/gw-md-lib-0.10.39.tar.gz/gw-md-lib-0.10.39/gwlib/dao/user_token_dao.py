from gwlib.base.base_dao import BaseDAO
from gwlib.models import UserToken


class BaseUserTokenDAO(BaseDAO):
    model = UserToken
