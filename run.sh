#! /bin/bash

# ensure in base directory
BASEDIR=$(dirname $0)
cd ${BASEDIR}

# activate the backend
pkill -f runserver
cd ./backend
nohup pipenv run python manage.py runserver &
cd ..

# activate the front end
cd ./frontend
npm start

#if [ -z "$1" ] then
#then cd /fronend
#else pipenv run flask run $1 $2
#fi
