import json

from django.test import TestCase
from workqueue.models import Project, WorkUnit
from workqueue.views import about, record_work, get_work


class TestRequest(object):
  def __init__(self, method=None, body=None):
    self.method = method
    self.body = bytes(body, encoding='utf-8')


class ViewsTestCase(TestCase):
  def setUp(self):
    self.project = Project(description="foobar")
    self.project.save()
    for i in range(10):
      wu = WorkUnit(project=self.project, status=WorkUnit.READY, kwargs=i)
      wu.save()

  def test_about(self):
    response = json.loads(about({}).content)
    self.assertTrue('version' in response)

  def test_record_work(self):
    wu = WorkUnit.objects.filter(project=self.project).first()
    d = {
      'id': wu.id,
      'result': "success",
      "logs": "All Clear"
    }
    request = TestRequest('PUT', json.dumps(d))
    response = record_work(request)

    wu = WorkUnit.objects.get(pk=wu.id)
    self.assertEqual(wu.result, d['result'])
    self.assertEqual(wu.logs, d['logs'])
    self.assertEqual(wu.status, WorkUnit.COMPLETED)

  def test_get_work(self):
    used_ids = set()
    for i in range(10):
      response = get_work({}, self.project.id)
      response = json.loads(response.content)
      self.assertTrue(response['exists'])
      used_ids.add(response['id'])

    wus = WorkUnit.objects.all()
    for wu in wus:
      self.assertTrue(wu.id in used_ids)
      wu.status = WorkUnit.RUNNING

    for i in range(10):
      response = get_work({}, self.project.id)
      response = json.loads(response.content)
      self.assertFalse(response['exists'])
