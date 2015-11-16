from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from django.contrib.auth.views import logout
from core.models import NameUserCreationForm as Form

urlpatterns = patterns('core.views',
    url(r'^$', "home", name="home"),
    url(r'^about$', TemplateView.as_view(template_name="core/about.html"), name="about"),
    url(r'^faq$', TemplateView.as_view(template_name="core/faq.html"), name="faq"),
    url(r'^feedback$', "feedback", name="feedback"),
    url(r'^supervisor_overview$', "supervisor_overview", name="supervisor_overview"),
    url(r'^supervisor_overview/(?P<child_pk>\d+)$', "supervisor_overview", name="edit_child"),
    url(r'^send_child$', "send_child", name="send_child"),
    url(r'^receive_child/(?P<code>\w{10})$', "receive_child", name="receive_child"),
    url(r'^join_supervisor$', "join_supervisor", name="join_supervisor"),
    url(r'^log_as_child/(?P<child_pk>\d+)$', "log_as_child", name="log_as_child"),

    url(r'^playground/$', TemplateView.as_view(template_name="core/playground.html"), name='playground'),

    # authorization
    url(r'^convert/', include('lazysignup.urls'), {"template_name": "core/convert.html", 'form_class': Form}),
    url(r'', include('social_auth.urls')),
    url(r'^close_login_popup/$', TemplateView.as_view(template_name="core/close_login_popup.html"), name='login_popup_close'),
    url(r'^logout/$', logout, {"next_page": "home"}, name='logout'),
    url(r'^ajaxlogin/$', "ajax_login", name='ajax_login'),
)
