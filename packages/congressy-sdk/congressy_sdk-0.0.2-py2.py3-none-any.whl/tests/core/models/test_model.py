import uuid

from congressy.core.models import fields
from congressy.core.models.model import Model


class Car(Model):
    """ Example model """
    color = fields.StringField(label='Color', required=False)
    doors = fields.PositiveIntegerField(label='number of doors')


class CarUUID(Model):
    """ Example model with UUID field as alterantive primary key """
    uuid = fields.UUIDField(label='uuid', primary_key=True)
    color = fields.StringField(label='Color', required=False)
    doors = fields.PositiveIntegerField(label='number of doors')


def test_no_configured_fields():
    """ Test not configured field having only ID field as default field """
    model = Model()
    assert model.field_names == ['id']


def test_model_has_pkfield_by_default():
    """
    Test model with primary key by default being accessed by 'pk' property.
    """
    model = Car()

    assert model.pk is None
    assert isinstance(model.pk_field, fields.PositiveIntegerField)

    model = Car(pk=2)
    assert model.pk == 2
    assert model.id == 2

    model = Car(doors=4)
    assert model.pk is None


def test_model_has_uuid_as_pk():
    """
    Test model with primary key as UUID as an alternative primary key and being
    accessed by 'pk' property.
    """
    uuid_v = uuid.uuid4()
    model = CarUUID(pk=uuid_v)

    assert model.pk == uuid_v
    assert model.uuid == uuid_v


def test_list_fields():
    """
    Test 'field_names' attribute with a list of configured field's names.
    """
    model = Car()
    assert 'color' in model.field_names
    assert 'doors' in model.field_names


def test_populate_field_in_constructor():
    """
    Test constructor to populate fields when arguments with the same
    name of model's fields are given
    """
    model = Car(doors=5, color='yellow')

    assert model.color == 'yellow'
    assert model.doors == 5

    field = model.get_field('color')
    assert field.value == 'yellow'

    field = model.get_field('doors')
    assert field.value == 5


def test_set_get_value():
    """ Test model fields when values as given as properties. """
    model = Car()

    model.color = 'red'
    model.doors = 5

    field = model.get_field('color')
    assert field.value == 'red'

    field = model.get_field('doors')
    assert field.value == 5


def test_fields_validation():
    """ Test fields validation when given value is not of the correct type. """
    model = Car(doors='not number', color=True)

    assert model.valid() is False
    assert 'doors' in model.errors.keys()
    assert 'color' in model.errors.keys()

    model.color = 'red'
    model.doors = 5
    assert model.valid() is True


def test_new_instance_to_data():
    model = Car(doors=4, color='green')
    expected_data = {'doors': 4, 'color': 'green', 'id': None, 'pk': None}
    assert model.to_dict() == expected_data

    model = CarUUID(doors=4, color='green')
    expected_data = {'doors': 4, 'color': 'green', 'uuid': None, 'pk': None}
    assert model.to_dict() == expected_data


def test_existing_instance_to_data():
    model = Car(id=3, doors=4, color='green')
    expected_data = {'doors': 4, 'color': 'green', 'id': 3, 'pk': 3}
    assert model.to_dict() == expected_data

    pk = uuid.uuid4()
    model = CarUUID(uuid=str(pk), doors=4, color='green')
    expected_data = {
        'doors': 4,
        'color': 'green',
        'uuid': str(pk),
        'pk': str(pk)
    }
    assert model.to_dict() == expected_data

# @TODO Test atribute value acording to the field type
