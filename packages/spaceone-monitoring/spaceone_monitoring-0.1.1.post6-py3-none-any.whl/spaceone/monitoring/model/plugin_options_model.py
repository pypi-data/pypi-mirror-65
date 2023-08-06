import jsonschema
from schematics.models import Model
from schematics.exceptions import ValidationError
from schematics.types import BaseType, ListType, DictType, StringType
from schematics.types.compound import ModelType

__all__ = ['MetricPluginOptionsModel', 'LogPluginOptionsModel']

_SUPPORTED_RESOURCE_TYPE = [
    'inventory.Server',
    'inventory.CloudService'
]


class JSONSchemaType(BaseType):
    def validate_netloc(self, value):
        try:
            jsonschema.Draft7Validator.check_schema(value)
        except Exception as e:
            raise ValidationError(key=f'Plugin option is invalid. (filter_format = {str(value)}')


class ReferenceKeyModel(Model):
    resource_type = StringType(required=True, choices=_SUPPORTED_RESOURCE_TYPE)
    reference_key = StringType(required=True)


class DynamicViewField(Model):
    name = StringType(required=True)
    key = StringType(required=True)
    view_type = StringType()
    view_option = DictType(StringType)


class MetricPluginOptionsModel(Model):
    supported_resource_type = ListType(StringType(choices=_SUPPORTED_RESOURCE_TYPE), required=True)
    reference_keys = ListType(ModelType(ReferenceKeyModel))


class LogPluginOptionsModel(Model):
    supported_resource_type = ListType(StringType(choices=_SUPPORTED_RESOURCE_TYPE), required=True)
    reference_keys = ListType(ModelType(ReferenceKeyModel))
    filter_format = JSONSchemaType()
    data_source = ListType(ModelType(DynamicViewField))
