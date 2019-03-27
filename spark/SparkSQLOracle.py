from pyspark.sql import SparkSession

if __name__ == '__main__':

    ## Need to edit spark-defaults.conf add - spark.driver.extraClassPath /Users/chung.ta/dev/apps/ojdbc6-11.2.0.4.jar

    spark = SparkSession \
        .builder \
        .appName("Spark Python Oracle Test") \
        .master('local') \
        .getOrCreate()

    channels = spark.read\
        .format("jdbc") \
        .option("url", "jdbc:oracle:thin:@(DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=vmtestdb01)(PORT=1521))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=NWEBT)))") \
        .option("dbtable", "CHANNEL") \
        .option("user", "test_user") \
        .option("password", "test_password") \
        .option("driver", "oracle.jdbc.driver.OracleDriver") \
        .load()

    print('******* --------- channels: ')
    channels.show()

    channels.createOrReplaceTempView("channels")
    channelSQLDf = spark.sql('select * from channels where id=24960')

    print('******* --------- channels where id=24960 ')

    channelSQLDf.show()

    query = '(select * from test_table where season_id=2016) schedules'
    schedules = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:oracle:thin:@(DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=vmtestdb01)(PORT=1521))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=NWEBT)))") \
        .option("dbtable", query) \
        .option("user", "test_user") \
        .option("password", "test_password") \
        .option("driver", "oracle.jdbc.driver.OracleDriver") \
        .load()

    print("----------  Schedules : ")
    schedules.show()