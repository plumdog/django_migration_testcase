#!/bin/bash

SUCCESS=0

for f in $(find tests -type d -name 'test_project_*'); do
    echo "Tests for $f"
    if ! (cd "$f" && ./manage.py test) ; then
	SUCCESS=1;
    fi
done


exit $SUCCESS
