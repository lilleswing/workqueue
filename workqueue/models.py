from django.db import models
from django.utils.encoding import smart_text



class Project(models.Model):
  description = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')

  def __repr__(self):
    return smart_text(self.description)

  def __str__(self):
    return smart_text(self.description)

class WorkUnit(models.Model):
  READY = 'READY'
  RUNNING = 'RUNNING'
  COMPLETED = 'COMPLETED'
  project = models.ForeignKey(Project, on_delete=models.CASCADE)
  key = models.CharField(max_length=200)
  kwargs = models.TextField()
  result = models.TextField(null=True)
  status = models.CharField(max_length=200)
  start_time = models.DateTimeField('start_time')
  end_time = models.DateTimeField('end_time')
  logs = models.TextField(null=True)

