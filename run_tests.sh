#!/bin/bash

SUCCESS=0

# A hack so that we only run the south tests for 
TOXVENV=$(basename "$VIRTUAL_ENV")
if [[ $TOXVENV =~ "django16" || $TOXVENV =~ "django15" || $TOXVENV =~ "django14" ]]; then
    NAME='test_project_*_south'
    APPNAME='test_app_south'
else
    NAME='test_project_*_django'
    APPNAME='test_app'
fi

# echo $TOXVENV "|" $NAME "|" $APPNAME


for f in $(find tests -type d -name "$NAME"); do
    echo "Tests for $f"
    if ! (cd "$f" && ./manage.py test "$APPNAME") ; then
	SUCCESS=1;
    fi
done


exit $SUCCESS
