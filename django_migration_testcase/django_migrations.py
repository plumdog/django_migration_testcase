import django
from django.test import TransactionTestCase
from django.core.management import call_command
from django.db import connection
from django.db.migrations.loader import MigrationLoader


class MigrationTest(TransactionTestCase):

    __abstract__ = True

    def setUp(self):
        self.apps_before = None
        self.apps_after = None

        super(MigrationTest, self).setUp()
        call_command('migrate', self.app_name, self.before,
                     no_initial_data=True, verbosity=0)

    def tearDown(self):
        super(MigrationTest, self).tearDown()
        call_command('migrate', self.app_name,
                     no_initial_data=True, verbosity=0)

    def _get_apps_for_migration(self, app_label, migration_name):
        loader = MigrationLoader(connection)
        # Resolve shorthand for a migration into the full name.
        migration_name = loader.get_migration_by_prefix(app_label, migration_name).name
        state = loader.project_state((app_label, migration_name))
        if django.VERSION < (1, 8):
            state.render()
        return state.apps

    def _get_app_and_model_name(self, model_name):
        if '.' in model_name:
            return model_name.split('.', 2)
        else:
            return self.app_name, model_name

    def get_model_before(self, model_name):
        app_name, model_name = self._get_app_and_model_name(model_name)
        if not self.apps_before:
            self.apps_before = self._get_apps_for_migration(app_name, self.before)
        return self.apps_before.get_model(app_name, model_name)

    def get_model_after(self, model_name):
        app_name, model_name = self._get_app_and_model_name(model_name)
        if not self.apps_after:
            self.apps_after = self._get_apps_for_migration(app_name, self.after)
        return self.apps_after.get_model(app_name, model_name)

    def run_migration(self):
        call_command('migrate', self.app_name, self.after,
                     no_initial_data=True, verbosity=0)
