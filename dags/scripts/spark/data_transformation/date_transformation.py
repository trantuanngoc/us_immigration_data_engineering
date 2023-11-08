from pyspark.sql import functions as F
from utils import convert_to_datetime

class DateTransformer:
    def __init__(self, spark):
        self.spark = spark

    def transform(self, immi_file_path, target_path):
        imm_df = self.spark.read.option("header", True).options(delimiter=";").csv(immi_file_path)
        admission_date_df = imm_df.select(F.to_date(F.col("dtaddto"), "MMddyyyy").alias("date")).distinct()
        added_file_date_df = imm_df.select(F.to_date(F.col("dtadfile"), "yyyyMMdd")).distinct()
        arrival_date_df = imm_df.select(convert_to_datetime(F.col("arrdate"))).distinct()
        departure_date_df = imm_df.select(convert_to_datetime(F.col("depdate"))).distinct()
        date_df = (
            admission_date_df.union(admission_date_df)
            .union(added_file_date_df)
            .union(arrival_date_df)
            .union(departure_date_df)
            .distinct()
        )

        date_df = date_df.select(
            F.col("date"),
            F.year(F.col("date")).alias("year"),
            F.month(F.col("date")).alias("month")
        ).na.drop(subset=["date"])

        date_df.write.mode("overwrite").parquet(target_path)
