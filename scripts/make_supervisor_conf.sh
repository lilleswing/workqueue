#!/usr/bin/env bash
export CUR_DIR=`pwd`
export USER=`whoami`

if [ ! -d /var/log/workserver ]; then
    sudo mkdir /var/log/workserver
    sudo chown $USER:$USER /var/log/workserver
fi

echo "[program:workserver]" >> scripts/workserver.conf
echo "command=/bin/bash scripts/run_server.sh" >> scripts/workserver.conf
echo "directory=$CUR_DIR" >> scripts/workserver.conf
echo "autostart=true" >> scripts/workserver.conf
echo "autorestart=true" >> scripts/workserver.conf
echo "startretries=3" >> scripts/workserver.conf
echo "stderr_logfile=/var/log/workserver/workserver.err.log" >> scripts/workserver.conf
echo "stdout_logfile=/var/log/workserver/workserver.out.log" >> scripts/workserver.conf
echo "user=$USER" >> scripts/workserver.conf

sudo cp scripts/workserver.conf /etc/supervisor/conf.d/workserver.conf
sudo supervisorctl reread
sudo supervisorctl update