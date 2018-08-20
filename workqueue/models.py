from django.db import models


class Project(models.Model):
  description = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')


class WorkUnit(models.Model):
  project = models.ForeignKey(Project, on_delete=models.CASCADE)
  key = models.CharField(max_length=200)
  kwargs = models.TextField()
