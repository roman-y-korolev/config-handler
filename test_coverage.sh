#!/usr/bin/env bash

python manage_test_db.py drop
python manage_test_db.py create
py.test --cov --cov-report term-missing --cov-config=.coveragerc
python manage_test_db.py drop

