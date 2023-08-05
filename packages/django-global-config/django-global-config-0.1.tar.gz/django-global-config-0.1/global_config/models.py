from itertools import chain

from django.db import models
from django.contrib.postgres.fields import ArrayField

from .config import GlobalConfig


def get_field_from_type(t):
    array = False
    if t.startswith('list_'):
        array = True
        t = t.replace('list_', '')

    if t == 'str':
        field = models.CharField(max_length=1000, null=not array)
    elif t == 'int':
        field = models.IntegerField(null=not array)
    elif t == 'float':
        field = models.FloatField(null=not array)
    elif t == 'bool':
        field = models.BooleanField(null=not array)
    else:
        raise NotImplementedError('Type not mapped to a field: ' + t)

    if array:
        field = ArrayField(field, null=True)

    return field


class ConfigItem(models.Model):
    KEYS_BY_TYPE = GlobalConfig._get_keys_by_type()

    # enums
    KeyEnum = models.TextChoices('KeyEnum', ' '.join(
        chain.from_iterable(KEYS_BY_TYPE.values())  # functional programming ftw
    ))

    # fields
    key = models.CharField(max_length=100, choices=KeyEnum.choices, unique=True)
    updated_at = models.DateTimeField(auto_now=True)  # this is the only normal-ish thing in this class

    # set more fields using meta-programming, because why not
    for key_type in ('str', 'int', 'float', 'bool'):
        locals()[key_type] = get_field_from_type(key_type)
        locals()['list_' + key_type] = get_field_from_type('list_' + key_type)

    @property
    def value_field_name(self):
        for k, v in self.KEYS_BY_TYPE.items():
            if self.key in v:
                return k

    @property
    def value(self):
        return getattr(self, self.value_field_name)

    def __str__(self):
        return f'{self.get_key_display()}'
