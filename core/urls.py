from django.conf.urls import patterns,  url, include
from django.views.generic import TemplateView

urlpatterns = patterns('core.views',
    url(r'^$', "home", name="home"),

    # authorization
    url(r'^convert/', include('lazysignup.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^close_login_popup/$', TemplateView.as_view(template_name="core/close_login_popup.html"),
        name='login_popup_close'),
)
