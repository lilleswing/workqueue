import json

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

  def create_work(self, project_id, kwargs_list):
    """
    :param project_id: int
    :param kwargs_list:
      list of dict, json serializable
      each dict must have key "kwargs"
    :return:
    """
    for elem in kwargs_list:
      if 'kwargs' not in elem:
        raise ValueError("All elements need key kwargs")
    url = "%s/v1/project/%s/create_work" % (self.host, project_id)
    payload = json.dumps(kwargs_list)
    r = requests.post(url, data=payload)
    return r.json()
