import argparse
from pyspark.sql import SparkSession
from Transformer import Transformer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", type=str, default="/input"
    )
    parser.add_argument(
        "--output", type=str, default="/output"
    )
    args = parser.parse_args()
    spark = SparkSession.builder.appName("run emr").getOrCreate()
    transformer = Transformer(spark)
    transformer.transform(f"{args.input}/immigration.csv", f"{args.output}/immigration", "immigration_table", "spark_sql/transform_visa_dim.sql")
    transformer.transform(f"{args.input}/airport.csv", f"{args.output}/airport", "airport_table", "spark_sql/transform_us_port_dim.sql")
    transformer.transform(f"{args.input}/demographic.csv", f"{args.output}/demographic", "demographic_table", "spark_sql/transform_us_city_dim.sql")
    transformer.transform(f"{args.input}/immigration.csv", f"{args.output}/immigration", "immigration_table", "spark_sql/transform_travel_mode_dim.sql")
    transformer.transform(f"{args.input}/immigration.csv", f"{args.output}/immigration", "immigration_table", "spark_sql/transform_date_dim.sql")
    transformer.transform(f"{args.input}/temperature.csv", f"{args.output}/temperature", "temp_table", "spark_sql/transform_country_dim.sql")

    