from django.conf.urls import patterns, url

urlpatterns = patterns(
    'model.views',
    url(r'^my_skills/$', "my_skills", name="my_skills"),
)
