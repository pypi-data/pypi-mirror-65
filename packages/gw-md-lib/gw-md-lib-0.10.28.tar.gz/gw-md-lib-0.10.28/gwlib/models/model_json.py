import datetime
import inspect
from inspect import getmembers

from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.util import NoneType


class ModelJson:
    not_show = ["password", "resource_id", "type_id"]
    extras = []

    def keys(self):
        return [i for i in self.__dict__.keys() if i[:1] != '_']

    def __getitem__(self, key):
        return dict(zip("abc", "one two three".split()))[key]

    def _get_foreign_keys(self):
        return list(self.__table__.foreign_keys)

    def get_column_type(self, name):
        return getattr(getattr(self.__table__.columns, name), "type")

    @property
    def columns(self):
        columns = [column.name for column in self.__table__.columns]
        columns.extend(self.extras)
        return columns

    def get_methods_not_allowed(self):
        members = getmembers(self, predicate=inspect.ismethod)
        if members:
            member_names = [member[0] for member in members]
            return member_names

    def _validates(self, data):
        from . import UserTypePolicy, UserType, Resource
        from sqlalchemy_utils.types.choice import Choice
        if type(data) == Choice:
            new_obj = {"code": data.code, "value": data.value}
            data = new_obj
        elif type(data) is InstrumentedList:
            new_data = []
            for obj in data:
                new_data.append(self._validates(obj))
            data = new_data
        elif str(type(data)) == "<class 'sqlalchemy.orm.dynamic.AppenderBaseQuery'>":
            new_data = []
            for obj in data:
                new_data.append(self._validates(obj))
            data = new_data
        elif type(data) in (UserTypePolicy, UserType, Resource):
            if hasattr(data, "uuid"):
                data = data.uuid
            else:
                data = self._validates(data.to_json())
        elif type(data) in [datetime.time]:
            data = data.strftime("%H:%M:%S")
        elif type(data) is dict:
            new_data = {}
            for key, value in data.items():
                new_data[key] = self._validates(value)
            data = new_data
        elif type(data) not in (str, int, dict, list, bool, NoneType):
            data = str(data)
        return data

    def to_json(self):
        obj = {}
        for key in [i for i in dir(self) if i[:1] != '_' and i not in self.not_show and
                                            i not in self.get_methods_not_allowed() and i in self.columns]:
            data = getattr(self, key)
            obj[key] = self._validates(data)

        return obj
