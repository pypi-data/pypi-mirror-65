from gwlib.base.base_dao import BaseDAO
from gwlib.base.errors import FieldRequired


class BaseService:
    required_fields = []

    def __init__(self):
        self.data = {}
        self.dao = BaseDAO()

    def validate(self):
        for key in self.required_fields:
            if key not in self.data:
                raise FieldRequired

    def __save(self):
        self.validate()
        self.before_save()
        response = self.dao.save(**self.data)
        self.after_save()
        return response

    def __update(self, data=None, filters=None):
        self.data = data
        return self.dao.update(data=self.data, **filters)

    def before_save(self):
        pass

    def after_save(self):
        pass

    def save(self, **data):
        self.data = data
        return self.__save()

    def update(self, **args):
        return self.__update(**args).to_json()

    def delete(self, **filters):
        return self.dao.delete(**filters)

    def filter(self, **filters):
        return self.dao.filter(**filters)
