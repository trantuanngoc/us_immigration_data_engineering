from pyspark.sql.types import StructType, StructField, IntegerType
from utils import map_column_names
from pyspark.sql import functions as F
from pyspark.sql.types import FloatType, IntegerType, StringType

class ImmigrationTransformer:
    def __init__(self, spark):
        self.spark = spark
    

    def transform(self, imm_path, visa_path, arrival_path, target_path):
        imm_df = self.spark.read.parquet(imm_path)
        visa_df = self.spark.read.parquet(visa_path)
        arriaval_mode_df = self.spark.read.parquet(arrival_path)

        imm_appl_df = (
            imm_df.join(
                F.broadcast(visa_df),
                (imm_df.visatype == visa_df.visa_type)
                & (imm_df.i94visa == visa_df.visa_category_code)
                & (imm_df.visapost == visa_df.visa_issuer),
                how="left",
            )
            .join(
                arriaval_mode_df,
                (imm_df.i94mode == arriaval_mode_df.mode_code)
                & (imm_df.airline == arriaval_mode_df.airline)
                & (imm_df.fltno == arriaval_mode_df.flight_number),
                how="left",
            )
        )
        imm_appl_df = imm_appl_df.select(
            F.col("cicid").alias("file_id").cast(IntegerType()),
            F.col("insnum").alias("ins_number").cast(IntegerType()),
            F.col("admnum").alias("admission_number").cast(IntegerType()),
            F.col("i94bir").alias("applicant_age").cast(IntegerType()),
            F.col("biryear").alias("applicant_birth_year").cast(IntegerType()),
            F.col("gender"),
            F.col("occup").alias("occupation"),
            F.col("visa_id"),
            F.to_date(F.col("dtadfile"), "yyyyMMdd").alias("application_date"),
            F.col("i94port").alias("admission_port_code"),
            F.col("i94addr").alias("arriaval_state_code"),
            F.col("arriaval_mode_id"),
            convert_to_datetime(F.col("arrdate")).alias("arriaval_date"),
            convert_to_datetime(F.col("depdate")).alias("departure_date"),
            F.to_date(F.col("dtaddto"),"MMddyyyy").alias("limit_date"),
            F.col("status_flag_id"),
            F.col("i94cit").alias("birth_country").cast(IntegerType()).cast(StringType()),
            F.col("i94res").alias("residence_country").cast(IntegerType()).cast(StringType())
        )
        imm_appl_df.write.mode("overwrite").parquet(target_path)

    