from congressy.core import synchable_models as models
from congressy.core.models import fields


class Project(models.SynchableModel):
    class Meta(models.SynchableModel.Meta):
        list_endpoint = '/v1/videos/projects'
        create_endpoint = '/v1/videos/projects'
        item_endpoint = '/v1/videos/projects/{pk}'

    uuid = fields.UUIDField(
        label='ID',
        primary_key=True,
    )
    name = fields.StringField(
        label='name',
        required=True,
        max_length=100,
    )
    namespace = fields.UUIDField(
        label='namespace',
        required=True,
    )
    active = fields.BooleanField(
        label='ative',
        required=True,
    )
    created_at = fields.DateTimeField(
        label='created at',
        required=False,
    )
    updated_at = fields.DateTimeField(
        label='updated fields',
        required=False,
    )

    def clean_namespace(self, value):
        if isinstance(value, dict):
            pks = ['uuid', 'id', 'pk']
            for pk in pks:
                if pk in value:
                    return value['pk']

        return value
