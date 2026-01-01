from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    LongType
)

spark = (
    SparkSession.builder
    .appName("KafkaToBronzeStreaming")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# Event schema (contract from SDK / ingestion API)
event_schema = StructType([
    StructField("event_id", StringType(), False),
    StructField("user_id", StringType(), False),
    StructField("event_type", StringType(), False),
    StructField("experiment_id", StringType(), True),
    StructField("variant", StringType(), True),
    StructField("event_time", LongType(), False)
])

# Read from Kafka
kafka_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "product_events")
    .option("startingOffsets", "latest")
    .load()
)

# Parse Kafka value
bronze_df = (
    kafka_df
    .selectExpr("CAST(value AS STRING) AS json_value")
    .select(from_json(col("json_value"), event_schema).alias("data"))
    .select("data.*")
)

# Write to Bronze layer
(
    bronze_df.writeStream
    .format("parquet")
    .outputMode("append")
    .option(
        "checkpointLocation",
        "s3://practice_bucket/checkpoints/bronze"
    )
    .start(
        "s3://practice_bucket/bronze/events"
    )
    .awaitTermination()
)
