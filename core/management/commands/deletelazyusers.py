from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db.models import Count
from model.utils import recalculate_model

class Command(BaseCommand):
    args = 'execute'
    help = "Delete all lazy user without data"

    def handle(self, *args, **options):

        users_to_delete = User.objects.annotate(answers_count=Count("answers"), skills_count=Count("user_skills"))\
            .filter(lazyuser__isnull=False, answers_count=0, skills_count=0, social_auth__isnull=True)

        self.stdout.write("Users to delete: {}".format(users_to_delete.count()))
        for user in users_to_delete:
            self.stdout.write("{0} - {0.first_name} {0.last_name}".format(user))

        if len(args) > 0 and args[0] == "yes":
            users_to_delete.delete()
            self.stdout.write("Deleted")


