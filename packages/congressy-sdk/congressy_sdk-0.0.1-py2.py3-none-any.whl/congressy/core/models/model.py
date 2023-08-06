from .fields import Field, PositiveIntegerField


class ModelBase(type):
    def __new__(mcs, name, bases, attrs, **kwargs):
        super_new = super().__new__

        # Create the class.
        module = attrs.pop('__module__')
        new_attrs = {'__module__': module, 'pk_field': None}

        # Pass all attrs to type.__new__() so that they're properly initialized
        # (i.e. __set_name__()).
        fields = list()
        pk_field = None

        for obj_name, obj in list(attrs.items()):
            new_attrs[obj_name] = obj

            if isinstance(obj, Field):
                obj.name = obj_name
                fields.append(obj)

                if pk_field is None and obj.primary_key is True:
                    pk_field = obj

        if pk_field is None:
            pk_field = PositiveIntegerField(label='ID')
            pk_field.name = 'id'
            pk_field.primary_key = True
            fields.append(pk_field)

        new_attrs.update({
            'fields': fields,
            'field_names': [f.name for f in fields],
            'pk_field': pk_field,
        })
        # new_attrs[pk_field.name] = pk_field.value
        new_attrs.update(attrs)

        return super_new(mcs, name, bases, new_attrs, **kwargs)


class Model(metaclass=ModelBase):
    def __init__(self, *args, **kwargs):
        self._errors = dict()

        for field in self.fields:
            prop = field.name
            value = None
            if prop in kwargs:
                value = kwargs.pop(prop)

            setattr(self, prop, value)

        if 'pk' in kwargs:
            setattr(self, self.pk_field.name, kwargs.pop('pk'))

    @property
    def pk(self):
        return self.pk_field.value

    @property
    def errors(self) -> dict:
        self.valid()
        return self._errors

    def to_dict(self):
        data = dict()
        for f in self.fields:
            data[f.name] = f.exportable_value

        data['pk'] = self.pk_field.exportable_value

        return data

    def valid(self) -> bool:
        self._errors = dict()
        for field in self.fields:
            if field.valid() is False:
                self._errors[field.name] = field.errors

        return not self._errors

    def get_field(self, name) -> Field:

        found_field = None

        for f in self.fields:
            if f.name == name:
                found_field = f
                break

        return found_field

    def __setattr__(self, key, value):
        setter_method = None
        setter_method_str = 'clean_{}'.format(key)
        if key.startswith('_') is False and hasattr(self, setter_method_str):
            setter_method = getattr(self, setter_method_str)
            if callable(setter_method) is False:
                setter_method = None

        if value:
            value = setter_method(value) if setter_method else value

        if key in self.field_names:
            field = self.get_field(key)
            field.value = value

            # returns value after field validation
            value = field.value

        elif key == 'pk':
            setattr(self, self.pk_field.name, value)

        super().__setattr__(key, value)
