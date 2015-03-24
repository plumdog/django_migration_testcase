# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def forwards(apps, schema_editor):
    pass
    # print(repr(apps))
    # print(repr(schema_editor))


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mymodel',
            name='number',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.RunPython(forwards, lambda apps, schema_editor: None)
    ]
