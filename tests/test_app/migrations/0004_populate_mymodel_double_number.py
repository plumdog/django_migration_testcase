# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def forwards(apps, schema_editor):
    MyModel = apps.get_model("test_app", "MyModel")
    MyModel.objects.update(double_number=models.F('number') * 2)


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0003_mymodel_double_number'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards)
    ]
