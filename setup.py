from setuptools import find_packages, setup


setup(
    name='django-migration-testcase',
    version='0.0.15',
    author='Andrew Plummer',
    author_email='plummer574@gmail.com',
    description='For testing migrations in Django',
    url='https://github.com/plumdog/django_migration_testcase',
    packages=find_packages(),
    install_requires=['Django>=1.4'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
