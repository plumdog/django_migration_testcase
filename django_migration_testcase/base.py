import functools

import django
from django.db import transaction
from django.conf import settings
from django.test import TransactionTestCase
from django.core.management import call_command


class InvalidModelStateError(Exception):
    pass


def idempotent_transaction(func):
    if django.VERSION < (1, 7,) or django.VERSION >= (2, 0) and settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
        return func
    else:
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            with transaction.atomic():
                sp = transaction.savepoint()
                try:
                    func(*args, **kwargs)
                    transaction.savepoint_rollback(sp)
                except BaseException:
                    raise
        return func_wrapper


class BaseMigrationTestCase(TransactionTestCase):
    __abstract__ = True

    before = None
    after = None
    app_name = None

    def __init__(self, *args, **kwargs):
        super(BaseMigrationTestCase, self).__init__(*args, **kwargs)
        # if self.app_name is None, then assume self.before is a list
        # of 2-tuples. This is more explicit (and easier to document).
        # TODO: add more sanity checks
        if self.app_name:
            self.before = [(self.app_name, self.before)]
            self.after = [(self.app_name, self.after)]

    def tearDown(self):
        # We do need to tidy up and take the database to its final
        # state so that we don't get errors when the final truncating
        # happens.
        for app_name, _ in self.after:
            self.migrate(app_name, version=None)
        super(BaseMigrationTestCase, self).tearDown()

    def setUp(self):
        self._migration_run = False

    def _check_migration_run(self):
        if not self._migration_run:
            raise InvalidModelStateError('Migration(s) not yet run, invalid state requested')

    def _check_migration_not_run(self):
        if self._migration_run:
            raise InvalidModelStateError('Migration(s) already run, invalid state requested')

    def get_model_before(self, model_name):
        raise NotImplementedError()

    def get_model_after(self, model_name):
        raise NotImplementedError()

    def run_migration(self):
        raise NotImplementedError()

    def run_reverse_migration(self):
        raise NotImplementedError()

    def migrate_kwargs(self):
        if django.VERSION >= (2, 0,):
            return {
                'verbosity': 0,
                'interactive': False,
            }
        else:
            return {
                'verbosity': 0,
                'no_initial_data': True,
                'interactive': False,
            }

    def migrate(self, app_name, version, fake=False):
        kwargs = self.migrate_kwargs()
        kwargs['fake'] = fake
        # For Django 1.7 - does a len() check on args.
        if version:
            args = ('migrate', app_name, version)
        else:
            args = ('migrate', app_name)
        call_command(*args, **kwargs)

    def _get_app_and_model_name(self, model_name):
        if '.' in model_name:
            app_name, model_name = model_name.split('.', 2)
        elif self.app_name:
            app_name = self.app_name
        else:
            raise ValueError('Must specify app name')
        return app_name, model_name
