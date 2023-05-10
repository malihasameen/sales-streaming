#/bin/bash

cd /home/scripts

spark-submit --jars jars/kafka-clients-3.4.0.jar,jars/spark-sql-kafka-0-10_2.12-3.3.0.jar,jars/spark-streaming-kafka-0-10-assembly_2.12-3.3.0.jar,jars/commons-pool2-2.11.1.jar,jars/spark-cassandra-connector_2.12-3.3.0.jar,jars/jsr166e-1.1.0.jar,jars/spark-cassandra-connector-assembly_2.12-3.3.0.jar,jars/mysql-connector-java-8.0.28.jar consumer.py