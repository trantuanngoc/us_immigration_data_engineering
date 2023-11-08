from pyspark.sql import functions as F
from pyspark.sql.types import FloatType, IntegerType

class USCityTransformer:
    def __init__(self, spark):
        self.spark = spark

    def transform(self, uscity_file_path, target_path):
        us_city_df = self.spark.read.option("header", True).options(delimiter=";").csv(uscity_file_path)
        us_city_df = us_city_df.groupBy(F.col("State Code").alias("state_code")).agg(
            F.sum("Total Population").cast(IntegerType()).alias("total_population"),
            F.sum("Male Population").cast(IntegerType()).alias("male_population"),
            F.sum("Female Population").cast(IntegerType()).alias("female_population"),
            F.sum("Number of Veterans").cast(IntegerType()).alias("number_of_veterans"),
            F.sum("Foreign-born").cast(IntegerType()).alias("foregin_born"),
            F.avg("Median Age").cast(FloatType()).alias("median_age"),
            F.avg("Average Household Size").cast(FloatType()).alias("average_household_size"),
        )
        us_city_df.write.mode("overwrite").parquet(target_path)


