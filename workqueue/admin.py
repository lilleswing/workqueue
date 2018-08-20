# Register your models here.

from django.contrib import admin
from workqueue.models import Project, WorkUnit

admin.site.register(Project)
admin.site.register(WorkUnit)
