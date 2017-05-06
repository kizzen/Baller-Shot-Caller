from django.conf.urls import url

from . import views

app_name = 'baller_shot_caller'
urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.user, name='user'),
]