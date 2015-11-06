from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.apps import apps

urlpatterns = [
    # Examples:
    # url(r'^$', 'sanscript.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login, {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', logout, {'next_page': '/'}),
    url(r'^docs/$', 'sanscript.views.home'),
    url(r'^$', 'sanscript.views.home'),
]

for app in apps.get_app_configs():
    if app.name[:5] == 'apps.':
        urlpatterns += [
            url(r'^{}/'.format(app.label), include('apps.{}.urls'.format(app.label))),
            url(r'^{}-sa/'.format(app.label), include('apps.sa.urls')),
        ]
