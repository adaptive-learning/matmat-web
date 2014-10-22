from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from django.contrib.auth.views import logout
from questions.views import SimulatorTestView

urlpatterns = patterns('administration.views',
    url(r'^overview/$', "overview", name="admin-overview"),
)