from pyspark.sql import functions as F
from pyspark.sql.types import FloatType

class USPortTransformer:
    def __init__(self, spark):
        self.spark = spark

    def transform(self, state_path, country_path, airport_path, target_path):
        us_states_df = self.spark.read.option("header", True).options(delimiter=";").csv(state_path)
        country_df = self.spark.read.option("header", True).options(delimiter=";").csv(country_path)
        airport_df = self.spark.read.option("header", True).options(delimiter=";").csv(airport_path)

        airport_df = airport_df.where(F.col("type").isin(["small_airport", "medium_airport", "large_airport"]))
        airport_df = (
            airport_df.join(
                F.broadcast(country_df),
                F.col("iso_country") == country_df.country_code,
                how="left",
            )
            .join(
                F.broadcast(us_states_df),
                how="left",
            )
        )

        airport_df = airport_df.select(
            F.col("ident").alias("airport_id"),
            F.col("name").alias("airport_name"),
            F.split(F.col("type"), "_")[0].alias("airport_type"),
            F.col("iata_code"),
            F.col("local_code").alias("municipality_code"),
            F.col("municipality").alias("municipality"),
            F.col("state").alias("region"),
            F.col("country_code"),
            F.col("country"),
            F.col("Code").alias("continent_code"),
            F.col("Continent name").alias("continent"),
            F.col("elevation_ft").cast(FloatType()),
            F.split(F.col("coordinates"), ", ")[1].cast(FloatType()).alias("latitude"),
            F.split(F.col("coordinates"), ", ")[0].cast(FloatType()).alias("longitude"),
        )
        airport_df.write.mode("overwrite").parquet(target_path)