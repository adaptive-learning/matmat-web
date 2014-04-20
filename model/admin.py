from django.contrib import admin
from model.models import Skill, UserSkill


class SkillManager(admin.ModelAdmin):
    exclude = ('level', 'children_list')
    list_display = ('name', 'parent', 'level', 'note', 'children_list')


class UserSkillManager(admin.ModelAdmin):
    list_display = ('user', 'skill', 'value')


admin.site.register(Skill, SkillManager)
admin.site.register(UserSkill, UserSkillManager)
