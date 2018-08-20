# Create your views here.
import datetime

from django.http import HttpResponse
import json

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


def record_work(request):
  """
  /v1/record_work
  :param request:
  :return:
  """
  if request.method != 'POST':
    raise ValueError("Must be a POST")
  ws_work_unit = json.loads(request.body)
  work_unit = WorkUnit.objects.filter(WorkUnit.id == ws_work_unit['id']).first()
  work_unit.status = WorkUnit.COMPLETED
  work_unit.logs = ws_work_unit['logs']
  work_unit.end_time = datetime.datetime.now()
  work_unit.result = ws_work_unit['result']
  work_unit.save()

  ws_work_unit['end_time'] = str(work_unit.end_time)
  ws_work_unit['status'] = work_unit.status
  s = json.dumps(ws_work_unit)
  return json.dumps(s)


def project_about(request, project_id):
  """
  /v1/project/<project_id/
  :param request:
  :param project_id: int
  :return:
  """
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
  /v1/project/<project_id/get_work
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
