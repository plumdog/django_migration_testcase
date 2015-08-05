from django_migration_test import MigrationTest


class ExampleMigrationTest(MigrationTest):
    before = '0001_initial'
    after = '0002_mymodel_number'
    app_name = 'test_app_south'

    def test_migration(self):
        MyModel = self.get_model_before('MyModel')

        for i in range(10):
            mymodel = MyModel()
            mymodel.name = 'example name {}'.format(i)
            mymodel.save()
        self.assertEqual(MyModel.objects.count(), 10)

        self.run_migration()

        MyModel = self.get_model_before('MyModel')
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
    app_name = 'test_app_south'

    def test_migration(self):
        MyModel = self.get_model_before('MyModel')
        self.assertNotIn('double_number', MyModel._meta.get_all_field_names())

        self.run_migration()

        MyModel = self.get_model_after('MyModel')
        self.assertIn('double_number', MyModel._meta.get_all_field_names())


class PopulateDoubleNumberTest(MigrationTest):
    before = '0003_mymodel_double_number'
    after = '0004_populate_mymodel_double_number'
    app_name = 'test_app_south'

    def test_migration(self):
        MyModel = self.get_model_before('MyModel')

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
