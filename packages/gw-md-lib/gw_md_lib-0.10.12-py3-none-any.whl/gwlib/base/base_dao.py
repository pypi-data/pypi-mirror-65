from sqlalchemy.orm import Query
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from gwlib.base.errors import FieldNotInModel
from gwlib.utils.helper import Helper


class BaseDAO:
    include_logical_deleted = False
    model = None

    def __init__(self):
        from gwlib.models import db
        self.session = db.session

    def change_model(self, model):
        self.model = model

    @property
    def queryset(self):
        """

        :rtype: Query
        """
        if not self.include_logical_deleted:
            return self.model.query.filter_by(deleted=False)
        else:
            return self.model.query

    def save(self, **data):
        model = self.model(**data)
        self.session.add(model)
        self.session.commit()
        return model.to_json()

    def __get(self, filters):
        try:
            query = self.queryset.filter_by(**filters)
            obj = query.one_or_none()
            if obj is None:
                raise NoResultFound

        except MultipleResultsFound:
            raise MultipleResultsFound
        return obj

    def update(self, data=None, **filters):
        print("filters", filters)
        obj = self.__get(filters)
        for field, value in data.items():
            if field == "password":
                value = Helper.set_crypt(value)
            if hasattr(obj, field):
                setattr(obj, field, value)
            else:
                raise FieldNotInModel(field, {})

        self.session.commit()
        return obj.to_json()

    def delete(self, **filters):
        obj = self.__get(**filters)
        if hasattr(obj, "deleted"):
            obj.deleted = True
        self.session.commit()
        return obj.to_json()

    def filter(self, **filters):
        query = self.queryset.filter_by(**filters)
        return query.all()

    def get(self, **filters):
        return self.__get(**filters).to_json()
