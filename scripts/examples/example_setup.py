from workqueue_client import WQClient


def setup_work(client):
  project = client.create_project("Hash Test")

  kwargs_list = [{"kwargs": "%s" % i} for i in range(10)]
  response = client.create_work(project['id'], kwargs_list)
  with open('project_id', 'w') as fout:
    fout.write(str(project['id']))


if __name__ == "__main__":
  client = WQClient(host='http://localhost:8000')
  setup_work(client)
