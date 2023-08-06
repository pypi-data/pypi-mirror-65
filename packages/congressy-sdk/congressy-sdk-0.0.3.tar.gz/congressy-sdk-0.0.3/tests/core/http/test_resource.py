import pytest
import responses

from congressy.exceptions import CongressyAPIException
from congressy.http import Resource

fake_api_key = 'fake-api-key'
fake_base_url = 'http://api.local.com'


def create_resource():
    """ Creates an instance of resource object """
    resource = Resource(base_url=fake_base_url)
    resource.set_api_key(key=fake_api_key)
    return resource


def test_base_url_slash():
    """ Test base_url configuration concerning to slash in the end """
    expected_base_url = 'http://aaa'

    resource = Resource(base_url=expected_base_url)
    resource.set_api_key(key=fake_api_key)
    assert resource.base_url == expected_base_url

    resource = Resource(base_url=expected_base_url + '/', )
    resource.set_api_key(key=fake_api_key)
    assert resource.base_url == expected_base_url


def test_uri():
    """ Test the way resource URI should return """
    resource = create_resource()
    endpoint = 'my-endpoint'
    expected_uri = '{}/{}/'.format(resource.base_url, endpoint)
    assert resource.get_uri(endpoint) == expected_uri

    # with slash in beginning
    endpoint = '/my-endpoint'
    expected_uri = '{}{}/'.format(resource.base_url, endpoint)
    assert resource.get_uri(endpoint) == expected_uri

    # with slash in the end
    endpoint = 'my-endpoint/'
    expected_uri = '{}/{}'.format(resource.base_url, endpoint)
    assert resource.get_uri(endpoint) == expected_uri

    # with slash in beginning and end
    endpoint = '/my-endpoint/'
    expected_uri = '{}{}'.format(resource.base_url, endpoint)
    assert resource.get_uri(endpoint) == expected_uri


def test_uri_replacement_with_data():
    endpoint = '/my/{param1}/and/{param2}/{id}'
    data = {
        'param1': 'albatroz',
        'param2': 'galileu',
        'id': 1,
    }

    resource = create_resource()
    endpoint = resource.get_uri(endpoint=endpoint, data=data)
    assert endpoint == 'http://api.local.com/my/albatroz/and/galileu/1/'


def test_api_key_configuration():
    resource = create_resource()
    resource.set_api_key(key=fake_api_key)

    assert resource.api_key == fake_api_key
    assert resource.api_key_type == resource.DEFAULT_TOKEN_TYPE

    resource.set_api_key(key=fake_api_key, api_key_type='BearerTest')
    assert resource.api_key_type == 'BearerTest'


def test_headers():
    resource = Resource(base_url=fake_base_url)
    headers = resource.get_headers()

    assert 'User-Agent' in headers
    assert 'Content-Type' in headers

    resource.set_api_key(key=fake_api_key, api_key_type='Bearer')
    headers = resource.get_headers()

    assert 'Authorization' in headers
    assert headers['Authorization'] == 'Bearer {}'.format(fake_api_key)

    headers = resource.get_headers(headers={'Customer-Key': 'custom-value'})

    assert 'Customer-Key' in headers
    assert headers['Customer-Key'] == 'custom-value'


@responses.activate
def test_success_request_with_results():
    resource = create_resource()
    endpoint = '/my-endpoint/'

    responses.add(
        responses.GET,
        resource.get_uri(endpoint),
        status=200,
        content_type='application/json',
        body='{"results": []}'
    )
    results = resource.request(method='GET', endpoint=endpoint)
    assert results == []


@responses.activate
def test_success_request():
    resource = create_resource()
    endpoint = '/my-endpoint/'

    responses.add(
        responses.GET,
        resource.get_uri(endpoint),
        status=200,
        content_type='application/json',
        body='{}'
    )
    resource = create_resource()
    results = resource.request('GET', endpoint)
    assert results == {}


@responses.activate
def test_fail_request():
    resource = create_resource()
    endpoint = '/my-endpoint/'

    responses.add(
        responses.GET,
        resource.get_uri(endpoint),
        status=500,
        content_type='application/json',
        body='{"errors": [{"message": "failure", "description": "desc"}]}'
    )

    resource = create_resource()
    with pytest.raises(CongressyAPIException):
        resource.request('GET', endpoint)


@responses.activate
def test_fail_wrong_json_request():
    resource = create_resource()
    endpoint = '/my-endpoint/'

    responses.add(
        responses.GET,
        resource.get_uri(endpoint),
        status=500,
        content_type='application/json',
        body='{"errors": ["Error!"]}'
    )
    resource = create_resource()
    with pytest.raises(CongressyAPIException):
        resource.request('GET', endpoint)


@responses.activate
def test_fail_no_json_request():
    resource = create_resource()
    endpoint = '/my-endpoint/'

    responses.add(
        responses.GET,
        resource.get_uri(endpoint),
        status=500,
        content_type='application/json',
        body='{"errors": '
    )
    resource = create_resource()
    with pytest.raises(CongressyAPIException):
        resource.request('GET', endpoint)


@responses.activate
def test_fail_no_errors_message():
    resource = create_resource()
    endpoint = '/my-endpoint/'

    responses.add(
        responses.GET,
        resource.get_uri(endpoint),
        status=500,
        content_type='application/json',
        body='no errors'
    )
    resource = create_resource()
    with pytest.raises(CongressyAPIException):
        resource.request('GET', endpoint)


@responses.activate
def test_get():
    resource = create_resource()
    endpoint = '/my-endpoint/'

    responses.add(
        responses.GET,
        resource.get_uri(endpoint),
        status=200,
        content_type='application/json',
        body='{}'
    )
    resource = create_resource()
    results = resource.get(endpoint)
    assert results == {}


@responses.activate
def test_list():
    resource = create_resource()
    endpoint = '/my-endpoint/'

    uri = resource.get_uri(endpoint)

    responses.add(
        responses.GET,
        uri,
        status=200,
        content_type='application/json',
        body='[]'
    )
    results = resource.list(endpoint)
    assert results == []


@responses.activate
def test_create():
    resource = create_resource()
    endpoint = '/my-endpoint/'

    responses.add(
        responses.POST,
        resource.get_uri(endpoint),
        status=200,
        content_type='application/json',
        body='[]'
    )
    results = resource.create(endpoint=endpoint)
    assert results == []


@responses.activate
def test_update():
    resource = create_resource()
    endpoint = '/my-endpoint/'

    responses.add(
        responses.PATCH,
        resource.get_uri(endpoint),
        status=200,
        content_type='application/json',
        body='{}'
    )
    resource = create_resource()
    results = resource.update(endpoint)
    assert results == {}


@responses.activate
def test_delete():
    resource = create_resource()
    endpoint = '/my-endpoint/'

    responses.add(
        responses.DELETE,
        resource.get_uri(endpoint),
        status=204,
        content_type='application/json',
    )
    resource = create_resource()
    results = resource.delete(endpoint)
    assert results is True
