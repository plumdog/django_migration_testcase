import unittest
import django
from django_migration_testcase import MigrationTest


class SecondAppMigrationTest(MigrationTest):
    before = '0001_initial'
    after = '0002_mymodel_number'
    app_name = 'test_second_app'

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


class MigrateBothMigrationTest(MigrationTest):
    before = [('test_app', '0001'), ('test_second_app', '0001')]
    after = [('test_app', '0002'), ('test_second_app', '0002')]

    def test_both_migrated(self):
        # Check test_app.MyModel hasn't been migrated
        test_app_MyModel = self.get_model_before('test_app.MyModel')
        mymodel = test_app_MyModel()
        mymodel.number = 10
        mymodel.save()

        mymodel = test_app_MyModel.objects.get()
        with self.assertRaises(AttributeError):
            mymodel.number

        # Check test_second_app.MyModel hasn't been migrated
        test_second_app_MyModel = self.get_model_before('test_second_app.MyModel')
        mymodel = test_second_app_MyModel()
        mymodel.number = 10
        mymodel.save()

        mymodel = test_second_app_MyModel.objects.get()
        with self.assertRaises(AttributeError):
            mymodel.number

        self.run_migration()

        # Check test_app.MyModel has been migrated
        test_app_MyModel = self.get_model_after('test_app.MyModel')
        mymodel = test_app_MyModel.objects.get()
        self.assertEqual(mymodel.number, None)

        mymodel.number = 10
        mymodel.save()

        mymodel = test_app_MyModel.objects.get()
        self.assertEqual(mymodel.number, 10)

        # Check test_second_app.MyModel has been migrated
        test_second_app_MyModel = self.get_model_after('test_second_app.MyModel')
        mymodel = test_second_app_MyModel.objects.get()
        self.assertEqual(mymodel.number, None)

        mymodel.number = 10
        mymodel.save()

        mymodel = test_second_app_MyModel.objects.get()
        self.assertEqual(mymodel.number, 10)


@unittest.skipIf(django.VERSION < (1, 7), 'Not supported by South')
class SecondAppFKToTestAppMigrationTest(MigrationTest):
    """We don't actually migrate anything here, before and after are the
    same. We just check that the model we load can be linked and
    saved, even if they come from different apps.

    See SecondAppFKToTestAppUsingPksMigrationTest for a
    south-supported approach.

    """

    app_name = 'test_second_app'
    before = '0003'
    after = '0003'

    def test_save_and_reload_model(self):
        MyModelSecond = self.get_model_before('test_second_app.MyModel')
        MyModelFirst = self.get_model_before('test_app.MyModel')

        mymodelfirst = MyModelFirst()
        mymodelfirst.save()

        mymodelsecond = MyModelSecond()
        mymodelsecond.my_model = mymodelfirst
        mymodelsecond.save()


class SecondAppFKToTestAppUsingPksMigrationTest(MigrationTest):
    """Copy of SecondAppFKToTestAppMigrationTest but uses pks instead of
    django's orm magic. Also have to declare in before and after the
    migrations for all the models that are used.

    """

    before = [('test_app', '0005'), ('test_second_app', '0003')]
    after = [('test_app', '0005'), ('test_second_app', '0003')]

    def test_save_and_reload_model(self):
        MyModelSecond = self.get_model_before('test_second_app.MyModel')
        MyModelFirst = self.get_model_before('test_app.MyModel')

        mymodelfirst = MyModelFirst()
        mymodelfirst.save()

        mymodelsecond = MyModelSecond()
        mymodelsecond.my_model_id = mymodelfirst.pk
        mymodelsecond.save()


class MigrateFromZero(MigrationTest):
    before = [('test_app', '0002'), ('test_second_app', 'zero')]
    after = [('test_app', '0002'), ('test_second_app', '0001')]

    def test_model_exists(self):
        # Should fail because we have migrated this app back to zero.
        with self.assertRaises(LookupError):
            self.get_model_before('test_second_app.MyModel')

        self.run_migration()

        # But after the migration, it should succeed.
        MyModel = self.get_model_after('test_second_app.MyModel')
        self.assertEqual(MyModel.__name__, 'MyModel')
