from .exceptions import CongressyAPIException


class Transporter(object):
    def __init__(self):
        import requests
        self.sess = requests.Session()

    def request(self, method, uri, headers, data=None, params=None, **kwargs):
        response = self.sess.request(method,
                                     uri,
                                     headers=headers,
                                     json=data,
                                     params=params,
                                     **kwargs)
        if response.status_code == 204:
            return True
        if not response.ok:
            raise CongressyAPIException(response)
        if 'results' in response.json():
            return response.json()['results']
        return response.json()


class Resource(object):
    DEFAULT_TOKEN_TYPE = 'Token'

    def __init__(self, base_url: str, transporter_class=Transporter):
        if base_url.endswith('/'):
            base_url = base_url[:-1]

        self.base_url = base_url
        self.transporter = transporter_class()

        self.api_key = None
        self.api_key_type = self.DEFAULT_TOKEN_TYPE

    def set_api_key(self, key, api_key_type: str = None):
        self.api_key = key

        if not api_key_type:
            api_key_type = self.DEFAULT_TOKEN_TYPE

        self.api_key_type = api_key_type

    def get_uri(self, endpoint: str, data: dict = None):
        if not endpoint.startswith('/'):
            endpoint = '/{}'.format(endpoint)

        if not endpoint.endswith('/'):
            endpoint = '{}/'.format(endpoint)

        if data:
            endpoint = endpoint.format(**data)

        return '{}{}'.format(self.base_url, endpoint)

    def get_headers(self, headers: dict = None):
        default_headers = {
            'User-Agent': 'congressy-sdk-python/0.0.1',
            'Content-Type': 'application/json',
        }

        if self.api_key:
            key = '{}{}'.format(
                self.api_key_type + ' ' or '',
                self.api_key
            )
            default_headers['Authorization'] = key

        if headers:
            default_headers.update(headers)

        return default_headers

    def request(self,
                method,
                endpoint,
                headers: dict = None,
                data: dict = None,
                ** kwargs):

        headers = headers or dict()
        headers = self.get_headers(**headers)

        data = data or dict()

        return self.transporter.request(
            method=method,
            uri=self.get_uri(endpoint, data=data),
            headers=headers,
            data=data,
            **kwargs,
        )

    def get(self, endpoint, data: dict = None, headers: dict = None):
        return self.request(
            method='GET',
            endpoint=endpoint,
            headers=headers,
            data=data,
        )

    def list(self,
             endpoint,
             params: dict = None,
             data: dict = None,
             headers: dict = None):
        # @TODO precisa de melhorias
        return self.request(
            method='GET',
            endpoint=endpoint,
            headers=headers,
            data=data,
            params=params,
        )

    def create(self, endpoint, data: dict = None, headers: dict = None):
        return self.request(
            method='POST',
            endpoint=endpoint,
            headers=headers,
            data=data,
        )

    def update(self, endpoint, data: dict = None, headers: dict = None):
        return self.request(
            method='PATCH',
            endpoint=endpoint,
            headers=headers,
            data=data,
        )

    def delete(self, endpoint, data: dict = None, headers: dict = None):
        return self.request(
            method='DELETE',
            endpoint=endpoint,
            headers=headers,
            data=data,
        )
