[![Build Status](https://travis-ci.org/lilleswing/workqueue.svg?branch=master)](https://travis-ci.org/lilleswing/workqueue)
# Workserver
Simple server for logging pleasingly parallel jobs

## Deploy
``` bash
git clone git@github.com:lilleswing/workqueue.git
cd workqueue
conda create --name workqueue -y
source activate workqueue
conda install --yes --file requirements.txt
python manage.py migrate
python manage.py createsuperuser
bash scripts/make_run_server.sh
bash scripts/make_supervisor_conf.sh
```

If you need to over-ride django settings like ALLOWED_HOSTS
you can edit create settings.json in the git-root.

By default it will deploy on port 8003
* To change edit scripts/run_server.sh after first deploy

logs are in /var/log/workserver

## Client

whls located [here](https://karlleswing.com/misc/pypi/workqueue_client/)
```bash
pip install <whl_file>
```

[Usage Examples](https://github.com/lilleswing/workqueue/blob/master/workqueue_client/test_WQClient.py)

## Example
see scripts/examples/example.sh

This walks through an example of hashing an integer distributed.

NOTE that sqlite does not have row level locking so you will not have
the ONLY once semantics
