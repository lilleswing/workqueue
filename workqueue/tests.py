import json
from django.test import TestCase
from workqueue.models import Project, WorkUnit
from workqueue.views import about


class ViewsTestCase(TestCase):
  def setUp(self):
    self.project = Project(description="foobar")
    self.project.save()
    for i in range(10):
      wu = WorkUnit(project=self.project, kwargs=i)
      wu.save()

  def test_about(self):
    response = json.loads(about({}).content)
    self.assertTrue('version' in response)
