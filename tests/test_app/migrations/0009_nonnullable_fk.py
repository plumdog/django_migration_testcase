# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0008_nonnullableforeignmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonnullableforeignmodel',
            name='my',
            field=models.ForeignKey(to='test_app.MyModel'),
        ),
    ]
