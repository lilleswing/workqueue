from unittest import TestCase

from workqueue_client.wqclient import WQClient


class TestWQClient(TestCase):
  def setUp(self):
    host = "http://localhost:8000"
    self.client = WQClient(host)

  def test_ping(self):
    resp = self.client.ping()
    self.assertTrue('version' in resp)

  def test_create_project(self):
    project = self.client.create_project("Test Project")
    self.assertTrue("id" in project)
    self.assertTrue("description" in project)

  def test_create_work(self):
    project = self.client.create_project("Test Project")
    self.assertTrue("id" in project)
    self.assertTrue("description" in project)

    kwargs_list = [{"kwargs": "%s"} for i in range(10)]
    response = self.client.create_work(project['id'], kwargs_list)
    self.assertEqual(len(kwargs_list), len(response))
    for elem in response:
      self.assertTrue("id" in elem)

  def test_get_work(self):
    project = self.client.create_project("Test Project")
    self.assertTrue("id" in project)
    self.assertTrue("description" in project)

    kwargs_list = [{"kwargs": "%s"} for i in range(10)]
    response = self.client.create_work(project['id'], kwargs_list)
    self.assertEqual(len(kwargs_list), len(response))
    for elem in response:
      self.assertTrue("id" in elem)

    for i in range(10):
      response = self.client.get_work(project['id'])
      self.assertTrue(response['exists'])
      self.assertTrue('kwargs' in response)
    response = self.client.get_work(project['id'])
    self.assertFalse(response['exists'])

  def test_record_work(self):
    project = self.client.create_project("Test Project")
    self.assertTrue("id" in project)
    self.assertTrue("description" in project)

    kwargs_list = [{"kwargs": "%s"} for i in range(2)]
    response = self.client.create_work(project['id'], kwargs_list)
    self.assertEqual(len(kwargs_list), len(response))
    for elem in response:
      self.assertTrue("id" in elem)

    work_unit = self.client.get_work(project['id'])
    self.assertTrue(work_unit['exists'])
    self.assertTrue('kwargs' in work_unit)
    work_unit['result'] = "Success"

    response = self.client.record_work(work_unit)
    self.assertEqual(response['status'], 'COMPLETED')
    self.assertTrue('end_time' in response)
