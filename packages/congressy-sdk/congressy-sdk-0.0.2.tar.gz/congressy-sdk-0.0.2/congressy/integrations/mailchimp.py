from congressy.core import synchable_models as models
from congressy.core.models import fields


class Namespace(models.SynchableModel):
    class Meta(models.SynchableModel.Meta):
        list_endpoint = '/v1/mailchimp/namespaces'
        create_endpoint = '/v1/mailchimp/namespaces'
        item_endpoint = '/v1/mailchimp/namespaces/{pk}'

    uuid = fields.UUIDField(
        label='ID',
        required=True,
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
    api_key = fields.StringField(
        label='api_key',
        required=True,
        max_length=48,
    )
    external_id = fields.StringField(
        label='external ID',
        required=True,
        max_length=255,
    )
    default_tag = fields.StringField(
        label='default tag',
        required=True,
        max_length=80,
    )
    default_list_id = fields.StringField(
        label='default list ID',
        required=False,
        max_length=20,
    )
    default_list_name = fields.StringField(
        label='default list Name',
        required=False,
        max_length=80,
    )
    sync_phone = fields.BooleanField(
        label='sychronize phone',
        required=False,
        default_value=True,
    )
    sync_address = fields.BooleanField(
        label='sychronize address',
        required=False,
        default_value=True,
    )
    create_notes = fields.BooleanField(
        label='create notes',
        required=False,
        default_value=False,
    )
    create_fields = fields.BooleanField(
        label='create fields',
        required=False,
        default_value=False,
    )
    created_at = fields.DateTimeField(
        label='created at',
        required=True,
    )
    updated_at = fields.DateTimeField(
        label='updated fields',
        required=False,
    )
    healthy = fields.BooleanField(
        label='healthy',
        required=False,
        default_value=False,
    )


class AudienceList(models.SynchableModel):
    class Meta(models.SynchableModel.Meta):
        list_endpoint = '/v1/mailchimp/namespaces/{namespace_id}/lists'
        create_endpoint = '/v1/mailchimp/namespaces/{namespace_id}/lists'
        item_endpoint = '/v1/mailchimp/namespaces/{namespace_id}/lists/{pk}'

    namespace_id = fields.UUIDField(
        label='namespace ID',
        required=True,
    )
    id = fields.StringField(
        label='ID',
        required=True,
        primary_key=True,
    )
    web_id = fields.PositiveIntegerField(
        label='web ID',
        required=True,
    )
    name = fields.StringField(
        label='name',
        required=True,
        max_length=32,
    )


class MailChimp:
    def __init__(self, api_key: str = None, api_key_type: str = 'Bearer'):
        self.api_key = api_key
        self.api_key_type = api_key_type

    @property
    def namespace_class(self):
        Namespace.authenticate(self.api_key, self.api_key_type)
        return Namespace

    def create_namespace(self, data: dict):
        return self.namespace_class(**data)

    def get_namespace(self, pk):
        return self.namespace_class.get_manager().get(pk=pk)

    def get_namespaces(self):
        return self.namespace_class.get_manager().get_all()

    @property
    def audience_list_class(self):
        AudienceList.authenticate(self.api_key, self.api_key_type)
        return AudienceList

    def get_audience_list(self, namespace_pk, pk):
        return self.audience_list_class.get_manager().get(
            pk=pk,
            namespace_id=namespace_pk
        )

    def get_audience_lists(self, namespace_pk: str):
        return self.audience_list_class.get_manager().get_all(
            namespace_id=namespace_pk
        )
