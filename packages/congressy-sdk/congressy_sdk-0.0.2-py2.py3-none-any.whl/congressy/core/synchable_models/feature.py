from congressy.core import SynchableModel


class Feature:
    def __init__(self, api_key: str = None,
                 api_key_type: str = 'Bearer',
                 host=None):
        self.api_key = api_key
        self.api_key_type = api_key_type
        self.host = host

    def configure_endpoint(self, endpoint_class):
        if issubclass(endpoint_class, SynchableModel) is False:
            raise Exception(
                'Class {} must be a subclass of SynchableModel'.format(
                    endpoint_class.__name__
                )
            )
        endpoint_class.authenticate(self.api_key, self.api_key_type)
        if self.host:
            endpoint_class.set_host(self.host)
        return endpoint_class
