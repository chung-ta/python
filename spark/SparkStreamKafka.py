from pyspark.sql import SparkSession
from pyspark import RDD
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

# https://stackoverflow.com/questions/49861973/run-pyspark-and-kafka-in-jupyter-notebook
if __name__ == '__main__':
    # Set kafka topic
    topic = "test_python_kafka"

    # Set application groupId
    groupId = "myTopic"

    spark = SparkSession \
        .builder \
        .config('spark.jars.packages', 'org.apache.spark:spark-streaming_2.11:2.3.1,'
                                       'org.apache.spark:spark-streaming-kafka-0-10_2.11:2.3.1,'
                                       'org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.1') \
        .appName("StructuredKafkaWordCount") \
        .master('local') \
        .getOrCreate()

    lines = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", topic)\
        .load()\
        .selectExpr("CAST(value AS STRING)")

    # Split the lines into words
    words = lines.select(
        # explode turns each item in an array into a separate row
        explode(
            split(lines.value, ' ')
        ).alias('word')
    )

    # Generate running word count
    wordCounts = words.groupBy('word').count()

    #Start running the query that prints the running counts to the console
    query = wordCounts \
        .writeStream \
        .outputMode('complete') \
        .format('console') \
        .start()

    query.awaitTermination()
