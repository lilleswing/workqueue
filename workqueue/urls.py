from django.conf.urls import url

from workqueue import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
]