"""rs_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^movies/', include('movies.urls')),
    url(r'^collect/', include('collector.urls')),
    url(r'^analytics/', include('analytics.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^rec/', include('recommender.urls'))
]
