from django.conf.urls import url

from movies import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^movie/(?P<movie_id>\d+)/$', views.detail, name='detail'),
    url(r'^search/$', views.search_for_movie, name='search_for_movie'),
    url(r'^userinfo/$', views.get_user_id, name='get_user_id'),
]