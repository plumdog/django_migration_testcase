from setuptools import find_packages, setup


setup(
    name='django-migration-testcase',
    version='0.0.13',
    author='Andrew Plummer',
    author_email='plummer574@gmail.com',
    description='For testing migrations in Django',
    url='https://github.com/plumdog/django_migration_testcase',
    packages=find_packages(),
    install_requires=['Django>=1.4'])
