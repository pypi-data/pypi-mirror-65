from congressy.core import synchable_models as models
from congressy.core.models import fields


class Subscriber(models.SynchableModel):
    class Meta(models.SynchableModel.Meta):
        list_endpoint = '/v1/videos/subscribers'
        create_endpoint = list_endpoint
        item_endpoint = '/v1/videos/subscribers/{pk}'

    uuid = fields.UUIDField(
        label='ID',
        primary_key=True,
    )
    project = fields.UUIDField(
        label='project',
        required=True,
    )
    external_id = fields.StringField(
        label='external ID',
        required=True,
        max_length=255,
    )
    restriction_keys = fields.StringField(
        label='restriction keys',
        required=True,
        max_length=255,
    )
    subscription_metadata = fields.DictField(
        label='subscription metadata',
        required=True,
    )
    verified = fields.BooleanField(
        label='verified',
        required=False,
    )
    created_at = fields.DateTimeField(
        label='created at',
        required=False,
    )
    updated_at = fields.DateTimeField(
        label='updated fields',
        required=False,
    )

    def clean_project(self, value):
        if isinstance(value, dict):
            pks = ['uuid', 'id', 'pk']
            for pk in pks:
                if pk in value:
                    return value['pk']

        return value
