from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from django.contrib.auth.views import logout

urlpatterns = patterns('questions.views',
    # url(r'^$', "home", name="home"),
)