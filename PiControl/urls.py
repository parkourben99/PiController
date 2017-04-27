from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from PiControl import views
from PiControl.forms import LoginForm

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),

    url(r'^update/$', views.update, name='update'),
    url(r'^maintain/update$', views.maintain_update, name='maintain_update'),
    url(r'^maintain/manuel', views.manuel_toggle, name='manuel_toggle'),
    url(r'^get_temp/$', views.get_temp, name='get_temp'),

    url(r'^pins/$', views.pins, name='pins'),
    url(r'^pins/create$', views.pin_create, name='pin_create'),
    url(r'^pins/create/post$', views.pin_post, name='pin_post'),
    url(r'^pins/delete/(?P<id>\d+)/$', views.pin_delete, name='pin_delete'),
    url(r'^pins/(?P<id>\d+)/$', views.pin_edit, name='pin_edit'),

    url(r'^schedule/$', views.schedule, name='schedule'),
    url(r'^schedule/create$', views.schedule_create, name='schedule_create'),
    url(r'^schedule/create/post$', views.schedule_post, name='schedule_post'),
    url(r'^schedule/delete/(?P<id>\d+)/$', views.schedule_delete, name='schedule_delete'),
    url(r'^schedule/(?P<id>\d+)/$', views.schedule_edit, name='schedule_edit'),

    url(r'^pin-set/$', views.pin_set, name='pin_set'),
    url(r'^$', views.dashboard, name='dashboard'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# todo
# fix git update return value / not breaking
# throw error if env not loaded
# load app name into master.html
# refactor views/controller/settings
