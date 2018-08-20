# Create your views here.
import datetime

from django.http import HttpResponse
import json

from workqueue.models import Project, WorkUnit


def about(request):
  d = {
    "version": "0.0.1"
  }
  s = json.dumps(d)
  return HttpResponse(s)


def project_about(request, project_id):
  my_project = Project.objects.filter(Project.id == project_id).first()
  work_units = WorkUnit.objects.filter(WorkUnit.project == my_project).all()
  d = {
    "id": my_project.id,
    "description": my_project.description,
    "work_units": len(work_units)
  }
  s = json.dumps(d)
  return HttpResponse(s)


def get_work(request, project_id):
  """
  :param request:
  :param project_id:
  :return:
  """
  my_project = Project.objects.filter(Project.id == project_id).first()
  work_unit = WorkUnit.objects.select_for_update() \
    .filter(WorkUnit.project == my_project) \
    .filter(WorkUnit.status == WorkUnit.READY).first()
  if work_unit is None:
    d = {
      "exists": False
    }
    s = json.dumps(d)
    return HttpResponse(s)
  work_unit.status = WorkUnit.RUNNING
  work_unit.start_time = datetime.datetime.now()
  work_unit.save()
  d = {
    'id': work_unit.id,
    'key': work_unit.key,
    'kwargs': work_unit.kwargs,
  }
  s = json.dumps(d)
  return HttpResponse(s)


def index(request):
  projects = Project.objects.all()
  retval = []
  for project in projects:
    d = {
      "id": project.id,
      "description": project.description
    }
    retval.append(d)
  s = json.dumps(retval)
  return HttpResponse(s)
