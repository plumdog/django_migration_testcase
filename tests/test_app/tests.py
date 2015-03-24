from django_migration_test import MigrationTest


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
