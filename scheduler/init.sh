# 0 17 * * 5
echo "* * * * * NOTIFICATION_API=$NOTIFICATION_API NOTIFICATION_PORT=$NOTIFICATION_PORT bash -c '/opt/app/regular_sender.sh'" | crontab
echo "Starting logs..." > /var/log/syslog
crontab -l
cron
tail -f /var/log/syslog