from gwlib.base.base_service import BaseService
from gwlib.dao.sensor_dao import BaseSensorDAO


class BaseSensorService(BaseService):

    def __init__(self):
        super().__init__()
        self.dao = BaseSensorDAO()
