import json

import pytest
import responses

from congressy.core import SynchableModel
from congressy.core.models import fields
from congressy.core.synchable_models import SynchableManager
from congressy.exceptions import CongressyException


class SynchableCar(SynchableModel):
    """ Example model """

    class Meta(SynchableModel.Meta):
        list_endpoint = '/cars/'
        create_endpoint = '/cars/'
        item_endpoint = '/cars/{pk}'

    color = fields.StringField(label='Color', required=True)
    doors = fields.PositiveIntegerField(label='number of doors', required=True)


def test_api_key_configuration():
    manager = SynchableManager(SynchableCar)
    http_client = manager.http_client

    assert http_client.api_key is None
    assert http_client.api_key_type == http_client.DEFAULT_TOKEN_TYPE

    SynchableCar.authenticate(api_key='fake-key', api_key_type='fake-type')
    manager.set_authentication()
    assert http_client.api_key == 'fake-key'
    assert http_client.api_key_type == 'fake-type'

    # Sets on construction
    manager2 = SynchableManager(SynchableCar)
    http_client2 = manager2.http_client
    assert http_client2.api_key == 'fake-key'
    assert http_client2.api_key_type == 'fake-type'


@responses.activate
def test_get_all_with_invalid_error():
    manager = SynchableManager(SynchableCar)
    http_client = manager.http_client

    response_data = [{
        'doors': 4,
        'color': True,  # wrong key value
    }]

    responses.add(
        responses.GET,
        http_client.get_uri(SynchableCar.Meta.list_endpoint),
        status=200,
        content_type='application/json',
        body=json.dumps({'results': response_data})
    )

    with pytest.raises(CongressyException):
        # Color deveria ser um string
        manager.get_all()


@responses.activate
def test_get_all_with_5xx_error():
    manager = SynchableManager(SynchableCar)
    http_client = manager.http_client

    responses.add(
        responses.GET,
        http_client.get_uri(SynchableCar.Meta.list_endpoint),
        status=503,
        content_type='application/json'
    )

    with pytest.raises(CongressyException):
        # Erro 503 deve voltar como exceção
        manager.get_all()


@responses.activate
def test_get_all_success():
    manager = SynchableManager(SynchableCar)
    http_client = manager.http_client

    response_data = [
        {
            'id': 1,
            'doors': 4,
            'color': 'red',
        },
        {
            'id': 2,
            'doors': 2,
            'color': 'green',
        },
    ]

    responses.add(
        responses.GET,
        url=http_client.get_uri(SynchableCar.Meta.list_endpoint),
        status=200,
        content_type='application/json',
        body=json.dumps({'results': response_data})
    )

    for item in manager.get_all():
        assert isinstance(item, SynchableCar) is True


def get_all_sucessfully_with_empty_return():
    manager = SynchableManager(SynchableCar)
    http_client = manager.http_client

    response_data = []

    responses.add(
        responses.GET,
        url=http_client.get_uri(SynchableCar.Meta.list_endpoint),
        status=200,
        content_type='application/json',
        body=json.dumps({'results': response_data})
    )

    items = manager.get_all()
    assert items == response_data


@responses.activate
def test_get_with_5xx_error():
    manager = SynchableManager(SynchableCar)
    http_client = manager.http_client

    uri = http_client.get_uri(SynchableCar.Meta.item_endpoint, data={
        'pk': 1,
    })

    responses.add(
        responses.GET,
        url=uri,
        status=500,
        content_type='application/json',
        body=None,
    )

    with pytest.raises(CongressyException):
        # Erro 500 deve voltar como exceção
        manager.get(pk=1)


@responses.activate
def test_get_with_invalid_error():
    manager = SynchableManager(SynchableCar)
    http_client = manager.http_client

    response_data = {
        'id': 10,
        'hand': True,  # wrong key
    }

    uri = http_client.get_uri(SynchableCar.Meta.item_endpoint, data={
        'pk': 1,
    })

    responses.add(
        responses.GET,
        url=uri,
        status=200,
        content_type='application/json',
        body=json.dumps({'results': response_data})
    )

    with pytest.raises(CongressyException):
        # Entidade inválida devido ao retorno inválido não contentdo campos
        # Obrigatórios adequados
        manager.get(pk=1)


@responses.activate
def test_get_success():
    manager = SynchableManager(SynchableCar)
    http_client = manager.http_client

    response_data = {
        'id': 10,
        'doors': 2,
        'color': 'yellow',
    }

    uri = http_client.get_uri(SynchableCar.Meta.item_endpoint, data={
        'pk': response_data['id']
    })

    responses.add(
        responses.GET,
        url=uri,
        status=200,
        content_type='application/json',
        body=json.dumps({'results': response_data})
    )

    item = manager.get(pk=response_data['id'])
    assert isinstance(item, SynchableCar)
    assert item.doors == response_data['doors']
    assert item.color == response_data['color']
