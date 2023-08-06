from congressy.core import synchable_models as models
from congressy.core.models import fields


class Namespace(models.SynchableModel):
    class Meta(models.SynchableModel.Meta):
        list_endpoint = '/v1/videos/namespaces'
        create_endpoint = '/v1/videos/namespaces'
        item_endpoint = '/v1/videos/namespaces/{pk}'

    uuid = fields.UUIDField(
        label='ID',
        primary_key=True,
    )
    name = fields.StringField(
        label='name',
        required=True,
        max_length=100,
    )
    slug = fields.StringField(
        label='slug',
        required=True,
        max_length=255,
    )
    user = fields.IntegerField(
        label='user ID',
        required=False,
    )
    external_id = fields.StringField(
        label='external ID',
        required=True,
        max_length=255,
    )
    created_at = fields.DateTimeField(
        label='created at',
        required=False,
    )
    updated_at = fields.DateTimeField(
        label='updated fields',
        required=False,
    )
