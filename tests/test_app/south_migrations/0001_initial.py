# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MyModel'
        db.create_table(u'test_app_mymodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'test_app', ['MyModel'])


    def backwards(self, orm):
        # Deleting model 'MyModel'
        db.delete_table(u'test_app_mymodel')


    models = {
        u'test_app.mymodel': {
            'Meta': {'object_name': 'MyModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['test_app']