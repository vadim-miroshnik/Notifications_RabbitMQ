#!/bin/bash
echo "0 17 * * 5 NOTIFICATION_API=$NOTIFICATION_API NOTIFICATION_PORT=$NOTIFICATION_PORT ID_COMMON_GROUP=$ID_COMMON_GROUP ID_REGULAR_TEMPLATE=$ID_REGULAR_TEMPLATE bash -c '/opt/app/regular_sender.sh'" | crontab
echo "Starting logs..." > /var/log/syslog
crontab -l
cron
tail -f /var/log/syslog