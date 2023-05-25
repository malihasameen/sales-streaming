# Sales Streaming Data Pipeline
Note: This setup is for **Windows Subsystems for Linux (WSL)**.

To install WSL just open and run the Command Prompt as administrator and type the following command:

```bash
wsl --install
```

## Overview
- [Overview](#overview)
- [Install Docker and Docker Compose with WSL2](#install-docker-and-docker-compose-with-wsl2)
- [Architecture](#architecture)
  - [Data Ingestion Layer](#data-ingestion-layer)
  - [Message Broker Layer](#message-broker-layer)
  - [Stream Processing Layer](#stream-processing-layer)
  - [Serving Database Layer](#serving-database-layer)
  - [Visualization Layer](#visualization-layer)
- [FastAPI based Ingestion](#fastapi-based-ingestion)
- [Dashboard](#dashboard)
- [Potential Improvements](#potential-improvements)

## Install Docker and Docker Compose with WSL2
Follow this [link](https://nickjanetakis.com/blog/install-docker-in-wsl-2-without-docker-desktop) to install Docker and Docker Compose in WSL2

```bash
# Uninstall older versions of Docker and Docker compose
sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Install Docker, you can ignore the warning from Docker about using WSL
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to the Docker group
sudo usermod -aG docker $USER

# Install Docker Compose v2
sudo apt-get update && sudo apt-get install docker-compose-plugin

# Sanity check that both tools were installed successfully
docker --version
docker compose version

# Using Ubuntu 22.04 or Debian 10 / 11? You need to do 1 extra step for iptables
# compatibility, you'll want to choose option (1) from the prompt to use iptables-legacy.
sudo update-alternatives --config iptables

# Start Docker service
service docker start

# Check if docker was installed properly
docker run hello-world
```

**Docker Service Start, Stop, Status, Restart commands**
```bash
# Start docker service
service docker start

# Docker service status
service docker status

# Docker service stop
service docker stop

# Restart docker service
service docker restart
```

## Architecture
![](/images/sales-streaming-architecture.png)

All applications in this project are containerized into **Docker** containers to easily setup the environment for end to end streaming data pipeline.

The pipeline has following layers:
- Data Ingestion Layer
- Message Broker Layer
- Stream Processing Layer
- Serving Database Layer
- Visualization Layer

Let's review how each layer is doing its job.

### Data Ingestion Layer
A containerized FastAPI based Python application which provides a REST layer on top of kafka producer. User sends a post request to this fastapi application which retrieves the data in json format, performs data validation and ingests this data in Kafka broker.

### Message Broker Layer
Messages from FastAPI based Python application are consumed by kafka broker which is located inside the kafka service container. The first `kafka` service launches the kafka instance and creates a broker. The second `kafka-create topic` service is responsible to create *Order* topic inside the `kafka` instance. The `zookeeper` service is launched before kafka as it is required for its metadata management.

### Stream Processing Layer
A spark application called `spark-streaming` is submitted to spark cluster manager along with the required jars. This application connects to Kafka broker to retrieve messages from *Order* topic, transforms them using Spark Structured Streaming and loads them into Cassandra and Mysql tables. The first query transforms data into format accepted by cassandra table and second query aggregates this data to load into mysql.

**Spark Jars:**

Following are the spark jars required for stream processing:
- commons-pool2-2.11.1.jar
- kafka-clients-3.4.0.jar
- spark-sql-kafka-0-10_2.12-3.3.0.jar
- spark-streaming-kafka-0-10-assembly_2.12-3.3.0.jar
- spark-cassandra-connector_2.12-3.3.0.jar
- spark-cassandra-connector-assembly_2.12-3.3.0.jar
- jsr166e-1.1.0.jar
- mysql-connector-java-8.0.28.jar

The .jar files can easily be downloaded from maven.

### Serving Database Layer
A cassandra database stores and persists raw data and mysql database stores the aggregated data from Spark jobs. The fisrt `cassandra` service is responsible for launching the cassandra instance and second `cassandra-create-ks-topic` creates keyspace and table inside cassandra instance.

### Visualization Layer
The `superset` service launches the superset instance. Superset connects to MySQL database and visualizes sales data to users. The dashboard is refreshed every 10 seconds.

## FastAPI based Ingestion
![](/images/fastapiproducer.png)

## Dashboard
![](/images/dashboard.gif)

## Potential Improvements
There is definitely some room for improvement in this streaming data pipeline.
For example:
- Creating a .env file to have all enviroment variables in one place
- Multi node Spark cluster and multiple kafka brokers
- Deploying docker services inside a Kubernetes cluster
- Code cleanup & further development