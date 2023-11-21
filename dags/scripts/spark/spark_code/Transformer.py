from spark.spark_code.Parser import SchemaParser
import json

class Transformer:
    def __init__(self, spark):
        self.spark = spark
        
    def transform(self, input_path, output_path, table_name, schema_path, query_path):
        with open(schema_path, 'r') as f:
            schema_json = json.load(f)
        parser = SchemaParser(schema_json)
        self.spark.read.csv(input_path, header=True, sep=",",  mode="DROPMALFORMED", schema=parser.parse_schema()).dropna().dropDuplicates().createTempView(table_name)
        with open(query_path, 'r') as file:
            sql_query = file.read()
        self.spark.sql(sql_query).write.parquet(output_path)