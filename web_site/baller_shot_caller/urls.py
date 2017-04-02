from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.user, name='user'),
]