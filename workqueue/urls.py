from django.conf.urls import url

from workqueue import views

urlpatterns = [
  url(r'^about$', views.about, name='about'),
  url(r'^record_work$', views.record_work, name='record_work'),
  url(r'^project/(?P<project_id>[0-9]+)$', views.project_about, name='project_about'),
  url(r'^project/(?P<project_id>[0-9]+)/get_work$', views.get_work, name='get_work'),
]