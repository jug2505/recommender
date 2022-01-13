from django.conf.urls import url

from recommender import views

urlpatterns = [
    url(r'^movie/(?P<movie_id>\d+)/$', views.detail, name='detail'),

    url(r'^association_rule/(?P<content_id>\w+)/$', views.get_association_rules_for, name='get_association_rules_for'),

    url(r'^pop/user/(?P<user_id>\w+)/$', views.recs_by_popularity, name='recs_by_popularity'),
    url(r'^cf/user/(?P<user_id>\w+)/$', views.recs_using_collaborative_filtering, name='recs_using_collaborative_filtering'),
    url(r'^svd/user/(?P<user_id>\w+)/$', views.recs_by_svd, name='recs_by_svd'),
    
]
