import datetime


class SerializeMixin:
    """Mixin to make model serializable."""

    def to_dict(self):
        def normalize(value):
            if isinstance(value, (datetime.datetime, datetime.date)):
                return value.isoformat()
            return value

        return {field.name: normalize(getattr(self, field.name)) for field in self.__table__.c}
