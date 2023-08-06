from congressy.core import synchable_models as models
from congressy.core.models import fields


class Category(models.SynchableModel):
    class Meta(models.SynchableModel.Meta):
        list_endpoint = '/v1/videos/categories'
        create_endpoint = list_endpoint
        item_endpoint = '/v1/videos/categories/{pk}'

    uuid = fields.UUIDField(
        label='ID',
        required=True,
        primary_key=True,
    )
    project = fields.UUIDField(
        label='project',
        required=True,
    )
    name = fields.StringField(
        label='name',
        required=True,
        max_length=100,
    )
    active = fields.BooleanField(
        label='ative',
        required=True,
    )
    created_at = fields.DateTimeField(
        label='created at',
        required=True,
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
