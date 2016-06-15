from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^user/', include('proso_user.urls')),
    url(r'^models/', include('proso_models.urls')),
    url(r'^common/', include('proso_common.urls')),
    url(r'^concepts/', include('proso_concepts.urls', namespace="concepts")),
    url(r'^feedback/', include('proso_feedback.urls')),
    url(r'^tasks/', include('proso_tasks.urls', namespace="tasks")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('social.apps.django_app.urls', namespace='social')),
    url(r'^small_concepts/(?P<skill_identifier>\w+)$', "matmat.views.small_concepts", name='small_concepts'),
    url(r'^.*$', "matmat.views.index", name='index'),
)