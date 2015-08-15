from django.test import TransactionTestCase
from django.core.management import call_command

from south.migration import Migrations


class MigrationTest(TransactionTestCase):
    """Test for migrations, reworked from:
    https://micknelson.wordpress.com/2013/03/01/testing-django-migrations/

    """

    __abstract__ = True

    before = None
    after = None
    app_name = None

    def setUp(self):
        super(MigrationTest, self).setUp()
        migrations = Migrations(self.app_name)
        self.before = migrations.guess_migration(
            self._get_migration_number(self.before)).name()
        self.after = migrations.guess_migration(
            self._get_migration_number(self.after)).name()

        self.before_orm = migrations[self.before].orm()
        self.after_orm = migrations[self.after].orm()

        # Do a fake migration first to update the migration history.
        call_command('migrate', self.app_name,
                     fake=True, verbosity=0, no_initial_data=True)
        call_command('migrate', self.app_name, self.before,
                     verbosity=0, no_initial_data=True)

    def tearDown(self):
        # We do need to tidy up and take the database to its final
        # state so that we don't get errors when the final truncating
        # happens.
        call_command('migrate', self.app_name,
                     verbosity=0, no_initial_data=True)
        super(MigrationTest, self).tearDown()

    def get_model_before(self, model_name):
        if '.' in model_name:
            return self.before_orm[model_name]
        else:
            return getattr(self.before_orm, model_name)

    def get_model_after(self, model_name):
        if '.' in model_name:
            return self.after_orm[model_name]
        else:
            return getattr(self.after_orm, model_name)

    def run_migration(self):
        call_command('migrate', self.app_name, self.after,
                     verbosity=0, no_initial_data=True)

    def _get_migration_number(self, migration_name):
        # TODO: make this better and report exception
        return migration_name.split('_')[0]
