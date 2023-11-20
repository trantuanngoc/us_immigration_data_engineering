class Transformer:
    def __init__(self, spark):
        self.spark = spark
        
    def transform(self, input_path, output_path, table_name, query_path):
        self.spark.read.option("header", "true").option("delimiter", ",").csv(input_path).createTempView(table_name)
        with open(query_path, 'r') as file:
            sql_query = file.read()
        self.spark.sql(sql_query).write.parquet(output_path)


    