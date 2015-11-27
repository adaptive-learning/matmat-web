from django.conf.urls import patterns, url

urlpatterns = patterns(
    'model.views',
    url(r'^moje_vedomosti/$', "my_skills", name="my_skills"),
    url(r'^moje_vedomosti/user/(?P<user_pk>\d+)$', "my_skills", name="user_skills"),
    url(r'^moje_vedomosti/user/$', "my_skills", name="user_skills"),
    url(r'^moje_vedomosti/(?P<proceed_skill>\d+)$', "my_skills", name="my_skills"),
    url(r'^prehled_deti/$', "children_comparison", name="children_comparison"),
    url(r'^children_comparison/$', "children_comparison", {"as_json": True}, name="children_comparison"),
    url(r'^skill_detail/(?P<user_pk>\d+)/(?P<skill_pk>\d+)$', "skill_detail", name="skill_detail"),
)