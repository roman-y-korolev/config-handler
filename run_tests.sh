#!/usr/bin/env bash

python manage_test_db.py drop
python manage_test_db.py create
py.test
python manage_test_db.py drop
