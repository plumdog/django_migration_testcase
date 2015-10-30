# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0005_foreignmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='NullableForeignModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('my', models.ForeignKey(to='test_app.MyModel')),
            ],
        ),
    ]
