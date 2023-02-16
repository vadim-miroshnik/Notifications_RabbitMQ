curl -X POST "http://127.0.0.1:8000/api/v1/notifications/add-group" \
  -H  "accept: application/json" \
  -H  "Content-Type: application/json" \
  -d "{  \"template_id\": \"7dfba2c1-4057-4ef7-a85d-452aae23d428\",  \"group_id\": \"9fe7e975-a8e9-4387-9dc3-c92770ffd1cb\"}"