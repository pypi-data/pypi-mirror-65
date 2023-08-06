"""Declares :class:`RealmConfigSchema`."""
import marshmallow
from unimatrix.lib.datastructures import DTO


class RealmSingleSignonSchema(marshmallow.Schema):
    dict_class = DTO

    providers = marshmallow.fields.Field(
        missing=dict,
        default=dict
    )


class RealmConfigSchema(marshmallow.Schema):
    dict_class = DTO

    public = marshmallow.fields.Boolean(
        missing=False,
        default=False
    )

    domains = marshmallow.fields.List(
        marshmallow.fields.String,
        missing=list,
        default=list
    )

    sso = marshmallow.fields.Nested(
        RealmSingleSignonSchema,
        missing=lambda: RealmSingleSignonSchema().load({}),
        default=lambda: RealmSingleSignonSchema().load({})
    )
