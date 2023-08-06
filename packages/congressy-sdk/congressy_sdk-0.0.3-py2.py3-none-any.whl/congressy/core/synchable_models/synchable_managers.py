from congressy import configurations
from congressy.exceptions import CongressyException


class SynchableManager:
    def __init__(self, model_class, host=None):

        self.model_class = model_class
        self.http_client = configurations.get_http_client(host)

        self.set_authentication()

    def set_authentication(self):
        meta = self.model_class.Meta
        if hasattr(meta, 'api_key') and meta.api_key:
            key_type = meta.api_key_type or None
            self.http_client.set_api_key(
                key=meta.api_key,
                api_key_type=key_type,
            )

    def get_all(self, **kwargs):
        self.set_authentication()

        endpoint = self.model_class.Meta.list_endpoint.format(**kwargs)
        api_items = self.http_client.list(endpoint, params=kwargs)

        items = list()

        if api_items:
            for item in api_items:
                item.update(**kwargs)
                instance = self.model_class(**item)
                if instance.valid() is False:
                    raise CongressyException(instance.errors)

                items.append(self.model_class(**item))

        return items

    def get(self, **kwargs):
        self.set_authentication()

        instance = self.model_class(**kwargs)
        api_item = self.http_client.get(instance.item_endpoint)

        if not api_item:  # pragma: no-cover
            raise CongressyException('API does not return a response')

        for k, v in api_item.items():
            setattr(instance, k, v)

        if instance.valid() is False:
            raise CongressyException(instance.errors)

        return instance
