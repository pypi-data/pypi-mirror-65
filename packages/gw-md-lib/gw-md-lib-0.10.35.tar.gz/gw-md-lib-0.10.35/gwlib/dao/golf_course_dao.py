from gwlib.base.base_dao import BaseDAO
from gwlib.models import GolfCourse


class BaseGolfCourseDAO(BaseDAO):
    model = GolfCourse

