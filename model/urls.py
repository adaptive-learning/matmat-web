from django.conf.urls import patterns, url

urlpatterns = patterns(
    'model.views',
    url(r'^moje_vedomosti/$', "my_skills", name="my_skills"),
    url(r'^moje_vedomosti/user/(?P<user_pk>\d+)$', "my_skills", name="user_skills"),
    url(r'^moje_vedomosti/user/$', "my_skills", name="user_skills"),
    url(r'^moje_vedomosti/(?P<proceed_skill>\d+)$', "my_skills", name="my_skills"),
    url(r'^porovnani_deti/(?P<user_pk>\d+)$', "children_comparison", name="children_comparison"),
    url(r'^skill_detail/(?P<user_pk>\d+)/(?P<skill_pk>\d+)$', "skill_detail", name="skill_detail"),
)