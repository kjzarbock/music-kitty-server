#!/bin/bash

rm db.sqlite3
rm -rf ./musickittyapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations musickittyapi
python3 manage.py migrate musickittyapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata locations
python3 manage.py loaddata cats
python3 manage.py loaddata profiles
python3 manage.py loaddata products
python3 manage.py loaddata catfavorites
python3 manage.py loaddata reservations
python3 manage.py loaddata profileadoptions
