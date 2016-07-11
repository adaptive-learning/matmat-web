#!/bin/sh
# deployment script run by Viper server after push

echo "Starting deploy script"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR

#requirements
pip install -r $DIR/requirements.txt

# database
python $DIR/manage.py migrate  --noinput

#js
export PATH=$PATH:/usr/local/bin
npm install
bower install
grunt

# static files
python $DIR/manage.py collectstatic --noinput

# data
python $DIR/manage.py generate_tasks
python $DIR/manage.py load_tasks

