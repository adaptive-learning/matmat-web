from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^user/', include('proso_user.urls')),
    url(r'^models/', include('proso_models.urls')),
    url(r'^common/', include('proso_common.urls')),
    url(r'^feedback/', include('proso_feedback.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('social.apps.django_app.urls', namespace='social')),
    url(r'^.*$', "matmat.views.index", name='index'),
)