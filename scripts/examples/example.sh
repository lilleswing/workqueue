#!/bin/bash
python example_setup.py
export PROJECT_ID=$(cat project_id)
python /home/leswing/Documents/workqueue/workqueue_client/process_pool.py http://tentacruel.bb.schrodinger.com:8003 $PROJECT_ID example_worker.py