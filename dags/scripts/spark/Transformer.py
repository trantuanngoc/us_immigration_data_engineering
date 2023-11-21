class Transformer:
    def __init__(self, spark):
        self.spark = spark
        
    def transform(self, input_path, output_path, table_name, query_path):
        self.spark.read.csv(input_path, header=True, sep=",",  mode="DROPMALFORMED").dropna().dropDuplicates().createTempView(table_name)
        with open(query_path, 'r') as file:
            sql_query = file.read()
        self.spark.sql(sql_query).write.parquet(output_path)