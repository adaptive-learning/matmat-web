#!/bin/sh

# script by měl dělat následující
# current_data.json
#  - všechny stávající data
#  - tento soubor by měl být zachován
# old_data.json
#  - zálaho starého current_data.json, kdyby se něco podělalo
#  - když se nic nepodělá může se smazat
# new_data.json
#  - nová data (vůči strému current_data.json)
#  - nejlépe přejmenovat a vytvořit novou migraci, která tyto data zapracuje do databáze
# TODO - hledání upravených dat a smazaných dat

python manage.py dumpdata --indent=4 questions.Simulator questions.Question > questions/migrations/tmp.json
python save.py questions/migrations

python manage.py dumpdata --indent=4 model.Skill > model/migrations/tmp.json
python save.py model/migrations