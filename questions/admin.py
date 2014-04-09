from django.contrib import admin
from questions.models import Simulator, Question


class SimulatorManager(admin.ModelAdmin):
    list_display = ('name', 'note')

class QuestionManager(admin.ModelAdmin):
    list_display = ('player', 'skill', 'data')

admin.site.register(Simulator, SimulatorManager)
admin.site.register(Question, QuestionManager)