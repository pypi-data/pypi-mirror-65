from gwlib.base.base_service import BaseService
from gwlib.dao.golf_course_dao import BaseGolfCourseDAO
from gwlib.models import GolfCourse


class BaseGolfCourseService(BaseService):
    required_fields = ["email"]

    def __init__(self):
        super().__init__()
        self.dao = BaseGolfCourseDAO()

    def get_obj_by_id(self, golf_course_id):
        filters = {
            "course_id": golf_course_id
        }
        return self.dao.get(**filters)

    def get_users(self, course_id):
        golf_course = self.get_obj_by_id(course_id)  # type: GolfCourse
        return golf_course.users
