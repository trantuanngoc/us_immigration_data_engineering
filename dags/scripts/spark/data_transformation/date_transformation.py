from pyspark.sql import functions as F
from pyspark.sql.functions import udf
import datetime
from datetime import datetime, timedelta
from pyspark.sql import functions as F
from pyspark.sql import types as T

class DateTransformer:
    def __init__(self, spark):
        self.spark = spark
    
    @staticmethod
    @udf(returnType=T.DateType())
    def timestamp_to_date(timestamp):
        try:
            start = datetime(1960, 1, 1)
            return start + timedelta(days=int(float(timestamp)))
        except:
            return None

    def transform(self, immi_file_path, target_path):
        immigration_df = self.spark.read.option("header", True).options(delimiter=",").csv(immi_file_path)

        date_df = immigration_df.select(F.col("arrdate").alias("date")).union(immigration_df.select("depdate")).distinct()

        transformed_df = date_df.withColumn("id", self.timestamp_to_date(F.col("date"))) \
            .withColumn('day', F.dayofmonth('id')) \
            .withColumn('month', F.month('id')) \
            .withColumn('year', F.year('id')) \
            .withColumn('week', F.weekofyear('id')) \
            .withColumn('weekday', F.dayofweek('id'))\
            .select(["id", "day", "month", "year", "week", "weekday"])\
            .dropDuplicates(["id"])
        transformed_df.write.mode("overwrite").parquet(target_path)

