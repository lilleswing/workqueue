#!/bin/bash
python example_setup.py
export PROJECT_ID=$(cat project_id)
python -m workqueue_client.process_pool http://localhost:8000 $PROJECT_ID example_worker.py