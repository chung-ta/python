from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

if __name__ == '__main__':

    spark = SparkSession \
        .builder \
        .config('spark.jars.packages', 'com.datastax.spark:spark-cassandra-connector_2.11:2.3.0') \
        .appName("Spark Python Cassandra Test") \
        .master('local') \
        .getOrCreate()


    kvTableDf = spark.read \
        .format("org.apache.spark.sql.cassandra") \
        .option("spark.cassandra.connection.host", "localhost") \
        .options(table="kv", keyspace="test") \
        .load()

    kvTableDf.show()

    kv1TableDf = spark.read \
        .format("org.apache.spark.sql.cassandra") \
        .options(table="kv1", keyspace="test") \
        .load()

    kv1TableDf.show()

    kvTableDf.createOrReplaceTempView("kv_sql_df")
    kvSqlDf = spark.sql('Select * from kv_sql_df where key=\'key1\'')

    print('SQL DF')
    kvSqlDf.show()

    print("Select from Cassandra using where")

    dfCass = spark.read \
        .format("org.apache.spark.sql.cassandra") \
        .options(table="kv1", keyspace="test", pushdown="true") \
        .load() \
        .filter("value='33'")
    dfCass.show()

