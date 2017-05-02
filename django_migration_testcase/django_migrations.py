import django
from django.db import connection
from django.db.migrations.loader import MigrationLoader

from .base import BaseMigrationTestCase


class MigrationTest(BaseMigrationTestCase):

    def setUp(self):
        self.apps_before = None
        self.apps_after = None

        super(MigrationTest, self).setUp()
        for app_name, version in self.before:
            self.migrate(app_name, version)

    def _get_apps_for_migration(self, migration_states):
        loader = MigrationLoader(connection)
        full_names = []
        for app_name, migration_name in migration_states:
            if migration_name != 'zero':
                migration_name = loader.get_migration_by_prefix(app_name, migration_name).name
                full_names.append((app_name, migration_name))
        state = loader.project_state(full_names)
        if django.VERSION < (1, 8):
            state.render()
        return state.apps

    def _get_model(self, model_name, before=True):
        app_name, model_name = self._get_app_and_model_name(model_name)
        if before:
            if not self.apps_before:
                self.apps_before = self._get_apps_for_migration(self.before)
            return self.apps_before.get_model(app_name, model_name)
        else:
            if not self.apps_after:
                self.apps_after = self._get_apps_for_migration(self.after)
            return self.apps_after.get_model(app_name, model_name)

    def run_migration(self):
        for app_name, version in self.after:
            self.migrate(app_name, version)
        self._migration_run = True

    def run_reverse_migration(self):
        self._check_migration_run()
        for app_name, version in self.before:
            self.migrate(app_name, version)
        self._migration_run = False

    def get_model_before(self, model_name):
        self._check_migration_not_run()
        return self._get_model(model_name, before=True)

    def get_model_after(self, model_name):
        self._check_migration_run()
        return self._get_model(model_name, before=False)
