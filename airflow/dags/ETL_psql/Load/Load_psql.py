import pandas as pd
import psycopg2 
import time
import os 

def load_table(table_name, df, cur):
        df = df.convert_dtypes()
        records = df.to_records(index=False)
        column_names = ', '.join(df.columns)

        s_list = ', '.join(['%s'] * len(df.columns))

        query = f"""
            INSERT INTO {table_name} ({column_names}) VALUES ({s_list});
        """

        cur.executemany(query, records);

        print(f"Successfully insert data to table {table_name}");        

        
def load_schema() :
    # parameters for connecting to postgreSQL database
    connect_params = {
        "host": "postgres",
        "port": 5432,
        "database": "airflow",
        "user": "airflow",
        "password": "airflow"
    }
    
    conn = psycopg2.connect(**connect_params)
    conn.autocommit = True
    cur = conn.cursor()
    
    
    table_order = ['locations', 'customers', 'products', 'sales', 'shipments']
    root_dir = "/opt/airflow/Transformed_data";
    for table in table_order:
        filePath = os.path.join(root_dir, table + ".csv");
        while(os.path.isfile(filePath) != True):
            time.sleep(3)

        df = pd.read_csv(filePath)
        load_table(f"Sale_schema.{table}", df, cur)

    cur.close()
    conn.close()