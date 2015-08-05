import django

if django.VERSION >= (1, 7):
    from .django_migrations import MigrationTest
else:
    from .south_migrations import MigrationTest
