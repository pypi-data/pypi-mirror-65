from congressy.core import synchable_models as models
from congressy.core.models import fields


class Video(models.SynchableModel):
    class Meta(models.SynchableModel.Meta):
        list_endpoint = '/v1/videos/videos'
        create_endpoint = list_endpoint
        item_endpoint = '/v1/videos/videos/{pk}'

    uuid = fields.UUIDField(
        label='ID',
        required=True,
        primary_key=True,
    )
    name = fields.StringField(
        label='name',
        required=True,
        max_length=255,
    )
    provider = fields.StringField(
        label='provider',
        required=True,
        max_length=255,
    )
    project = fields.UUIDField(
        label='project',
        required=True,
    )
    category = fields.UUIDField(
        label='project',
        required=False,
    )
    main_video = fields.UUIDField(
        label='main video',
        required=False,
    )
    external_id = fields.StringField(
        label='external ID',
        required=True,
        max_length=255,
    )
    link = fields.StringField(
        label='link',
        required=True,
        max_length=500,
    )
    thumbnail_link = fields.StringField(
        label='link',
        required=False,
        max_length=500,
    )
    description_html = fields.StringField(
        label='description (html)',
        required=False,
        max_length=5000,
    )
    description = fields.StringField(
        label='description (html)',
        required=False,
        max_length=5000,
    )
    active = fields.BooleanField(
        label='active',
        required=True,
        default_value=False,
    )
    restrict = fields.BooleanField(
        label='restriction',
        required=True,
        default_value=False,
    )
    is_360 = fields.BooleanField(
        label='360 degrees',
        required=True,
        default_value=False,
    )
    starts_at = fields.DateTimeField(
        label='starts at',
        required=False,
    )
    ends_at = fields.DateTimeField(
        label='ends at',
        required=False,
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

    def clean_category(self, value):
        if isinstance(value, dict):
            pks = ['uuid', 'id', 'pk']
            for pk in pks:
                if pk in value:
                    return value['pk']

            return value
