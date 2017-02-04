"""PiPool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from PiPool import views
from PiPool.forms import LoginForm

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),

    url(r'^pins/$', views.pins, name='pins'),
    url(r'^pins/create$', views.pin_create, name='pin_create'),
    url(r'^pins/create/post$', views.pin_create_post, name='pin_create_post'),
    url(r'^pins/delete/(?P<id>\d+)/$', views.pin_delete, name='pin_delete'),
    url(r'^pins/(?P<id>\d+)/$', views.pin_edit, name='pin_edit'),

    url(r'^pin-set/$', views.pin_set, name='pin_set'),
    url(r'^$', views.dashboard, name='dashboard'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# todo
# edit not populating html inputs fields
# edit & create form validation
# production working correctly - static files not working
# test with relay & thermometer
# add update button to git pull and restart server - alias = 'pipool-server'

