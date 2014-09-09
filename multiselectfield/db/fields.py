# -*- coding: utf-8 -*-
# Copyright (c) 2012-2013 by Pablo Martín <goinnn@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this programe.  If not, see <http://www.gnu.org/licenses/>.

import sys

import django

from django.db import models
from django.utils.text import capfirst
from django.core import exceptions
from django.utils.encoding import force_text

from ..forms.fields import MultiSelectFormField, MaxChoicesValidator
from ..utils import get_max_length
from ..validators import MaxValueMultiFieldValidator

if sys.version_info[0] == 2:
    string_type = unicode
else:
    string_type = str

# Code from six egg https://bitbucket.org/gutworth/six/src/a3641cb211cc360848f1e2dd92e9ae6cd1de55dd/six.py?at=default


def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        for slots_var in orig_vars.get('__slots__', ()):
            orig_vars.pop(slots_var)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


class MultiSelectField(models.CharField):
    """ Choice values can not contain commas. """

    def __init__(self, *args, **kwargs):
        self.max_choices = kwargs.pop('max_choices', None)
        self.value_type = kwargs.pop('value_type', None)
        super(MultiSelectField, self).__init__(*args, **kwargs)
        self.max_length = get_max_length(self.choices, self.max_length)
        self.validators[0] = MaxValueMultiFieldValidator(self.max_length)
        if self.max_choices is not None:
            self.validators.append(MaxChoicesValidator(self.max_choices))

    def get_choices_default(self):
        return self.get_choices(include_blank=False)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def validate(self, value, model_instance):
        for opt_select in value:
            if not self.valid_value(opt_select):
                if django.VERSION[0] >= 1 and django.VERSION[1] >= 6:
                    raise exceptions.ValidationError(self.error_messages['invalid_choice'] % {"value": value})
                else:
                    raise exceptions.ValidationError(self.error_messages['invalid_choice'] % value)

    def valid_value(self, value):
        "Check to see if the provided value is a valid choice"
        text_value = force_text(value)
        for k, v in self.get_choices_default():
            if isinstance(v, (list, tuple)):
                # This is an optgroup, so look inside the group for options
                for k2, v2 in v:
                    if value == k2 or text_value == force_text(k2):
                        return True
            else:
                if value == k or text_value == force_text(k):
                    return True
        return False

    def get_default(self):
        default = super(MultiSelectField, self).get_default()
        if isinstance(default, int):
            default = string_type(default)
        return default

    def formfield(self, **kwargs):
        defaults = {'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text,
                    'choices': self.choices,
                    'max_length': self.max_length,
                    'max_choices': self.max_choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def get_prep_value(self, value):
        if value in ('', u'', None):
            return value
        return ",".join(map(str, value))

    def to_python(self, value):
        if value is None:
            return None
        elif not value:
            return []
        else:
            value_list = value if isinstance(value, list) else value.split(',')
            if self.value_type is not None:
                value_list = map(self.value_type, value_list)
            return value_list

    def contribute_to_class(self, cls, name):
        super(MultiSelectField, self).contribute_to_class(cls, name)
        if self.choices:
            def get_display(obj):
                fieldname = name
                choicedict = dict(self.choices)
                display = []
                for value in getattr(obj, fieldname):
                    item_display = choicedict.get(value, None)
                    if item_display is None:
                        try:
                            item_display = choicedict.get(int(value), value)
                        except (ValueError, TypeError):
                            item_display = value
                    item_display = string_type(item_display)
                    if item_display not in ('', u'', None):
                        display.append(item_display)
                return ", ".join(display)
            setattr(cls, 'get_%s_display' % self.name, get_display)

MultiSelectField = add_metaclass(models.SubfieldBase)(MultiSelectField)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^multiselectfield\.db.fields\.MultiSelectField'])
except ImportError:
    pass
