#!/bin/bash

SUCCESS=0

# A hack so that we run the south tests for django 1.6 and below, but
# the django migration tests for 1.7 and above
TOXVENV=$(basename "$VIRTUAL_ENV")
if [[ $TOXVENV =~ "django16" || $TOXVENV =~ "django15" || $TOXVENV =~ "django14" ]]; then
    NAME='test_project_*_south'
    APPNAME='test_app_south'
else
    NAME='test_project_*_django'
    APPNAME='test_app'
fi


for f in $(find tests -type d -name "$NAME"); do
    echo "Tests for $f"
    if ! (cd "$f" && ./manage.py test "$APPNAME") ; then
	SUCCESS=1;
    fi
done


exit $SUCCESS
