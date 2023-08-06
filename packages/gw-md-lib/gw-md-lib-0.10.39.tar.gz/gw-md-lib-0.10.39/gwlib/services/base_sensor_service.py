from gwlib.base.base_service import BaseService
from gwlib.dao.sensor_dao import BaseSensorDAO


class BaseSensorService(BaseService):

    def __init__(self):
        super().__init__()
        self.dao = BaseSensorDAO()

    def get_by_sensor_id(self, sensor_id):
        return self.dao.get(sensor_id=sensor_id).to_json()
