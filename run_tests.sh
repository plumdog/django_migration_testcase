#!/bin/bash

if [[ -z $DB_HOST ]]; then
    DB_HOST=localhost
fi

if [[ -z $DB_PORT ]]; then
    DB_PORT=${POSTGRES_5432_TCP:-5432}
fi

function wait_for_port() {
    while ! nc -z "$DB_HOST" "$DB_PORT"; do
        sleep 1
    done
    sleep 5
}

SUCCESS=0

DJANGO_VERSION=$("$VIRTUAL_ENV"/bin/django-admin.py --version)

# A hack so that we run the south tests for django 1.6 and below, but
# the django migration tests for 1.7 and above
if [[ $DJANGO_VERSION == "1.4"* || $DJANGO_VERSION == "1.5"* || $DJANGO_VERSION == "1.6"* ]]; then
    NAME='test_project_*_south'
else
    NAME='test_project_*_django'
fi

for f in $(find tests -type d -name "$NAME"); do
    echo "Tests for $f"
    if [[ $f = *postgresql* ]]; then
        echo "waiting"
        wait_for_port
    fi
    echo "Running"
    if ! (cd "$f" && ./manage.py test test_app test_second_app) ; then
	SUCCESS=1;
    fi
done


exit $SUCCESS
