#!/usr/bin/env bash
export PORT=8003

if [ -f scripts/run_server.sh ] ; then
    rm scripts/run_server.sh
fi
echo "#!/bin/bash" >> scripts/run_server.sh
echo "export PATH=$PATH" >> scripts/run_server.sh
echo "python manage.py migrate" >> scripts/run_server.sh
echo "gunicorn workserver.wsgi --bind=0.0.0.0:$PORT --workers=3" >> scripts/run_server.sh
