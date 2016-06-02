import os
import json
from django.core.management import BaseCommand
from django.db.models import F, Q
from proso.dict import group_keys_by_value_lists
from proso_models.models import Item
from proso_tasks.models import Skill

from matmat import settings


class Command(BaseCommand):
    help = 'Generate concepts'
    data_dir = 'data'

    def __init__(self, stdout=None, stderr=None, no_color=False):
        super().__init__(stdout=None, stderr=None, no_color=False)
        self.action_names = {
            "practice": {"cs": "Procvičovat"},
            "view": {"cs": "Prohlížet"}
        }

        self.tags = {
            "concept": {
                "names": {"cs": "Koncept"},
                "values": {}
            },
            "level": {
                "names": {"cs": "Úroveň"},
                "values": {
                    "0": {"cs": "0"},
                    "1": {"cs": "1"},
                    "2": {"cs": "2"},
                }
            },
        }
        self.concepts = []

    def handle(self, *args, **options):
        self._generate_concepts()
        json.dump({
            'action_names': self.action_names,
            'tags': self.tags,
            'concepts': self.concepts,
        }, open(os.path.join(self.data_dir, 'matmat-concepts.json'), 'w'), indent=4)

    def _generate_concepts(self):
        skills = Skill.objects.filter(~Q(identifier=F('name')), ~Q(identifier__contains='/'), ~Q(identifier__contains='x'))
        skill_map = {skill.item_id: skill for skill in skills}
        root = Skill.objects.get(identifier='math')
        parents = Item.objects.get_parents_graph([s.item_id for s in skills])
        tree = group_keys_by_value_lists(parents)
        for skill in [skill_map[i] for i in tree[root.item_id] if i is not None]:
            self.tags['concept']['values'][skill.identifier] = {'cs': skill.name}

        for skill in skills:
            concept = {
                "query": '[["skill/{}"]]'.format(skill.identifier),
                "tags": [],
                "names": {
                    "cs": skill.name
                },
                "actions": {
                    "practice": {
                        "cs": '{}/practice/{}'.format(settings.LANGUAGE_DOMAINS['cs'], skill.name)
                    },
                    "view": {
                        "cs": '{}/view/{}'.format(settings.LANGUAGE_DOMAINS['cs'], skill.name)
                    }
                }
            }
            if skill != root:
                if skill.item_id in tree[root.item_id]:
                    concept_name = skill.identifier
                    level = 1
                else:
                    concept_name = skill_map[parents[skill.item_id][0]].identifier
                    level = 2
                concept['tags'].append('concept:' + concept_name)
                concept['tags'].append('level:' + str(level))
            else:
                concept['tags'].append('level:0')
            self.concepts.append(concept)
