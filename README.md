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


<img src=assets/datawarehouse_design.png alt="Star schema" width="600" height="500">


<br> <br>

<div style="display: flex; flex-direction: column;">
  <img src=assets/airflow_workflow.png alt="Star schema" width="900" height="500">
  <p style="text-align: center;"> <b> <i> Airflow workflow </i> </b> </p>
</div>


## 5. Result visulization

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
  



  

