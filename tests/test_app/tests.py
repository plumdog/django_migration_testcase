import unittest

import django
from django.db import IntegrityError
from django.conf import settings

from django_migration_testcase import MigrationTest
from django_migration_testcase.base import InvalidModelStateError, idempotent_transaction


class ExampleMigrationTest(MigrationTest):
    before = '0001_initial'
    after = '0002_mymodel_number'
    app_name = 'test_app'

    def test_migration(self):
        MyModel = self.get_model_before('MyModel')

        for i in range(10):
            mymodel = MyModel()
            mymodel.name = 'example name {}'.format(i)
            mymodel.save()
        self.assertEqual(MyModel.objects.count(), 10)

        self.run_migration()

        MyModel = self.get_model_after('MyModel')
        self.assertEqual(MyModel.objects.count(), 10)

    def test_run_reverse_migration(self):
        MyModel = self.get_model_before('MyModel')

        for i in range(10):
            mymodel = MyModel()
            mymodel.name = 'example name {}'.format(i)
            mymodel.save()
        self.assertEqual(MyModel.objects.count(), 10)

        self.run_migration()

        MyModel = self.get_model_after('MyModel')
        self.assertEqual(MyModel.objects.count(), 10)

        self.run_reverse_migration()

        self.assertEqual(MyModel.objects.count(), 10)

    def test_invalid_field(self):
        MyModel = self.get_model_before('MyModel')
        mymodel = MyModel()
        mymodel.number = 10
        mymodel.save()

        mymodel = MyModel.objects.get()
        with self.assertRaises(AttributeError):
            mymodel.number

        self.run_migration()

        MyModel = self.get_model_after('MyModel')
        mymodel = MyModel.objects.get()
        self.assertEqual(mymodel.number, None)

        mymodel.number = 10
        mymodel.save()

        mymodel = MyModel.objects.get()
        self.assertEqual(mymodel.number, 10)


def field_names(model_class):
    try:
        return model_class._meta.get_all_field_names()
    except AttributeError:
        return [f.name for f in model_class._meta.get_fields()]


class AddDoubleNumberTest(MigrationTest):
    before = '0002_mymodel_number'
    after = '0003_mymodel_double_number'
    app_name = 'test_app'

    def test_migration(self):
        MyModel = self.get_model_before('MyModel')
        self.assertNotIn('double_number', field_names(MyModel))

        self.run_migration()

        MyModel = self.get_model_after('MyModel')
        self.assertIn('double_number', field_names(MyModel))


class MigrationsByNumberOnlyTest(MigrationTest):
    before = '0002'
    after = '0003'
    app_name = 'test_app'

    def test_migration(self):
        MyModel = self.get_model_before('MyModel')
        self.assertNotIn('double_number', field_names(MyModel))

        self.run_migration()

        MyModel = self.get_model_after('MyModel')
        self.assertIn('double_number', field_names(MyModel))


class PopulateDoubleNumberTest(MigrationTest):
    before = '0003_mymodel_double_number'
    after = '0004_populate_mymodel_double_number'
    app_name = 'test_app'

    def test_migration(self):
        MyModel = self.get_model_before('MyModel')

        for i in range(10):
            mymodel = MyModel()
            mymodel.name = 'example name {}'.format(i)
            mymodel.number = i
            mymodel.save()

        self.run_migration()

        MyModel = self.get_model_after('MyModel')
        for mymodel in MyModel.objects.all():
            self.assertEqual(mymodel.number * 2, mymodel.double_number)


class GetModelMigrationTest(MigrationTest):
    before = '0001_initial'
    after = '0002_mymodel_number'
    app_name = 'test_app'

    def test_migration(self):
        MyModel = self.get_model_before('test_app.MyModel')
        self.assertEqual(MyModel.__name__, 'MyModel')

        self.run_migration()

        MyModel = self.get_model_after('test_app.MyModel')
        self.assertEqual(MyModel.__name__, 'MyModel')


class ForeignKeyTest(MigrationTest):
    before = '0004_populate_mymodel_double_number'
    after = '0005_foreignmodel'
    app_name = 'test_app'

    def test_migration(self):
        MyModel = self.get_model_before('test_app.MyModel')
        self.assertEqual(MyModel.__name__, 'MyModel')

        self.run_migration()

        ForeignModel = self.get_model_after('test_app.ForeignModel')
        self.assertEqual(ForeignModel.__name__, 'ForeignModel')

        MyModel = self.get_model_after('test_app.MyModel')
        self.assertEqual(MyModel.__name__, 'MyModel')

        my = MyModel(name='test_my', number=1, double_number=3.14)
        my.save()

        ForeignModel(name='test_foreign', my=my)

    def test_migration2(self):
        """Same test as test_migration, but this one passes."""
        MyModel = self.get_model_before('test_app.MyModel')
        self.assertEqual(MyModel.__name__, 'MyModel')

        self.run_migration()

        ForeignModel = self.get_model_after('test_app.ForeignModel')
        self.assertEqual(ForeignModel.__name__, 'ForeignModel')

        # get_model_before/get_model_after seems to not get the same model as
        # this crazy thing.
        if django.VERSION >= (2, 0):
            MyModel = ForeignModel.my.field.related_model
        else:
            MyModel = ForeignModel.my.field.rel.to
        self.assertEqual(MyModel.__name__, 'MyModel')

        my = MyModel(name='test_my', number=1, double_number=3.14)
        my.save()

        ForeignModel(name='test_foreign', my=my)

    def test_migration_clearly(self):
        """A clear illustration of the problem."""
        self.run_migration()

        ForeignModel = self.get_model_after('test_app.ForeignModel')

        # get_model_before/get_model_after seems to not get the same model as
        # this crazy thing.
        if django.VERSION >= (2, 0):
            MyModel = ForeignModel.my.field.related_model
        else:
            MyModel = ForeignModel.my.field.rel.to
        MyModel2 = self.get_model_after('test_app.MyModel')

        self.assertEqual(MyModel, MyModel2)


class UtilsMigrationTest(MigrationTest):
    before = '0001_initial'
    after = '0002_mymodel_number'
    app_name = 'test_app'

    def test_migration_not_run_exception(self):
        with self.assertRaises(InvalidModelStateError):
            self.get_model_after('MyModel')
        with self.assertRaises(InvalidModelStateError):
            self.run_reverse_migration()

    def test_migration_already_run_exception(self):
        self.run_migration()
        with self.assertRaises(InvalidModelStateError):
            self.get_model_before('MyModel')


class MigrateFromZero(MigrationTest):
    before = 'zero'
    after = '0001_initial'

    app_name = 'test_app'

    def test_model_exists(self):

        with self.assertRaises(LookupError):
            self.get_model_before('MyModel')

        self.run_migration()

        MyModel = self.get_model_after('MyModel')
        self.assertEqual(MyModel.__name__, 'MyModel')


class TeardownCanFail(MigrationTest):
    before = '0006'
    after = '0007'

    app_name = 'test_app'

    def test_second_model_name_is_unique(self):
        model_before = self.get_model_before('MySecondModel')
        model_before.objects.create(name='foo')
        model_before.objects.create(name='foo')
        with self.assertRaises(IntegrityError):
            self.run_migration()

    def tearDown(self):
        self.assertTrue(self.get_model_before('MySecondModel').objects.all().exists())
        with self.assertRaises(IntegrityError):
            # tearDown fails since migrations runs again with the data
            super(TeardownCanFail, self).tearDown()

        self.get_model_before('MySecondModel').objects.all().delete()
        super(TeardownCanFail, self).tearDown()


@unittest.skipIf(django.VERSION < (1, 7), 'Not supported by older django versions')
@unittest.skipIf(django.VERSION >= (2, 0) and settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3',
                 'Not supported with django2 with sqlite3')
class TeardownFailCanBeAvoidedWithIdempotentTransaction(MigrationTest):
    before = '0006'
    after = '0007'

    app_name = 'test_app'

    @idempotent_transaction
    def test_second_model_name_is_unique(self):
        model_before = self.get_model_before('MySecondModel')
        model_before.objects.create(name='foo')
        model_before.objects.create(name='foo')
        with self.assertRaises(IntegrityError):
            self.run_migration()
