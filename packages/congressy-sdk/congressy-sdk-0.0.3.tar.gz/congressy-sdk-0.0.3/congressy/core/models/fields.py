import uuid
from datetime import datetime
from decimal import Decimal

from validation import (
    validate_bool,
    validate_date,
    validate_datetime,
    validate_int,
    validate_float,
    validate_text,
)

TYPE_STRING = 'string'
TYPE_INTEGER = 'integer'
TYPE_FLOAT = 'float'
TYPE_DATE = 'date'
TYPE_DATETIME = 'datetime'
TYPE_BOOLEAN = 'boolean'
TYPE_LIST = 'list'
TYPE_DICT = 'dict'


class Field:
    type = None

    def __init__(self,
                 label: str,
                 required=False,
                 value=None,
                 primary_key=True):

        self.label = label
        self.required = required
        self.name = None

        self.primary_key = False

        self.errors = list()
        self._value = None

        if value:
            self.value = value

        self.primary_key = primary_key

    @property
    def exportable_value(self):
        return self.value

    def valid(self) -> bool:
        if not self.value:
            return self.required is False

        return len(self.errors) == 0

    def _validate(self):
        raise NotImplementedError()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.normalize_value(value)
        self._validate()

    def normalize_value(self, value):
        return value

    def __str__(self):
        return str(self.value)


class StringField(Field):
    def __init__(self,
                 label: str,
                 required=False,
                 value=None,
                 pattern=None,
                 max_length=None,
                 primary_key=False):
        self.type = TYPE_STRING
        self.pattern = pattern
        self.max_length = max_length

        super().__init__(label, required, value, primary_key)

    def _validate(self):
        self.errors = list()
        try:
            validate_text(
                value=self.value,
                max_length=self.max_length,
                pattern=self.pattern,
                required=self.required is True,
            )
        except (TypeError, ValueError) as e:
            self.errors.append(str(e))


class UUIDField(Field):
    def __init__(self,
                 label: str,
                 required=False,
                 value=None,
                 primary_key=False):
        self.type = TYPE_STRING
        super().__init__(label, required, value, primary_key)

    @property
    def exportable_value(self):
        return str(self.value) if self.value else None

    def _validate(self):
        self.errors = list()
        if self.required is True and not self.value:
            self.errors.append('This value is required')
            return

        try:
            uuid.UUID(str(self.value), version=4)
        except (TypeError, AttributeError, ValueError) as e:
            self.errors.append(str(e))


class DateField(Field):
    def __init__(self,
                 label: str,
                 required=False,
                 value=None,
                 primary_key=False):
        self.type = TYPE_DATE
        super().__init__(label, required, value, primary_key)

    @property
    def exportable_value(self):
        return self.value.strftime('%Y-%m-%d') \
            if self.value \
            else ''

    def _validate(self):
        self.errors = list()
        try:
            validate_date(value=self.value, required=self.required)
        except (TypeError, ValueError) as e:
            self.errors.append(str(e))

    def normalize_value(self, value):
        value = super().normalize_value(value)
        if value:
            try:
                value = datetime.strptime(str(value), '%Y-%m-%d').date()
            except (TypeError, ValueError) as e:
                print(e)

        return value


class DateTimeField(Field):
    def __init__(self,
                 label: str,
                 required=False,
                 value=None,
                 primary_key=False):
        self.type = TYPE_DATETIME
        super().__init__(label, required, value, primary_key)

    @property
    def exportable_value(self):
        return self.value.strftime('%Y-%m-%dT%H:%M:%S%z') \
            if self.value \
            else ''

    def _validate(self):
        self.errors = list()
        try:
            validate_datetime(value=self.value, required=self.required)
        except (TypeError, ValueError) as e:
            self.errors.append(str(e))

    def normalize_value(self, value):
        value = super().normalize_value(value)
        if value and isinstance(value, datetime) is False:
            try:
                value = datetime.strptime(str(value), '%Y-%m-%dT%H:%M:%S%z')
            except (TypeError, ValueError) as e:
                print(e)

        return value

    def __str__(self):
        return self.exportable_value


class BooleanField(Field):
    def __init__(self,
                 label: str,
                 required=False,
                 default_value=None,
                 value=None,
                 primary_key=False):
        self.type = TYPE_BOOLEAN
        if not value and default_value:
            value = default_value

        self.default_value = default_value
        super().__init__(label, required, value, primary_key)

    def valid(self) -> bool:
        if isinstance(self.value, bool) is False:
            return self.required is False

        return len(self.errors) == 0

    def _validate(self):
        self.errors = list()
        try:
            validate_bool(value=self.value, required=self.required)
        except (TypeError, ValueError) as e:
            self.errors.append(str(e))


class IntegerField(Field):
    def __init__(self,
                 label: str,
                 required=False,
                 value=None,
                 primary_key=False,
                 min_value=None,
                 max_value=None):
        self.type = TYPE_INTEGER
        self.min_value = min_value
        self.max_value = max_value

        super().__init__(label, required, value, primary_key)

    def _validate(self):
        self.errors = list()
        try:
            validate_int(
                value=self.value,
                required=self.required is True,
                min_value=self.min_value,
                max_value=self.max_value,
            )
        except (TypeError, ValueError) as e:
            self.errors.append(str(e))


class PositiveIntegerField(Field):
    def __init__(self,
                 label: str,
                 required=False,
                 value=None,
                 primary_key=False,
                 max_value=None):
        self.type = TYPE_INTEGER
        self.min_value = 1
        self.max_value = max_value

        super().__init__(label, required, value, primary_key)

    def _validate(self):
        self.errors = list()

        try:
            validate_int(
                value=self.value,
                required=self.required is True,
                min_value=self.min_value,
                max_value=self.max_value,
            )
        except (TypeError, ValueError) as e:
            self.errors.append(str(e))


class DecimalField(Field):
    def __init__(self,
                 label: str,
                 required=False,
                 value=None,
                 primary_key=False):
        self.type = TYPE_FLOAT
        super().__init__(label, required, value, primary_key)

    def _validate(self):
        self.errors = list()
        try:
            if isinstance(self.value, Decimal) is False:
                raise ValueError('Value must be instance of decimal')

            # takes advantage of req
            validate_float(value=float(self.value), required=self.required)
        except (TypeError, ValueError) as e:
            self.errors.append(str(e))


class DictField(Field):
    def __init__(self,
                 label: str,
                 required=False,
                 value=None,
                 primary_key=False):
        self.type = TYPE_DICT
        super().__init__(label, required, value, primary_key)

    def _validate(self):
        self.errors = list()
        if isinstance(self.value, dict) is False:
            self.errors.append('Value is not a valid dict.')
