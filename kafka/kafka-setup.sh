#/bin/bash

sleep 10

/opt/bitnami/kafka/bin/kafka-topics.sh --create --if-not-exists --topic $TOPIC_NAME --replication-factor 1 --partitions 1 --bootstrap-server 172.18.0.4:9092
echo "topic $TOPIC_NAME was created"