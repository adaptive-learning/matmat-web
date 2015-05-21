from django.conf.urls import patterns, url

urlpatterns = patterns(
    'model.views',
    url(r'^my_skills/$', "my_skills", name="my_skills"),
    url(r'^my_skills/user/(?P<user_pk>\d+)$', "my_skills", name="user_skills"),
    url(r'^my_skills/(?P<proceed_skill>\d+)$', "my_skills", name="my_skills"),
)