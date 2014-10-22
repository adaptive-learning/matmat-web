from django.core.management import BaseCommand
from model.utils import recalculate_model

class Command(BaseCommand):

    args = ""
    help = "Recalculated model with all answers"

    def handle(self, *args, **options):
        self.stdout.write("Starting recalculation")

        recalculate_model()

        self.stdout.write("Recalculated")