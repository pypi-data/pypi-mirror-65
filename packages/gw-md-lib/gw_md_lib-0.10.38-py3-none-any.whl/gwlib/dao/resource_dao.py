from gwlib.base.base_dao import BaseDAO
from gwlib.models import Resource


class BaseResourceDAO(BaseDAO):
    model = Resource
