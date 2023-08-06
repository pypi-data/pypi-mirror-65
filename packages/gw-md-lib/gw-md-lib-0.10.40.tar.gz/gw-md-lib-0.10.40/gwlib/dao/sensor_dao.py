from gwlib.base.base_dao import BaseDAO
from gwlib.models import UserTypePolicy, Sensor


class BaseSensorDAO(BaseDAO):
    model = Sensor
