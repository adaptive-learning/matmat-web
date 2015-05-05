#!/bin/sh
# deployment script run by Viper server after push


echo "Starting deploy script"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR

#requirements
pip install -r $DIR/requirements.txt

# database
python $DIR/manage.py syncdb
python $DIR/manage.py migrate

echo "Changes in question:"
python $DIR/manage.py update_questions
echo "Do not forgot run"
echo "  ./manage.py update_questions --update"
echo "to load ně question"

# static files
python $DIR/manage.py collectstatic --noinput