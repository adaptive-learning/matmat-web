from django.contrib import admin
from model.models import Skill

class SkillManager(admin.ModelAdmin):
    exclude = ('level', 'children_list')
    list_display = ('name', 'parent', 'level', 'note', 'children_list')


admin.site.register(Skill, SkillManager)
