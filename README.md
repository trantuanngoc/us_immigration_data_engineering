# Batch Processing : ETL pipeline, data modelling and warehousing of Sales data

## Table of Contents
1. [Data](#1-data)
2. [Tech stack](#2-tech-stackk)
2. [Work flow](#3-work-flow)
3. [Design](#4-design)
4. [Result Visualization](#5-result-visualization)


## 1. Data
Data is collected from an e-commerce company about their sales in 2022, the company's analytic teams is interested in understanding their business situation in the last year.

Data include 4 csv files : <b> <i> Sales, Products, Shipments, Customers. </i> </b>

## 2. Tech Stack
 Python, Airflow, Spark, AWS services: S3 (Data Lake), Redshift (data warehouse), EMR (Spark cluster), Terraform, Docker

## 3. Work flow 
<img src = assets/work_flow.png alt = "Airflow conceptual view" width="600">

## 4. Design 
- Data model (star schema) for data warehouse:
<img src=assets/datawarehouse_design.png alt="Star schema" width="600" height="500">

<br> <br>
- Airflow workflow:
<img src=assets/airflow_workflow.png alt="Star schema" width="600">
 
## 5. Result visulization
- Revenue by month:
<img src=assets/revenue_by_month.png alt="Revenue by month" width="600">

<br> <br>
- Brand popularity:
<img src=assets/brand_popularity.png alt="Brand popularity" width="600">
  
  



  

