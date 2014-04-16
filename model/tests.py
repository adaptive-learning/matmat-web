from django.test import TestCase
from model.models import Skill


class EloTest(TestCase):
    def setUp(self):
        math = Skill.objects.create(name="math")
        addition = Skill.objects.create(name="addition", parent=math)
        multiplication = Skill.objects.create(name="multiplication", parent=math)

