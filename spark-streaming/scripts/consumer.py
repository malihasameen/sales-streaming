from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,IntegerType,FloatType,StringType
from pyspark.sql.functions import from_json, col, udf
import uuid

def save_to_cassandra(writeDF, epoch_id):
  print("Printing epoch_id: ")
  print(epoch_id)
  
  writeDF.write \
    .format("org.apache.spark.sql.cassandra")\
    .mode('append')\
    .options(table="order_table", keyspace="order_ks")\
    .save()
  
  print(epoch_id,"saved to Cassandra")

def save_to_mysql(writeDF, epoch_id):
  db_credentials = {
    "user": "root",
    "password": "secret",
    "driver" : "com.mysql.jdbc.Driver"
  }

  print("Printing epoch_id: ")
  print(epoch_id)
  
  writeDF.write \
    .jdbc(
      url="jdbc:mysql://172.18.0.8:3306/sales_db",
      table="sales",
      mode="append",
      properties=db_credentials
    )
  
  print(epoch_id,"saved to mysql")

schema = StructType([
    StructField("customer_id", IntegerType()),
    StructField("source", StringType()),
    StructField("quantity", IntegerType()),
    StructField("total", FloatType()),
    StructField("created_at", StringType()),
])

spark = SparkSession \
    .builder \
    .appName("Spark Kafka Streaming Data Pipeline") \
    .master("local[*]") \
    .config("spark.cassandra.connection.host","172.18.0.5") \
    .config("spark.cassandra.connection.port","9042") \
    .config("spark.cassandra.auth.username","cassandra") \
    .config("spark.cassandra.auth.password","cassandra") \
    .config("spark.driver.host", "localhost")\
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

input_df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "172.18.0.4:9092") \
  .option("subscribe", "Order") \
  .option("startingOffsets", "earliest") \
  .load() 

input_df.printSchema()

expanded_df = input_df \
  .selectExpr("CAST(value AS STRING)") \
  .select(from_json(col("value"),schema).alias("order")) \
  .select("order.*")

uuid_udf = udf(lambda: str(uuid.uuid4()), StringType()).asNondeterministic()
expanded_df = expanded_df.withColumn("uuid", uuid_udf())
expanded_df.printSchema()

# Output to Console
# expanded_df.writeStream \
#   .outputMode("append") \
#   .format("console") \
#   .option("truncate", False) \
#   .start() \
#   .awaitTermination()

query1 = expanded_df.writeStream \
  .trigger(processingTime="15 seconds") \
  .foreachBatch(save_to_cassandra) \
  .outputMode("update") \
  .start()

customers_df = spark.read.csv("customers.csv", header=True, inferSchema=True)
customers_df.printSchema()

sales_df = expanded_df.join(customers_df, expanded_df.customer_id == customers_df.customer_id, how="inner")
sales_df.printSchema()

final_df = sales_df.groupBy("source", "state") \
  .agg({"total":"sum"}).select("source", "state", col("sum(total)").alias("total_sum_amount"))
final_df.printSchema()

# Output to Console
# final_df.writeStream \
#   .trigger(processingTime="15 seconds") \
#   .outputMode("update") \
#   .format("console") \
#   .option("truncate", False) \
#   .start()

query2 = final_df.writeStream \
  .trigger(processingTime="15 seconds") \
  .outputMode("complete") \
  .foreachBatch(save_to_mysql) \
  .start()

query2.awaitTermination()