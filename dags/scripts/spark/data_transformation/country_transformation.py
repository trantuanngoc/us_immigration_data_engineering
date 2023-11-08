class CountryTransformer:
    def __init__(self, spark):
        self.spark = spark

    def transform(self, country_path, target_path):
        values = self.spark.read.option("header", True).options(delimiter=";").csv(country_path)
        labels = ["origin_country_code", "origin_country"]
        dim_appl_org_country_df = self.spark.createDataFrame(values, labels)
        dim_appl_org_country_df.write.mode("overwrite").parquet(target_path)