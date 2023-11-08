from pyspark.sql import functions as fn
import argparse
from pyspark.sql import SparkSession
from data_transformation.country_transformation import CountryTransformer
from data_transformation.date_transformation import DateTransformer
from data_transformation.immigration_transformation import ImmigrationTransformer
from data_transformation.travel_mode_transformation import TravelModeTransformer
from data_transformation.us_city_transformation import USCityTransformer
from data_transformation.us_port_transformation import USPortTransformer
from data_transformation.visa_transformation import VisaTransformer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", type=str, help="HDFS input", default="/movie"
    )
    parser.add_argument(
        "--output", type=str, help="HDFS output", default="/output"
    )
    args = parser.parse_args()
    spark = SparkSession.builder.appName("run emr").getOrCreate()

    USPortTransformer(spark).transform()
    VisaTransformer(spark).transform()
    CountryTransformer(spark).transform()
    TravelModeTransformer(spark).transform()
    DateTransformer(spark).transform()
    USCityTransformer(spark).transform()
    ImmigrationTransformer(spark).transform()