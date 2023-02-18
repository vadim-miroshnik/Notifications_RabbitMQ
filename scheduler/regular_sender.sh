#!/bin/bash
curl -X POST "http://$NOTIFICATION_API:$NOTIFICATION_PORT/api/v1/notifications/add-group" \
  -H  "accept: application/json" \
  -H  "Content-Type: application/json" \
  -d "{  \"template_id\": \"$ID_COMMON_GROUP\",  \"group_id\": \"$ID_REGULAR_TEMPLATE\"}" \
  >> /var/log/syslog
