from django.contrib import admin
from questions.models import Player, Question


class PlayerManager(admin.ModelAdmin):
    list_display = ('name', 'note')

class QuestionManager(admin.ModelAdmin):
    list_display = ('player', 'skill', 'data')

admin.site.register(Player, PlayerManager)
admin.site.register(Question, QuestionManager)