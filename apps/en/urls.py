from django.conf.urls import include, url
from . import views
from .apps import pages


urlpatterns = [
    url(r'^$', views.home),
]

for page in pages:
    try:
        view = getattr(views, page['view'])
    except:
        view = views.home
    urlpatterns.append(
        url(r'^{}'.format(page['label']), view)
    )
