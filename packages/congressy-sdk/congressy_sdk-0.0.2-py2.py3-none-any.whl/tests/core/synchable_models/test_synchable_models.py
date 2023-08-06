import json

import pytest
import responses

from congressy.core.models import fields
from congressy.core.synchable_models import SynchableModel


class Car(SynchableModel):
    """ Example model """

    class Meta(SynchableModel.Meta):
        list_endpoint = '/cars/'
        create_endpoint = '/cars/'
        item_endpoint = '/cars/{pk}'

    color = fields.StringField(label='Color', required=False)
    doors = fields.PositiveIntegerField(label='number of doors')


def test_wrong_meta_configuration():
    class WrongCar(SynchableModel):
        """ Example model """
        color = fields.StringField(label='Color', required=False)
        doors = fields.PositiveIntegerField(label='number of doors')

    with pytest.raises(Exception):
        WrongCar()


def test_configuration():
    """
    Test model configuration
    """
    car = Car(id=2, color='red', doors=4)
    create_endpoint = car.create_uri
    meta_create_endpoint = \
        Car.get_http_client().get_uri(Car.Meta.create_endpoint)
    assert create_endpoint == meta_create_endpoint

    item_endpoint = car.item_uri.format(pk=car.pk)
    meta_item_endpoint = \
        Car.get_http_client().get_uri(Car.Meta.item_endpoint, car.to_dict())
    assert item_endpoint == meta_item_endpoint


def test_endpoints():
    car = Car(id=2, color='red', doors=4)

    assert car.list_endpoint == Car.Meta.list_endpoint
    assert car.create_endpoint == Car.Meta.create_endpoint
    assert car.item_endpoint == Car.Meta.item_endpoint.format(**car.to_dict())


def test_uris():
    car = Car(id=2, color='red', doors=4)
    http_client = car.get_http_client()

    assert car.list_uri == http_client.get_uri(Car.Meta.list_endpoint)
    assert car.create_uri == http_client.get_uri(Car.Meta.create_endpoint)
    assert car.item_uri.format(**car.to_dict()) == http_client.get_uri(
        endpoint=Car.Meta.item_endpoint,
        data=car.to_dict(),
    )


@responses.activate
def test_save_new_item():
    car = Car(color='red', doors=4)

    response_data = car.to_dict()
    response_data['id'] = 2
    response_data = {'results': response_data}

    responses.add(
        responses.POST,
        car.create_uri,
        status=201,
        content_type='application/json',
        body=json.dumps(response_data)
    )

    car.save()


@responses.activate
def test_save_existing_item():
    car = Car(id=3, color='red', doors=4)

    response_data = car.to_dict()
    response_data = {'results': response_data}

    responses.add(
        responses.PATCH,
        car.item_uri,
        status=200,
        content_type='application/json',
        body=json.dumps(response_data)
    )

    car.save()


@responses.activate
def test_delete_item():
    car = Car(id=3, color='red', doors=4)

    response_data = car.to_dict()
    response_data = {'results': response_data}

    responses.add(
        responses.DELETE,
        car.item_uri,
        status=204,
        content_type='application/json'
    )

    car.delete()
