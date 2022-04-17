while IFS="" read -r p || [ -n "$p" ]
do
  echo -n "$p: "
  docker exec kafka /opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --list | grep "$p" >> /dev/null

  if [ $? -eq 0 ]
  then
    echo "Exist."
  else
    echo "Non exist... "
    docker exec kafka /opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --create --replication-factor 1 --partitions 1 --topic "$p"
  fi;

done < producer/topics.txt