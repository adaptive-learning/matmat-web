MatMat 
======

Intelligent Web Application for practicing mathematics.


Migration from old version
==========================

python manage.py deletelazyusers (on old system)
python manage.py migrate_data flush
python manage.py migrate_data users profiles
python manage.py migrate_data questions
python manage.py migrate_data answers