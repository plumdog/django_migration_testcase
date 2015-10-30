# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0006_nullableforeignmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nullableforeignmodel',
            name='my',
            field=models.ForeignKey(blank=True, to='test_app.MyModel', null=True),
        ),
    ]
