from django.contrib import admin
from questions.models import Simulator, Question, Answer


class SimulatorManager(admin.ModelAdmin):
    list_display = ('name', 'note')


class QuestionManager(admin.ModelAdmin):
    list_display = ("identifier", 'player', 'skill', 'data', "difficulty")

class AnswerManager(admin.ModelAdmin):
    list_display = ('question', 'user', 'log', 'timestamp', 'solving_time', 'correctly_solved')

admin.site.register(Simulator, SimulatorManager)
admin.site.register(Question, QuestionManager)
admin.site.register(Answer, AnswerManager)