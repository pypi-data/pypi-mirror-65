from congressy.core.models import Model
from congressy.exceptions import CongressyException
from .synchable_managers import SynchableManager


class SynchableModel(Model):
    class Meta:
        list_endpoint = None
        create_endpoint = None
        item_endpoint = None
        api_key = None
        api_key_type = None
        host = None

    manager_class = SynchableManager

    def __init__(self, *args, **kwargs):
        attr_meta = self.Meta

        wrong_meta_fields = list()

        if not attr_meta.list_endpoint:
            wrong_meta_fields.append(
                'You must provide "list_endpoint" string which must be the'
                ' Rest HTTP Resource of the model.'
            )

        if not attr_meta.create_endpoint:
            wrong_meta_fields.append(
                'You must provide "create_endpoint" string which must be the'
                ' Rest HTTP Resource of the model.'
            )

        if not attr_meta.item_endpoint:
            wrong_meta_fields.append(
                'You must provide "item_endpoint" string which must be the'
                ' Rest HTTP Resource of the model.'
            )

        if wrong_meta_fields:
            raise Exception('; '.join(wrong_meta_fields))

        super().__init__(*args, **kwargs)

    @classmethod
    def authenticate(cls, api_key: str, api_key_type: str = None):
        cls.Meta.api_key = api_key
        cls.Meta.api_key_type = api_key_type

    @classmethod
    def set_host(cls, host: str):
        cls.Meta.host = host

    @classmethod
    def get_manager(cls):
        return cls.manager_class(cls, host=cls.Meta.host)

    @classmethod
    def get_http_client(cls):
        return cls.get_manager().http_client

    @property
    def list_endpoint(self):
        return self.Meta.list_endpoint.format(**self.to_dict())

    @property
    def list_uri(self):
        return self.get_http_client().get_uri(self.list_endpoint)

    @property
    def create_endpoint(self):
        return self.Meta.create_endpoint.format(**self.to_dict())

    @property
    def create_uri(self):
        return self.get_http_client().get_uri(self.create_endpoint)

    @property
    def item_endpoint(self, data: dict = None):
        return self.Meta.item_endpoint.format(**self.to_dict())

    @property
    def item_uri(self):
        return self.get_http_client().get_uri(self.item_endpoint)

    def save(self):
        if self.valid() is False:
            raise CongressyException('You cannot save invalid models.')

        if self.pk is None:
            data = self.get_http_client().create(endpoint=self.create_endpoint,
                                                 data=self.to_dict())

            f_names = self.field_names
            for f_name, value in data.items():
                if f_name in f_names:
                    setattr(self, f_name, value)

            if self.pk_field.name in data:
                setattr(self, self.pk_field.name, data[self.pk_field.name])
            elif 'pk' in data:
                setattr(self, self.pk_field.name, data['pk'])
        else:
            self.get_http_client().update(endpoint=self.item_endpoint,
                                          data=self.to_dict())

    def delete(self):
        if self.pk is None:
            return
        self.get_http_client().delete(endpoint=self.item_endpoint)
