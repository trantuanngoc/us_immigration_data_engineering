from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql import functions as F


class CountryTransformer:
    def __init__(self, spark):
        self.spark = spark

    def transform(self, immi_file_path, target_path):
        immigration_df = self.spark.read.option("header", True).options(delimiter=",").csv(immi_file_path)

        transformed_df = immigration_df.groupBy(F.col("Country").alias("country")).agg(
            F.round(F.mean('AverageTemperature'), 2).alias("average_temperature"),\
            F.round(F.mean("AverageTemperatureUncertainty"),2).alias("average_temperature_uncertainty")
            ).dropna()\
            .withColumn("temperature_id", monotonically_increasing_id()) \
            .select(["temperature_id", "country", "average_temperature", "average_temperature_uncertainty"]) 
        transformed_df.write.mode("overwrite").parquet(target_path)

