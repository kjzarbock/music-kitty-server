rm db.sqlite3
rm -rf ./musickittyapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations musickittyapi
python3 manage.py migrate musickittyapi