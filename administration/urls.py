from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from django.contrib.auth.views import logout
from questions.views import SimulatorTestView

urlpatterns = patterns('administration.views',
    url(r'^overview/$', "overview", name="admin-overview"),
    url(r'^skills/$', "skills", name="admin-skills"),
    url(r'^skill-tables/$', "skill_tables", name="admin-skill-tables"),
    url(r'^skill-tables-counts/$', "skill_tables_counts", name="admin-skill-tables-counts"),
)