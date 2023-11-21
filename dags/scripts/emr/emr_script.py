import argparse
from pyspark.sql import SparkSession
from Transformer import Transformer
import json

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

    with open('transformations.json', 'r') as json_file:
        transformations_data = json.load(json_file)

    for transformation in transformations_data["transformations"]:
        transformer.transform(f"{args.input}/immigration.csv", f"{args.output}/immigration.csv", 
            transformation['table_name'], transformation['sql_file'])