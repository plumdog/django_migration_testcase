# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0005_foreignmodel'),
        ('test_second_app', '0002_mymodel_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='mymodel',
            name='my_model',
            field=models.ForeignKey(blank=True, to='test_app.MyModel', null=True, on_delete=models.CASCADE),
        ),
    ]
