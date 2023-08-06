from congressy.core import synchable_models as models
from congressy.core.models import fields


class User(models.SynchableModel):
    class Meta(models.SynchableModel.Meta):
        list_endpoint = '/v1/videos/users'
        create_endpoint = '/v1/videos/users/'
        item_endpoint = '/v1/videos/users/{username}'

    pk = fields.IntegerField(
        label='ID',
        primary_key=True,
    )
    first_name = fields.StringField(
        label='first name',
        required=True,
        max_length=30,
    )
    last_name = fields.StringField(
        label='last name',
        required=True,
        max_length=30,
    )
    username = fields.StringField(
        label='username',
        required=True,
        max_length=100,
    )
    auth_token = fields.StringField(
        label='auth token',
        required=False,
        max_length=100,
    )
