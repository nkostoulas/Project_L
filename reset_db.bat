del db.sqlite3
del projectl\migrations\*
del lists\migrations\*
del recommender\migrations\*

python manage.py makemigrations lists
python manage.py makemigrations recommender
python manage.py migrate

python manage.py loaddata lists/fixtures/category_db.json
python manage.py loaddata lists/fixtures/object_db.json
python manage.py loaddata lists/fixtures/user_db.json
python manage.py loaddata lists/fixtures/userprofile_db.json
python manage.py loaddata lists/fixtures/usertoplist_db.json
