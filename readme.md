# Batch Processing : ETL pipeline, data modelling and warehousing of Sales data

## Table of Contents
1. [Introduction](#1-introduction)
   - [Technologies used](#technologies-used)
2. [Implementation Overview](#2-implementation-overview)
3. [Design](#3-design)
4. [Project structure](#4-project-structure)
5. [Visualize Result](#7-visualize-result)


## 1. Introduction 
Data is collected from an e-commerce company about their sales in 2022, the company's analytic teams is interested in understanding their business situation in the last year. We will build ETL pipelines which will transform raw data into actionable insights, store them in OLTP database (PostgreSQL) and OLAP database (Amazon Redshift) for enhanced data analytics capabilities.

Data include 4 csv files : <b> <i> Sales, Products, Shipments, Customers. </i> </b>

### Technologies used
- Python
- PostgreSQL
- Airflow
- Terraform (Infrastructure provisioning tool)
- AWS services : S3, Redshift (data warehouse)
- Docker

## 2. Implementation overview 
Design data models for OLTP database (PostgreSQL) and data warehouse (Amazon Redshift). Build an ETL pipeline to transform raw data into actionable insights in PostgreSQL, also store them in S3 for staging. Then implement another ETL pipeline which process data from S3 and load them to Amazon Redshift for enhanced data analytics . Using Airflow to orchestrate pipeline workflow, Terraform for setting up AWS Redshift cluster, and Docker to containerize the project - allow for fast build, test, and deploy project.

<img src = assets/Airflow%20conceptual%20view.png alt = "Airflow conceptual view">

## 3. Design 
<div style="display: flex; flex-direction: column;">
  <img src=assets/Data%20model.png alt="Data model" width="600" height="500">
  <p style="text-align: center;"> <b> <i> Data model for Postgres </i> </b> </p>
</div>

<br> <br>

<div style="display: flex; flex-direction: column;">
  <img src=assets/Star%20schema.png alt="Star schema" width="600" height="500">
  <p style="text-align: center;"> <b> <i> Data model (star schema) for Redshift </i> </b> </p>
</div>

<br> <br>

<div style="display: flex; flex-direction: column;">
  <img src=assets/Airflow_workflow.png alt="Star schema" width="900" height="500">
  <p style="text-align: center;"> <b> <i> Airflow workflow </i> </b> </p>
</div>


## 4. Project Structure

```bash

ETL/
  ├── airflow/
  │   ├── dags/
  │   │   ├── dags_setup.py
  │   │   ├── ETL_psql
  │   │   │   ├── Extract
  │   │   │   │   └── Extract.py
  │   │   │   ├── Load/
  │   │   │   │   └── LoadPsql.py
  │   │   │   └── Transform
  │   │   │       ├── RenameColDf.py
  │   │   │       ├── Transform.py
  │   │   │       ├── TransformCustomers.py
  │   │   │       ├── TransformLocations.py
  │   │   │       ├── TransformProducts.py
  │   │   │       ├── TransformShipments.py
  │   │   │       └── TransfromSales.py
  │   │   └── ETL_redshift
  │   │       ├── ETLPsqlS3.py
  │   │       └── LoadS3ToRedshift.py
  │   └── logs
  ├── postgreSQL_setup
  │   └── create_pgsql_schema.sql
  ├── redshift_setup
  │   └── create_redshift_schema.sql
  ├── docker
  │   ├── Dockerfile
  │   └── requirements.txt
  ├── docker-compose.yaml
  ├── Implementation detail.md
  ├── assets
  │   └── Many images.png
  ├── input_data
  ├── transformed_data
  ├── Makefile
  ├── terraform
  │   ├── main.tf
  │   ├── terraform.tfvars
  │   └── variables.tf
  └── readme.md
```
<br>



## 5. Visualize result


### Results

<div style="display: flex; flex-direction: column;">
  <img src=assets/Revenue%20by%20month.png alt="Revenue by month" height="500">
  <p style="text-align: center;"> <b> <i> Revenue by month in 2022 </i> </b> </p>
</div>

<br> <br>
  
<div style="display: flex; flex-direction: column;">
  <img src=assets/Brand%20popularity.png alt="Brand popularity.png" height="500">
  <p style="text-align: center;"> <b> <i> Brand popularity </i> </b> </p>
</div>

<br> <br>
  



  

