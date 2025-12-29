from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, when

spark = (
    SparkSession.builder
    .appName("BronzeToSilverStreaming")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# Read from Bronze layer
bronze_df = (
    spark.readStream
    .format("parquet")
    .load("s3://<YOUR_BUCKET>/bronze/events")
)

# Silver transformations (business logic)
silver_df = (
    bronze_df
    .filter(
        col("event_type").isin(
            "page_view",
            "feature_exposed",
            "conversion"
        )
    )
    .withColumn(
        "is_experiment_event",
        when(col("experiment_id").isNotNull(), True).otherwise(False)
    )
    .withColumn("event_date", to_date(col("event_time")))
    .select(
        "event_id",
        "user_id",
        "event_type",
        "experiment_id",
        "variant",
        "event_time",
        "event_date",
        "is_experiment_event"
    )
)

(
    silver_df.writeStream
    .format("parquet")
    .outputMode("append")
    .option(
        "checkpointLocation",
        "s3://<YOUR_BUCKET>/checkpoints/silver"
    )
    .partitionBy("event_date")
    .start(
        "s3://<YOUR_BUCKET>/silver/events"
    )
    .awaitTermination()
)
