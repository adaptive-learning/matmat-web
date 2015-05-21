from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from django.contrib.auth.views import logout
from questions.views import SimulatorTestView

urlpatterns = patterns('questions.views',
    url(r'^play/$', "play", name="play", kwargs={"skill": "math"}),
    url(r'^play/(?P<skill>\w+)$', "play", name="play"),
    url(r'^play/(?P<skill>\w+)/(?P<pk>.+)$', "play", name="play"),
    url(r'^get_question/$', "get_questions", name="get_question"),
    url(r'^get_selected_question/(?P<question_pk>\d+)$', "get_selected_question", name="get_question"),
    url(r'^get_question_test/$', "get_question_test",),
    url(r'^simulator_test/$', "simulator_test", name="simulator_tester"),
    url(r'^save_answer/$', "save_answer", name="save_answer"),
)