import redshift_connector
import os


def establish_redshift_connection():
    conn = redshift_connector.connect(
        iam=True,
        database='redshift_main_db',
        db_user='fancol',
        password='fancol2356',
        cluster_identifier='fancol-redshift-cluster',
        access_key_id='********',
        secret_access_key='********',
        region='ap-southeast-1'
    );

    conn.autocommit = True
    return conn


def create_redshift_schema(root_dir):
    conn = establish_redshift_connection()
    cur = conn.cursor()

    path = os.path.join(root_dir, "create_redshift_schema.sql")
    with open(path, 'r') as file:
        redshift_sql = file.read()

    redshift_sql = redshift_sql.split(";")
    redshift_sql = [statement + ";" for statement in redshift_sql]

    for idx, statement in enumerate(redshift_sql):
        if (statement == ";"): continue;
        cur.execute(statement);

    print("Create redshift schema successfully")
    cur.close()
    conn.close()


def load_s3_to_redshift():
    conn = establish_redshift_connection()
    cur = conn.cursor()
    table_list = ['customers', 'products', 'locations', 'time', 'shipments', 'sales']
    bucket_name = "fancol-sale-bucket"
    schema = "warehouse_sales"

    for table in table_list:
        query = f"""
            COPY {schema}.{table}
            FROM 's3://{bucket_name}/{table}.csv'
            IAM_ROLE 'arn:aws:iam::814488564245:role/redshift_role'
            FORMAT AS CSV
            IGNOREHEADER 1
            FILLRECORD;
        """

        cur.execute(query)

    cur.close()
    conn.close()