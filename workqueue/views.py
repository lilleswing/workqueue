# Create your views here.
import datetime

from django.http import HttpResponse
from django.utils import timezone
import json

from django.views.decorators.csrf import csrf_exempt

from workqueue.models import Project, WorkUnit


def about(request):
  """
  /v1/about
  :param request:
  :return:
  """
  d = {
    "version": "0.0.1"
  }
  s = json.dumps(d)
  return HttpResponse(s)


@csrf_exempt
def record_work(request):
  """
  /v1/record_work
  :param request:
  PUT with body
  {
    "id": work_unit.id,
    "result": work_unit.result,
    "logs": work_unit.logs
  }
  :return:
  """
  if request.method != 'PUT':
    raise ValueError("Must Be PUT")
  ws_work_unit = json.loads(request.body)
  work_unit = WorkUnit.objects.filter(pk=ws_work_unit['id']).first()
  work_unit.status = WorkUnit.COMPLETED
  work_unit.logs = ws_work_unit['logs']
  work_unit.end_time = timezone.now()
  work_unit.result = ws_work_unit['result']
  work_unit.save()

  ws_work_unit['end_time'] = str(work_unit.end_time)
  ws_work_unit['status'] = work_unit.status
  s = json.dumps(ws_work_unit)
  return HttpResponse(s)


@csrf_exempt
def create_work(request, project_id):
  """
  /v1/project/<project_id/work
  :param request:
  POST with body
  [{
    "kwargs": work_unit.kwargs,
  }]
  :param project_id:
  :return:
  """
  my_project = Project.objects.filter(pk=project_id).first()
  if request.method != 'POST':
    raise ValueError("Must be POST")
  retval = []
  ws_w_units = json.loads(request.body)
  for ws_w_unit in ws_w_units:
    w_unit = WorkUnit(project=my_project, kwargs=ws_w_unit['kwargs'], status=WorkUnit.READY)
    w_unit.save()
    retval.append({
      'id': w_unit.id,
      'kwargs': w_unit.kwargs
    })
  s = json.dumps(retval)
  return HttpResponse(s)


def project_about(request, project_id):
  """
  /v1/project/<project_id/
  :param request:
  :param project_id: int
  :return:
  """
  my_project = Project.objects.filter(pk=project_id).first()
  ready_units = WorkUnit.objects.filter(project=my_project, status=WorkUnit.READY).count()
  running_units = WorkUnit.objects.filter(project=my_project, status=WorkUnit.RUNNING).count()
  complete_units = WorkUnit.objects.filter(project=my_project, status=WorkUnit.COMPLETED).count()
  d = {
    "id": my_project.id,
    "description": my_project.description,
    "ready": ready_units,
    "running": running_units,
    "complete": complete_units,
  }
  s = json.dumps(d)
  return HttpResponse(s)


def get_work(request, project_id):
  """
  /v1/project/<project_id/get_work
  :param request:
  :param project_id:
  :return:
  """
  my_project = Project.objects.get(pk=project_id)
  work_unit = WorkUnit.objects.select_for_update() \
    .filter(project=my_project) \
    .filter(status=WorkUnit.READY).first()
  if work_unit is None:
    d = {
      "exists": False
    }
    s = json.dumps(d)
    return HttpResponse(s)
  work_unit.status = WorkUnit.RUNNING
  work_unit.start_time = timezone.now()
  work_unit.save()
  d = {
    'id': work_unit.id,
    'key': work_unit.key,
    'kwargs': work_unit.kwargs,
    "exists": True
  }
  s = json.dumps(d)
  return HttpResponse(s)


@csrf_exempt
def create_project(request):
  """
  /v1/project
  :param request:
  :return:
  """
  if request.method != 'POST':
    raise ValueError("Must be POST")
  ws_project = json.loads(request.body)

  project = Project(description=ws_project['description'])
  project.save()
  d = {
    'id': project.id,
    'description': project.description
  }
  s = json.dumps(d)
  return HttpResponse(s)
