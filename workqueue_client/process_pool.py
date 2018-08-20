import multiprocessing
import sys
from multiprocessing.pool import Pool
from workqueue_client import WQClient
import traceback
import json
import tempfile
import os

import delegator


def run_command(args):
  q, client, project_id, executable = args
  cpu_id = q.get()
  try:
    work_unit = client.get_work(project_id)
    if not work_unit['exists']:
      raise ValueError("Done with work")
    print("work unit: %s" % work_unit['id'])
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8') as fout:
      fout.write(json.dumps(work_unit))
      command = "taskset -c %s python %s %s" % (cpu_id, executable, fout.name)
      print("running %s" % command)
      c = delegator.run(command)
      print(c.err)
      print(c.out)
      results = open(fout.name + "_results", 'r', encoding='utf-8').read()
      logs = open(fout.name + "_logs", 'r', encoding='utf-8').read()
      work_unit['result'] = results
      work_unit['logs'] = logs
      client.record_work(work_unit)
  except:
    traceback.print_exc()
  print("Putting back cpu_id")
  q.put(cpu_id)


def main(n_processors, client, project_id, executable):
  q = multiprocessing.Manager().Queue()
  for i in range(n_processors):
    q.put(i)

  project_about = client.get_project_about(project_id)
  print(project_about)
  argslist = [(q, client, project_id, executable) for i in range(project_about['ready'])]
  pool = Pool(processes=n_processors)
  pool.map(run_command, argslist)


if __name__ == "__main__":
  host = sys.argv[1]
  project_id = sys.argv[2]

  client = WQClient(host=host)
  client.ping()

  executable = sys.argv[3]
  if not os.path.exists(executable):
    raise ValueError("Executable Must Exist and Be Python Script")

  processors = multiprocessing.cpu_count()
  main(processors, client, project_id, executable)
