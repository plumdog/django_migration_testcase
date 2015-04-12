# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0002_mymodel_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='mymodel',
            name='double_number',
            field=models.IntegerField(null=True),
        ),
    ]
