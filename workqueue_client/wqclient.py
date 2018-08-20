import json
import random

import requests


class WQClient(object):
  def __init__(self, host):
    self.host = host

  def ping(self):
    url = "%s/v1/about" % self.host
    r = requests.get(url)
    return r.json()

  def create_project(self, description):
    url = "%s/v1/project" % self.host
    payload = json.dumps({
      'description': description
    })
    r = requests.post(url, data=payload)
    return r.json()

  def get_work(self, project_id):
    """
    :param project_id: int
    :return: dict
    {
      "id":
      "kwargs"
    }
    """
    url = "%s/v1/project/%s/get_work" % (self.host, project_id)
    r = requests.get(url)
    return r.json()

  def create_work(self, project_id, kwargs_list, shuffle=True):
    """
    :param project_id: int
    :param kwargs_list:
      list of dict, json serializable
      each dict must have key "kwargs"
    :param shuffle:  bool
      True by default
      Randomize order of the kwargs_list
    :return:
    """
    for elem in kwargs_list:
      if 'kwargs' not in elem:
        raise ValueError("All elements need key kwargs")
    if shuffle:
      random.shuffle(kwargs_list)
    url = "%s/v1/project/%s/create_work" % (self.host, project_id)
    payload = json.dumps(kwargs_list)
    r = requests.post(url, data=payload)
    return r.json()

  def record_work(self, work_unit):
    """
    :param work_unit:
    {
      "id": int,
      "result": str,
      "logs" str
    }
    :return:
    {
      "id": int,
      "result": str,
      "logs" str,
      "end_date", str(datetime)
      "status", "COMPLETED"
    }
    """
    if 'id' not in work_unit:
      raise ValueError("Work Unit Must have an ID To Save To")
    if 'result' not in work_unit:
      raise ValueError("Work Unit Must have an result, even if empty")
    if 'logs' not in work_unit:
      work_unit['logs'] = ""
    url = "%s/v1/record_work" % self.host
    payload = json.dumps(work_unit)
    r = requests.put(url, data=payload)
    return r.json()

  def get_project_about(self, project_id):
    url = "%s/v1/project/%s" % (self.host, project_id)
    r = requests.get(url)
    return r.json()
