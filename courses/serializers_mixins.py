from rest_framework import serializers


class ProductTypeMixin(metaclass=serializers.SerializerMetaclass):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return obj._meta.model.__name__.lower()
