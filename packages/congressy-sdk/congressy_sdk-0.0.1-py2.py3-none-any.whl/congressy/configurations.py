from congressy.constants import PROD_BASE_URL
from congressy.http import Resource


def get_http_client(host=None):
    host = host or PROD_BASE_URL
    return Resource(base_url=host)
