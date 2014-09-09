from django.db import models
from multiselectfield.db import fields


class TestModel(models.Model):
    CHOICES = (
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third'),
        (4, 'Fourth')
    )
    multivaluefield = fields.MultiSelectField(choices=CHOICES)
    blank_multivaluefield = fields.MultiSelectField(choices=CHOICES, blank=True)
    null_multivaluefield = fields.MultiSelectField(choices=CHOICES, blank=True, null=True)


class TestModelWithOptgroup(models.Model):
    OPTGROUP_CHOICES = (
        ('Opt Group 1', (
            (1, 'First'),
            (2, 'Second'),
        )),
        ('Opt Group 2', (
            (3, 'Third'),
        )),
        (4, 'Fourth')
    )

    optgroup_multivaluefield = fields.MultiSelectField(choices=OPTGROUP_CHOICES)


class TestValueTypeModel(models.Model):
    CHOICES = (
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third'),
        (4, 'Fourth')
    )
    value_type_multivaluefield = fields.MultiSelectField(choices=CHOICES, value_type=int)
