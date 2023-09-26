from datetime import datetime, timedelta
from io import BytesIO
import pandas as pd
import subprocess
import psycopg2
import boto3


def setup_psql_connection():
    connect_params = {
        "host": "postgres",
        "port": 5432,
        "database": "airflow",
        "user": "airflow",
        "password": "airflow"
    };

    conn = psycopg2.connect(**connect_params)
    conn.autocommit = True
    return conn


def extract_from_postgre_sql(df_dict):
    conn = setup_psql_connection()
    cur = conn.cursor()

    table_list = ['products', 'sales', 'customers', 'shipments', 'locations']

    for table in table_list:
        column_query = f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'sale_schema'
            AND table_name = '{table}';
        """

        cur.execute(column_query)

        column_list = list(cur.fetchall())
        column_list = [column[0] for column in column_list];

        # Query data
        data_query = f"""
            SELECT * FROM sale_schema.{table};
        """

        cur.execute(data_query);
        df_dict[table] = pd.DataFrame(columns=column_list, data=cur.fetchall());

    cur.close()
    conn.close()



def generate_date():
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2022, 12, 31)

    time_arr = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    time_dict = {}
    time_dict["full_date"] = []
    time_dict["day"] = []
    time_dict["month"] = []
    time_dict["year"] = []

    for date in time_arr:
        time_dict['full_date'].append(date.date())
        time_dict['day'].append(date.day)
        time_dict['month'].append(date.month)
        time_dict['year'].append(date.year)

    return time_dict


def joining_df(df_1, df_2, left, right):
    return df_1.merge(df_2, left_on=left, right_on=right, how='inner')


def drop_col_df(df, column_list):
    df.drop(columns=column_list, inplace=True)


def transform(df_dict):
    df_dict['time'] = pd.DataFrame(generate_date());

    df_to_join = df_dict['shipments'][['order_id', 'shipment_id', 'shipping_cost', 'shipping_zipcode']];
    df_dict['sales'] = joining_df(df_dict['sales'], df_to_join, 'order_id', 'order_id');

    df_to_join = df_dict['shipments'][['shipping_zipcode', 'shipping_address']];
    df_dict['locations'] = joining_df(df_dict['locations'], df_to_join, 'postal_code', 'shipping_zipcode');

    drop_col_df(df_dict['customers'], ['address', 'postal_code']);
    drop_col_df(df_dict['products'], ['sell_price', 'commision_rate', 'commision']);
    drop_col_df(df_dict['shipments'], ['shipping_date', 'shipping_address', 'order_id',
                                       'shipping_zipcode', 'shipping_cost']);
    drop_col_df(df_dict['locations'], ['shipping_zipcode']);

    df_dict['sales'].rename(columns={"order_id": "sale_id", "total_cost": "revenue"}, inplace=True);

    df_dict['sales'] = df_dict['sales'][['sale_id', 'revenue', 'profit', 'quantity', 'shipping_cost',
                                         'product_id', 'customer_id', 'shipping_zipcode', 'order_date', 'shipment_id']];




def load_df_s3(s3, bucket_name, df, key):
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    s3.upload_fileobj(csv_buffer, bucket_name, key + ".csv")


def load_s3(df_dict):
    session = boto3.Session(
        aws_access_key_id="****",
        aws_secret_access_key="****"
    );

    s3 = session.client("s3");
    bucket_name = "fancol-sale-bucket"

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        for obj in response['Contents']:
            key = obj['Key']
            s3.delete_object(Bucket=bucket_name, Key=key)
    except:
        pass

    for table, df in df_dict.items():
        print(f"Loading {table} to s3")
        load_df_s3(s3, bucket_name, df, table)
        print("Load successfully \n")


def ETL_s3():
    pd.set_option('display.max_columns', None)
    df_dict = {}
    extract_from_postgre_sql(df_dict)
    transform(df_dict)
    load_s3(df_dict)
