from django.db import models


class TestModelWithOptGroupField(models.Model):
    CHOICES = (
        ('Opt Group 1', (
            (1, 'First'),
            (2, 'Second'),
        )),
        ('Opt Group 2', (
            (3, 'Third'),
        )),
        (4, 'Fourth')
    )

    optgroup_field = models.CharField(choices=CHOICES, max_length=255)
