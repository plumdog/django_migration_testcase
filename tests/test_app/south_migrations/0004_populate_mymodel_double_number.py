# -*- coding: utf-8 -*-
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):
        MyModel = orm.MyModel
        MyModel.objects.update(double_number=models.F('number') * 2)

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'test_app.mymodel': {
            'Meta': {'object_name': 'MyModel'},
            'double_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['test_app']
    symmetrical = True
