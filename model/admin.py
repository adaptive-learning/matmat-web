from django.contrib import admin
from model.models import Skill

class SkillManager(admin.ModelAdmin):
    exclude = ('level',)
    list_display = ('name', 'parent', 'level', 'note')


admin.site.register(Skill, SkillManager)
