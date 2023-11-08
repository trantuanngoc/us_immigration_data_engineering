from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, StringType
from pyspark.sql import Window

class VisaTransformer:
    def __init__(self, spark):
        self.spark = spark

    def transform(self, immi_file_path, target_path):
        dim_visa_df = self.spark.read.option("delimiter", ";").option("header", True).csv(immi_file_path)

        dim_visa_df = dim_visa_df.select(
            F.col("visatype").alias("visa_type"),
            F.col("visapost").alias("visa_issuer"),
            F.col("I94VISA").alias("visa_category_code").cast(IntegerType()).cast(StringType()),
        ).dropDuplicates()
        dim_visa_df = dim_visa_df.withColumn("visa_category", F.col("visa_category_code"))

        window_visa = Window.orderBy("visa_type")
        dim_visa_df = dim_visa_df.withColumn("visa_id", F.row_number().over(window_visa))
        dim_visa_df.write.mode("overwrite").parquet(target_path)