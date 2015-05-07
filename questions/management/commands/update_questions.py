import json
from optparse import make_option
from django.core.management import BaseCommand, CommandError
from django.db.models import Q
from model.models import Skill
from questions.models import Question, Simulator


class Command(BaseCommand):
    help = 'Load question from JSON'

    option_list = BaseCommand.option_list + (
        make_option(
            '--update',
            dest='update',
            default=False,
            action="store_true",
            help='Update database'),
        make_option(
            '--force',
            dest='force',
            default=False,
            action="store_true",
            help='Update database identifiers'),
    )

    def handle(self, *args, **options):
        skills = json.load(open("questions/migrations/skills.json"))
        questions = json.load(open("questions/migrations/questions.json"))
        simulators = json.load(open("questions/migrations/simulators.json"))
        id_map = json.load(open("questions/migrations/id_map.json"))

        self.stdout.write("SKILLS")
        self.stdout.write("json: {}, db: {}".format(len(skills), Skill.objects.all().count()))
        for skill in skills:
            try:
                db_skill = Skill.objects.get(name=skill["name"])
                changed = False
                if db_skill.note != skill["note"]:
                    self.stdout.write("Updating skill note {}->{}".format(db_skill.note, skill["note"]))
                    db_skill.note = skill["note"]
                    changed = True
                if db_skill.parent and db_skill.parent.name != skill["parent"]:
                    self.stdout.write("Updating skill parent {}->{}".format(db_skill.parent.name, skill["parent"]))
                    try:
                        db_skill.parent = Skill.objects.get(name=skill["parent"])
                        changed = True
                    except Skill.DoesNotExist:
                        raise CommandError("Parent {} not found".format(skill["parent"]))
                if changed and options["update"]:
                    db_skill.save()

            except Skill.DoesNotExist:
                self.stdout.write("Create {}".format(skill))
                if options["update"]:
                    try:
                        Skill.objects.create(
                            name=skill["name"],
                            note=skill["note"],
                            parent=None if skill["parent"] is None else Skill.objects.get(name=skill["parent"])
                        )
                    except Skill.DoesNotExist:
                        raise CommandError("Parent {} not found".format(skill["parent"]))

        self.stdout.write("SIMULATORS")
        self.stdout.write("json: {}, db: {}".format(len(simulators), Simulator.objects.all().count()))
        for simulator in simulators:
            try:
                db_simulator = Simulator.objects.get(name=simulator["name"])
                changed = False
                if db_simulator.note != simulator["note"]:
                    self.stdout.write("Updating simulator note {}->{}".format(db_simulator.note, simulator["note"]))
                    db_simulator.note = simulator["note"]
                    changed = True
                if changed and options["update"]:
                    db_simulator.save()

            except Simulator.DoesNotExist:
                self.stdout.write("Create {}".format(simulator))
                if options["update"]:
                    Simulator.objects.create(
                        name=simulator["name"],
                        note=simulator["note"],
                    )

        self.stdout.write("QUESTIONS")
        self.stdout.write("json: {}, db: {}".format(len(questions), Question.objects.all().count()))
        for question in questions:
            try:
                db_question = Question.objects.get(Q(identifier=question["id"]) | Q(identifier__isnull=True, id=id_map[question["id"]]))
                changed = False
                if json.loads(db_question.data) != json.loads(question["data"]):
                    self.stdout.write("Updating question {} data {}->{}".format(question["id"], db_question.data, question["data"]))
                    db_question.data = question["data"]
                    changed = True
                if db_question.value != question["value"]:
                    self.stdout.write("Updating question {} value {}->{}".format(question["id"], db_question.value, question["value"]))
                    db_question.value = question["value"]
                    changed = True
                if db_question.active != question["active"]:
                    self.stdout.write("Updating question {} active {}->{}".format(question["id"], db_question.active, question["active"]))
                    db_question.active = question["active"]
                    changed = True
                if db_question.player.name != question["player"]:
                    self.stdout.write("Updating question {} player {}->{}".format(question["id"], db_question.player.name, question["player"]))
                    try:
                        db_question.player = Simulator.objects.get(name=question["player"])
                        changed = True
                    except Skill.DoesNotExist:
                        raise CommandError("Player {} not found".format(question["player"]))
                if db_question.skill.name  != question["skill"]:
                    self.stdout.write("Updating question skill {}->{}".format(db_question.skill.name, question["skill"]))
                    try:
                        db_question.skill = Skill.objects.get(name=question["skill"])
                        changed = True
                    except Skill.DoesNotExist:
                        raise CommandError("Skill {} not found".format(question["parent"]))
                if options["force"] or changed and options["update"]:
                    if options["force"]:
                        db_question.identifier = question["id"]
                    db_question.save()

            except (Question.DoesNotExist, KeyError) as e:
                self.stdout.write("Create {}".format(question))
                if options["update"]:
                    try:
                        Question.objects.create(
                            identifier=question["id"],
                            data=question["data"],
                            player=Simulator.objects.get(name=question["player"]),
                            skill=Skill.objects.get(name=question["skill"]),
                            active=question["active"],
                            type=question["type"],
                            )
                    except Skill.DoesNotExist:
                        raise CommandError("Skill {} not found".format(question["skill"]))
                    except Simulator.DoesNotExist:
                        raise CommandError("Simulator{} not found".format(question["player"]))