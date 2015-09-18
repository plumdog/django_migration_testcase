import django
from django.core.management import call_command
from django.db import connection
from django.db.migrations.loader import MigrationLoader

from .base import BaseMigrationTestCase


class MigrationTest(BaseMigrationTestCase):

    def setUp(self):
        self.apps_before = {}
        self.apps_after = {}

        super(MigrationTest, self).setUp()
        for app_name, version in self.before:
            call_command('migrate', app_name, version,
                         no_initial_data=True, verbosity=0)

    def _get_apps_for_migration(self, app_label, migration_name):
        loader = MigrationLoader(connection)
        # Resolve shorthand for a migration into the full name.
        migration_name = loader.get_migration_by_prefix(app_label, migration_name).name
        state = loader.project_state((app_label, migration_name))
        if django.VERSION < (1, 8):
            state.render()
        return state.apps

    def _get_model(self, model_name, before_or_after, apps_dict):
        app_name, model_name = self._get_app_and_model_name(model_name)
        version = dict(before_or_after)[app_name]
        if app_name not in apps_dict:
            apps_dict[app_name] = self._get_apps_for_migration(app_name, version)
        return apps_dict[app_name].get_model(app_name, model_name)

    def run_migration(self):
        for app_name, version in self.after:
            call_command('migrate', app_name, version,
                         verbosity=0, no_initial_data=True)
        self._migration_run = True

    def get_model_before(self, model_name):
        self._check_migration_not_run()
        return self._get_model(model_name, self.before, self.apps_before)

    def get_model_after(self, model_name):
        self._check_migration_run()
        return self._get_model(model_name, self.after, self.apps_after)
