from django.db import IntegrityError

from django_migration_testcase import MigrationTest
from django_migration_testcase.base import InvalidModelStateError


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


class AddDoubleNumberTest(MigrationTest):
    before = '0002_mymodel_number'
    after = '0003_mymodel_double_number'
    app_name = 'test_app'

    def test_migration(self):
        MyModel = self.get_model_before('MyModel')
        self.assertNotIn('double_number', MyModel._meta.get_all_field_names())

        self.run_migration()

        MyModel = self.get_model_after('MyModel')
        self.assertIn('double_number', MyModel._meta.get_all_field_names())


class MigrationsByNumberOnlyTest(MigrationTest):
    before = '0002'
    after = '0003'
    app_name = 'test_app'

    def test_migration(self):
        MyModel = self.get_model_before('MyModel')
        self.assertNotIn('double_number', MyModel._meta.get_all_field_names())

        self.run_migration()

        MyModel = self.get_model_after('MyModel')
        self.assertIn('double_number', MyModel._meta.get_all_field_names())


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

    def test_migration_already_run_exception(self):
        self.run_migration()
        with self.assertRaises(InvalidModelStateError):
            self.get_model_before('MyModel')


class NullableFkTest(MigrationTest):
    before = '0006'
    after = '0007'
    app_name = 'test_app'

    def test_becomes_nullable(self):
        NullableForeignModel = self.get_model_before('NullableForeignModel')
        MyModel = self.get_model_before('MyModel')

        my_model = MyModel.objects.create(
            name='testname',
            number=1,
            double_number=2)
        nullable_foreign_model = NullableForeignModel.objects.create(
            name='foreign_name',
            my=my_model)

        with self.assertRaises(ValueError):
            nullable_foreign_model.my = None

        self.run_migration()

        NullableForeignModel = self.get_model_after('NullableForeignModel')
        nullable_foreign_model = NullableForeignModel.objects.get()

        nullable_foreign_model.my = None
        nullable_foreign_model.save()
        self.assertIsNone(nullable_foreign_model.my)


class ReverseNullableFkTest(MigrationTest):
    before = '0007'
    after = '0006'
    app_name = 'test_app'

    def test_becomes_non_nullable(self):
        NullableForeignModel = self.get_model_before('NullableForeignModel')

        nullable_foreign_model = NullableForeignModel.objects.create(
            name='foreign_name',
            my=None)
        self.assertIsNone(nullable_foreign_model.my)

        MyModel = self.get_model_before('MyModel')
        my_model = MyModel.objects.create(
            name='testname',
            number=1,
            double_number=2)
        nullable_foreign_model.my = my_model
        nullable_foreign_model.save()

        self.run_migration()

        NullableForeignModel = self.get_model_after('NullableForeignModel')
        nullable_foreign_model = NullableForeignModel.objects.get()

        with self.assertRaises(ValueError):
            nullable_foreign_model.my = None

    def test_becomes_non_nullable_migration_error(self):
        NullableForeignModel = self.get_model_before('NullableForeignModel')

        nullable_foreign_model = NullableForeignModel.objects.create(
            name='foreign_name',
            my=None)
        self.assertIsNone(nullable_foreign_model.my)

        with self.assertRaises(IntegrityError):
            self.run_migration()


class NonNullableFkTest(MigrationTest):
    before = '0008'
    after = '0009'
    app_name = 'test_app'

    def test_becomes_non_nullable(self):
        NonNullableForeignModel = self.get_model_before('NonNullableForeignModel')

        non_nullable_foreign_model = NonNullableForeignModel.objects.create(
            name='foreign_name',
            my=None)
        self.assertIsNone(non_nullable_foreign_model.my)

        MyModel = self.get_model_before('MyModel')
        my_model = MyModel.objects.create(
            name='testname',
            number=1,
            double_number=2)
        non_nullable_foreign_model.my = my_model
        non_nullable_foreign_model.save()

        self.run_migration()

        NonNullableForeignModel = self.get_model_after('NonNullableForeignModel')
        non_nullable_foreign_model = NonNullableForeignModel.objects.get()

        with self.assertRaises(ValueError):
            non_nullable_foreign_model.my = None

    def test_becomes_non_nullable_migration_error(self):
        NonNullableForeignModel = self.get_model_before('NonNullableForeignModel')

        non_nullable_foreign_model = NonNullableForeignModel.objects.create(
            name='foreign_name',
            my=None)
        self.assertIsNone(non_nullable_foreign_model.my)

        with self.assertRaises(IntegrityError):
            self.run_migration()


class ReverseNonNullableFkTest(MigrationTest):
    before = '0009'
    after = '0008'
    app_name = 'test_app'

    def test_becomes_nullable(self):
        NonNullableForeignModel = self.get_model_before('NonNullableForeignModel')
        MyModel = self.get_model_before('MyModel')

        my_model = MyModel.objects.create(
            name='testname',
            number=1,
            double_number=2)
        non_nullable_foreign_model = NonNullableForeignModel.objects.create(
            name='foreign_name',
            my=my_model)

        with self.assertRaises(ValueError):
            non_nullable_foreign_model.my = None

        self.run_migration()

        NonNullableForeignModel = self.get_model_after('NonNullableForeignModel')
        non_nullable_foreign_model = NonNullableForeignModel.objects.get()

        non_nullable_foreign_model.my = None
        non_nullable_foreign_model.save()
        self.assertIsNone(non_nullable_foreign_model.my)
