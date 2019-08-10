#!/bin/sh

# pkill ssh
if ! nc -z -v -w5 localhost 3306
then
    kill -TERM $(ps aux | grep ssh | grep 2020 | grep 3306 | awk '{print $2}')
    ssh -f -N -p 2020 -L 3306:localhost:3306 arash@86.104.32.100
    echo "PORT 3306 REOPENED!!"
fi

if ! nc -z -v -w5 localhost 5672
then
    kill -TERM $(ps aux | grep ssh | grep 2020 | grep 5672 | awk '{print $2}')
    ssh -f -N -p 2020 -L 5672:localhost:5672 arash@86.104.32.100
    echo "PORT 5672 REOPENED!!"
fi
/home/hami/workspace/ip_checker/venv/bin/python /home/hami/workspace/ip_checker/manage.py dns_ip_updater >> /home/hami/workspace/ip_checker/logs/dns_ip_updater.log 2>&1
