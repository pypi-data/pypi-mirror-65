import pytest
import responses

from congressy.exceptions import CongressyAPIException
from congressy.http import Transporter

fake_api_key = 'fake-api-key'
fake_resource_uri = 'http://api.local.com/my-resource/1/'
fake_headers = {
    'User-Agent': 'congressy-sdk-python/0.0.1',
    'Content-Type': 'application/json',
    'Authorization': 'my-api-key'
}


@responses.activate
def test_success_request():
    responses.add(
        responses.GET,
        fake_resource_uri,
        status=200,
        content_type='application/json',
        body='{}'
    )

    transporter = Transporter()
    results = transporter.request('GET', fake_resource_uri, fake_headers)
    assert results == {}


@responses.activate
def test_success_request_with_results():
    responses.add(
        responses.GET,
        fake_resource_uri,
        status=200,
        content_type='application/json',
        body='{"results": []}'
    )
    transporter = Transporter()
    results = transporter.request('GET', fake_resource_uri, fake_headers)
    assert results == []


@responses.activate
def test_fail_request():
    responses.add(
        responses.GET,
        fake_resource_uri,
        status=500,
        content_type='application/json',
        body='{"errors": [{"message": "failure", "description": "desc"}]}'
    )
    transporter = Transporter()
    with pytest.raises(CongressyAPIException):
        transporter.request('GET', fake_resource_uri, fake_headers)


@responses.activate
def test_fail_wrongjson_request():
    responses.add(
        responses.GET,
        fake_resource_uri,
        status=500,
        content_type='application/json',
        body='{"errors": ["Error!"]}'
    )
    transporter = Transporter()
    with pytest.raises(CongressyAPIException):
        transporter.request('GET', fake_resource_uri, fake_headers)


@responses.activate
def test_fail_nojson_request():
    responses.add(
        responses.GET,
        fake_resource_uri,
        status=500,
        content_type='application/json',
        body='{"errors": '
    )
    transporter = Transporter()
    with pytest.raises(CongressyAPIException):
        transporter.request('GET', fake_resource_uri, fake_headers)


@responses.activate
def test_fail_no_errors():
    responses.add(
        responses.GET,
        fake_resource_uri,
        status=500,
        content_type='application/json',
        body='no errors'
    )
    transporter = Transporter()
    with pytest.raises(CongressyAPIException):
        transporter.request('GET', fake_resource_uri, fake_headers)
