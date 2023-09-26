import boto3 
import os

def extract_from_source():
    session = boto3.Session( 
        aws_access_key_id="****",
        aws_secret_access_key="****"
    )
    
    s3 = session.client("s3")
    bucket_name = "amazon-us-sales-bucket"

    response = s3.list_objects_v2(Bucket=bucket_name)

    write_dir = "/opt/airflow/Input_data"
    for obj in response['Contents']:
        key = obj['Key']

        write_path = os.path.join(write_dir, key)
        with open(write_path, "wb") as file:
            s3.download_fileobj(bucket_name, key, file)
