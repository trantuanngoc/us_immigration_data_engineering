from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow import DAG

from datetime import datetime, timedelta 

from ETL_redshift.ETLPsqlS3 import ETL_s3
from ETL_redshift.LoadS3ToRedshift import create_redshift_schema, load_s3_to_redshift
from ETL_psql.Extract.Extract import extract_from_source
from ETL_psql.Transform.TransformCustomers import transform_customers
from ETL_psql.Transform.TransformLocations import transform_locations
from ETL_psql.Transform.TransformShipments import transform_shipments
from ETL_psql.Transform.TransformProducts import transform_products
from ETL_psql.Transform.TransfromSales import transform_sales
from ETL_psql.Load.LoadPsql import load_schema

default_args = {
    'owner' : 'fancol',
    'retries' : 2,
    'retry_delay' : timedelta(minutes = 2)
};

with DAG (
    dag_id = 'ETL_psql_redshift_dag',
    default_args = default_args,
    description = 'ETLx to psql and redshift dag',
    start_date = datetime(2023, 8, 12, 1),
    schedule_interval = '@daily',
    template_searchpath = '/opt/airflow/postgreSQL_setup/'
                           
) as dag :
    Create_psql_schema = PostgresOperator(
        task_id = 'Create_psql_schema',
        postgres_conn_id = 'postgres_sale_db',
        sql = 'create_pgsql_schema.sql'
    )

    Extract_from_source = PythonOperator(
        task_id = 'Extract_from_source',
        python_callable = extract_from_source
    )

    Transform_products = PythonOperator(
        task_id = "Transform_product_df",
        python_callable = transform_products,
        op_kwargs = {"Name" : "products", "filePath" : "products.csv"}
    )

    
    Transform_locations = PythonOperator(
        task_id = "Transform_location_df",
        python_callable = transform_locations,
        op_kwargs = {"Name" : "locations", "filePath" : ""}
    )

    
    Transform_customers = PythonOperator(
        task_id = "Transform_customer_df",
        python_callable = transform_customers,
        op_kwargs = {"Name" : "customers", "filePath" : "customers.csv"}
    )

    
    Transform_sales = PythonOperator(
        task_id = "Transform_sale_df",
        python_callable = transform_sales,
        op_kwargs = {"Name" : "sales", "filePath" : "sales.csv"}
    )

    
    Transform_shipments = PythonOperator(
        task_id = "Transform_shipment_df",
        python_callable = transform_shipments,
        op_kwargs = {"Name" : "shipments", "filePath" : "shipments.csv"}
    )

    Load_psql = PythonOperator(
        task_id = "Load_to_psql",
        python_callable = load_schema
    )

    ETL_s3 = PythonOperator(
        task_id = "ETL_s3",
        python_callable = ETL_s3
    )
    
    Create_redshift_schema = PythonOperator(
        task_id = "Create_redshift_schema",
        python_callable = create_redshift_schema,
        op_kwargs = {"root_dir" : "/opt/airflow/redshift_setup"}  
    )

    Load_s3_redshift = PythonOperator(
        task_id = "Load_s3_redshift",
        python_callable = load_s3_to_redshift
    )

   
    Create_psql_schema >> Extract_from_source >> [Transform_products, Transform_locations, 
                           Transform_customers, Transform_sales, Transform_shipments] >> Load_psql >> ETL_s3 >> Create_redshift_schema >> Load_s3_redshift;
   



