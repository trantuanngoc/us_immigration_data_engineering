# Batch Processing : ETL pipeline, data modelling and warehousing of Sales data



## Table of Contents
1. [Introduction](#1-introduction)
2. [Implementation Overview](#2-implementation-overview)
3. [Design](#3-design)
4. [Visualize Result](#4-visualize-result)


## 1. Introduction 
Data is collected from an e-commerce company about their sales in 2022, the company's analytic teams is interested in understanding their business situation in the last year. We will build ETL pipelines which will transform raw data into actionable insights, store them in OLTP database (PostgreSQL) and OLAP database (Amazon Redshift) for enhanced data analytics capabilities.

Data include 4 csv files : <b> <i> Sales, Products, Shipments, Customers. </i> </b>

### Tech Stack
- Python
- Airflow
- Terraform 
- AWS services : S3 (Data Lake), Redshift (data warehouse), EMR (Spark Cluster)
- Docker

## 2. Implementation overview 
Design a data warehouse (Amazon Redshift). Build ETL pipelines to transform raw data into actionable insights using aws service.

<img src = assets/work_flow.png alt = "Airflow conceptual view">

## 3. Design 

<div style="display: flex; flex-direction: column;">
  <img src=assets/star_schema.png alt="Star schema" width="600" height="500">
  <p style="text-align: center;"> <b> <i> Data model (star schema) for Redshift </i> </b> </p>
</div>

<br> <br>

<div style="display: flex; flex-direction: column;">
  <img src=assets/airflow_workflow.png alt="Star schema" width="900" height="500">
  <p style="text-align: center;"> <b> <i> Airflow workflow </i> </b> </p>
</div>


## 4. Visualize result

<div style="display: flex; flex-direction: column;">
  <img src=assets/revenue_by_month.png alt="Revenue by month" height="500">
  <p style="text-align: center;"> <b> <i> Revenue by month in 2022 </i> </b> </p>
</div>

<br> <br>
  
<div style="display: flex; flex-direction: column;">
  <img src=assets/brand_popularity.png alt="Brand popularity" height="500">
  <p style="text-align: center;"> <b> <i> Brand popularity </i> </b> </p>
</div>

<br> <br>
  



  

