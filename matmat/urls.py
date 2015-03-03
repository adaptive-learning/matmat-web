import debug_toolbar
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from matmat import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('core.urls')),
    url(r'^q/', include('questions.urls')),
    url(r'^m/', include('model.urls')),
    url(r'^a/', include('administration.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^__debug__/', include(debug_toolbar.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)