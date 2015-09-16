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

        # if self.app_name is None, then assume self.before is a list
        # of 2-tuples. This is more explicit (and easier to document).
        if self.app_name:
            self.before = [(self.app_name, self.before)]
            self.after = [(self.app_name, self.after)]

        self.before_migrations = []
        for app_name, version in self.before:
            migrations = Migrations(app_name)
            self.before_migrations.append((app_name, migrations.guess_migration(
                self._get_migration_number(version)).name()))
        self.after_migrations = []
        for app_name, version in self.after:
            migrations = Migrations(app_name)
            self.after_migrations.append((app_name, migrations.guess_migration(
                self._get_migration_number(version)).name()))

        self.before_orm = {}
        for app_name, version in self.before_migrations:
            migrations = Migrations(app_name)
            self.before_orm[app_name] = migrations[version].orm()
        self.after_orm = {}
        for app_name, version in self.after_migrations:
            migrations = Migrations(app_name)
            self.after_orm[app_name] = migrations[version].orm()

        for app_name, version in self.before_migrations:
            # Do a fake migration first to update the migration history.
            call_command('migrate', app_name,
                         fake=True, verbosity=0, no_initial_data=True)
            call_command('migrate', app_name, version,
                         verbosity=0, no_initial_data=True)

    def tearDown(self):
        # We do need to tidy up and take the database to its final
        # state so that we don't get errors when the final truncating
        # happens.
        for app_name, _ in self.after:
            call_command('migrate', app_name,
                         verbosity=0, no_initial_data=True)
        super(MigrationTest, self).tearDown()

    def _get_model(self, model_name, orm_dict):
        if '.' in model_name:
            app_name, model_name = model_name.split('.', 2)
        elif self.app_name:
            app_name = self.app_name
        else:
            raise ValueError('Must specify app name')
        # Because we store all the orms for each migration against
        # their app name, lookup the relevant orm state first.
        orm = orm_dict[app_name]
        model_name = '{app_name}.{model_name}'.format(
            app_name=app_name,
            model_name=model_name)
        return orm[model_name]

    def get_model_before(self, model_name):
        return self._get_model(model_name, self.before_orm)

    def get_model_after(self, model_name):
        return self._get_model(model_name, self.after_orm)

    def run_migration(self):
        for app_name, version in self.after_migrations:
            call_command('migrate', app_name, version,
                         verbosity=0, no_initial_data=True)

    def _get_migration_number(self, migration_name):
        # TODO: make this better and report exception
        return migration_name.split('_')[0]
