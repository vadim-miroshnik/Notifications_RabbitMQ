while true
  do
    docker exec mongos1 bash -c 'mongosh --quiet --eval "quit()"' 1>/dev/zero 2>&1
    rc=$?
    if [ $rc -ne 0 ]; then
      echo "Сontinue waiting mongo"
      sleep 2
    else
      break
    fi
  done
