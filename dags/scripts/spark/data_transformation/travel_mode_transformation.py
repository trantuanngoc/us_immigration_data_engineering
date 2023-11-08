from pyspark.sql import functions as F
from pyspark.sql.types import FloatType, IntegerType, StringType
from pyspark.sql import Window

class TravelModeTransformer:
    def __init__(self, spark):
        self.spark = spark

    def transform(self, immi_file_path, target_path):
        imm_df = self.spark.read.option("delimiter", ";").option("header", True).csv(immi_file_path)
        arriaval_mode_df = imm_df.select(
            F.col("i94mode").alias("mode_code").cast(IntegerType()).cast(StringType()),
            F.col("airline"),
            F.col("fltno").alias("flight_number"),
        ).dropDuplicates()
        arriaval_mode_df = arriaval_mode_df.withColumn("mode", F.col("mode_code")).replace(mode, subset="mode")

        window_arriaval_mode = Window.orderBy("mode_code")
        arriaval_mode_df = arriaval_mode_df.withColumn("arriaval_mode_id", F.row_number().over(window_arriaval_mode))

        arriaval_mode_df.write.mode("overwrite").parquet(target_path)