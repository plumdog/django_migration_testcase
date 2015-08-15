# django_migration_test
For testing migrations in Django >= 1.4 (both South and Django migrations)

Because migrations are important. And if they go wrong, people get
angry. How better to be sure that they won't go wrong than to run
tests.

I found [this article](https://micknelson.wordpress.com/2013/03/01/testing-django-migrations/)
on writing tests around South migrations, which I had used, but as of
Django 1.7, I was out of luck. So I wrote this. It also supports
Django 1.4, 1.5 and 1.6.

This project is very much in its infancy, and I'd be really interested
to know how others get on. Also, if there's a better strategy or
existing library, I'd love to know about it.

Quickstart
----------

```python

from django_migration_test import MigrationTest


class MyMigrationTest(MigrationTest):

    # At present, we can only run migrations for one app at a time.
    app_name = 'my_app'
    # At present, these need to be full names of migrations, not just
    # prefixes.
    before = '0001_initial'
    after = '0002_change_fields'

    # Can have any name, is just a test method. MigrationTest
    # subclasses django.test.TestCase
    def test_migration(self):
        # Load some data. Don't directly import models. At this point,
        # the database is at self.before, and the models have fields
        # set accordingly.

        MyModel = self.get_model_before('MyModel')

        # ... save some models

        # Trigger the migration
        self.run_migration()

        # Now run some assertions based on what the data should now
        # look like. The database will now be at self.after. To run
        # queries via the models, reload the model.

        MyModel = self.get_model_after('MyModel')
```


How it works
------------

In Django's migrations, when writing data migrations, rather than
directly importing models, you load them using `apps.get_model()` --
see
[here](https://docs.djangoproject.com/en/1.7/topics/migrations/#data-migrations).
I've tried to unravel the migrations framework to do the same thing
here, so that we load models dynamically.

Tests
-----

There's a test app that has two migrations. It is linked to two
different projects within the test directory, one that uses postgres,
and one that uses sqlite3. Run the tests with `./run_tests.sh`
