from setuptools import setup

install_requires = [
    'Django'
]

setup(
    name='django-migration-test',
    #packages=['django_migration_test'],
    version='0.0.1',
    author='Andrew Plummer',
    author_email='plummer574@gmail.com',
    url='https://github.com/plumdog/django_migration_test',
    #description='HTML tables for use with the Flask micro-framework',
    install_requires=install_requires,
    test_suite='tests',
)
