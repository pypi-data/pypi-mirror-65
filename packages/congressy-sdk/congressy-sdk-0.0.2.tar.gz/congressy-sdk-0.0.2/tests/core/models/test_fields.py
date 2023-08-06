import uuid
import pytz
from datetime import date, datetime
from decimal import Decimal

import pytest

from congressy.core.models import fields


def test_base_field():
    """
    Test base field
    """
    field = fields.Field(label='field')

    with pytest.raises(NotImplementedError):
        field.value = 'bla'


def test_string_field():
    """
    Test string field
    """
    field = fields.StringField(label='Name', required=True, value=1)

    assert field.valid() is False

    field.value = 'bla'
    assert field.valid() is True

    assert field.exportable_value == field.value
    assert str(field) == field.value


def test_uuid_field():
    """
    Test alternative primary key as UUID
    """
    field = fields.UUIDField(label='Name', required=True)

    field.value = 1
    assert field.valid() is False

    field.value = 'bla'
    assert field.valid() is False

    field.value = uuid.uuid4()
    assert field.valid() is True

    assert field.exportable_value == str(field.value)
    assert str(field) == str(field.value)


def test_date_field():
    """
    Test date field
    """
    field = fields.DateField(label='Name', required=True)

    field.value = 1
    assert field.valid() is False

    field.value = 'bla'
    assert field.valid() is False

    field.value = True
    assert field.valid() is False

    field.value = '2019-08-25'
    assert field.valid() is True

    field.value = datetime.now()
    assert field.valid() is False

    field.value = date(2019, 8, 25)
    assert field.valid() is True

    assert field.exportable_value == '2019-08-25'
    assert str(field) == '2019-08-25'


def test_datetime_field():
    """
    Test datetime field
    """
    field = fields.DateTimeField(label='Name', required=True)

    field.value = 1
    assert field.valid() is False

    field.value = 'bla'
    assert field.valid() is False

    field.value = True
    assert field.valid() is False

    field.value = '2019-08-25'
    assert field.valid() is False

    field.value = datetime.now(tz=pytz.timezone('America/Sao_Paulo'))
    assert field.valid() is True

    field.value = date(2019, 8, 25)
    assert field.valid() is False

    field.value = '2019-08-25T12:55:03-0300'
    assert field.valid() is True

    assert field.exportable_value == '2019-08-25T12:55:03-0300'
    assert str(field) == '2019-08-25T12:55:03-0300'


def test_integer_field():
    """
    Test integer field
    """
    field = fields.IntegerField(label='Name', required=True, value='bla')

    assert field.valid() is False

    field.value = 1
    assert field.valid() is True

    assert field.exportable_value == 1
    assert str(field) == '1'


def test_positive_integer_field():
    """
    Test integer field only for positive values
    """
    field = fields.PositiveIntegerField(label='Name', required=True)

    field.value = 'bla'
    assert field.valid() is False

    field.value = -1
    assert field.valid() is False

    field.value = 1.5
    assert field.valid() is False

    field.value = 1
    assert field.valid() is True

    assert str(field) == '1'


def test_decimal_field():
    """
    Test decimal field
    """
    field = fields.DecimalField(label='Name', required=True)

    field.value = 'bla'
    assert field.valid() is False

    field.value = -1
    assert field.valid() is False

    field.value = 1.5
    assert field.valid() is False

    field.value = 1
    assert field.valid() is False

    field.value = Decimal(1)
    assert field.valid() is True


def test_boolean_field():
    """
    Test boolean field
    """
    field = fields.BooleanField(label='Name', required=True)

    field.value = 1
    assert field.valid() is False

    field.value = 'bla'
    assert field.valid() is False

    field.value = True
    assert field.valid() is True

    assert str(field) == 'True'


def test_requirements():
    """
    Testa campos obrigatório
    """
    field_classes = [
        fields.StringField,
        fields.UUIDField,
        fields.DateField,
        fields.DateTimeField,
        fields.BooleanField,
        fields.IntegerField,
        fields.PositiveIntegerField,
        fields.DecimalField,
    ]

    for field_class in field_classes:
        field = field_class(label='required', required=False)
        assert field.valid() is True

        field_req = field_class(label='required', required=True)
        assert field_req.valid() is False
