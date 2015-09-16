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

        MyModel = self.get_model_before('MyModel')
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
