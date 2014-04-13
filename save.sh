#!/bin/sh
python manage.py dumpdata --indent=4 questions.Simulator questions.Question > questions/migrations/current_data.json
python manage.py dumpdata --indent=4 model.Skill > model/migrations/current_data.json
