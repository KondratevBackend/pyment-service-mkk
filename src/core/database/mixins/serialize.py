class SerializeMixin:
    """Mixin to make model serializable."""

    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}
