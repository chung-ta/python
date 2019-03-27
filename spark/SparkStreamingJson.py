from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, IntegerType, StringType

if __name__ == '__main__':
    spark = SparkSession \
        .builder \
        .config('spark.jars.packages', 'org.apache.spark:spark-streaming_2.11:2.3.1,'
                                   'org.apache.spark:spark-streaming-kafka-0-10_2.11:2.3.1,'
                                   'org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.1,'
                                   'com.datastax.spark:spark-cassandra-connector_2.11:2.3.0') \
        .appName("StructuredKafkaWordCount") \
        .master('local') \
        .getOrCreate()

    schema = StructType().add("gameId", IntegerType()).add("gameKey", StringType())

    gameData = spark.readStream \
        .format("json") \
        .schema(schema) \
        .option("maxFilesPerTrigger", 1) \
        .json("/Users/chung.ta/dev/test/intellj-python/resources/json") \

    query = gameData.writeStream \
        .outputMode("Append") \
        .format('console') \
        .start()

    query.awaitTermination()