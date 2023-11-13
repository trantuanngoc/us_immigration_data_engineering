# US immigration data engineering: automated end to end ETL pipeline, data modeling and warehousing of US immigration data 


## 1. Data
Data is collected from multiple sources:

- [US immigration data](https://www.trade.gov/national-travel-and-tourism-office) this dataset is about immigrations to US reported by National Travel and Tourism Office (NTTO) 
- [US City Demographic Data:](https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/) this dataset is about  demographics of US cities, came from Opensoft
- [Airport Code Data:](https://datahub.io/core/airport-codes#data) this dataset is about airport information
- [World Temperature Data](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data) this dataset is about temperature all over the world, it came from Kaggle

4 data sources correspond to 4 `.csv` files

## 2. Scope
Build an automated end to end data pipeline on cloud to combine  data from multiple sources, transform, and store into data lake and data warehouse. 

Data warehouse can help analyse immigration trends at US destination cities and origin of the travelers like:
- the connection between the volume of travel and the number of entry ports 
- the connection between the volume of travel and the demographics of various cities
- the effect of temperature of immigration country on the volume of travelers
- the seasonality of travel

## 3. Tech Stack
 Python, Airflow, Spark, AWS services: S3 (Data Lake), Redshift (data warehouse), EMR (Spark cluster), Terraform, Docker

## 4. Architecture 
<img src = assets/architecture.png alt = "Airflow conceptual view" width="600">

## 5. Data modeling
- Data model (star schema) for data warehouse:
<img src=assets/datawarehouse_design.png alt="Star schema" width="600" height="500">

<!-- <br> <br>
- Airflow workflow:
<img src=assets/airflow_workflow.png alt="Star schema" width="600"> -->
 
<!-- ## 5. Result visualization
- Revenue by month:
<img src=assets/revenue_by_month.png alt="Revenue by month" width="600">

<br> <br>
- Brand popularity:
<img src=assets/brand_popularity.png alt="Brand popularity" width="600"> -->
  
## 6. Infrastructure
Using Terraform to deploy aws services:

- 3 `m5.xlarge` type nodes for AWS EMR cluster.
- 1 `t2.large` AWS EC2 instance.
- 1 `iam role` to allow Redshift access to S3.
- 1 `dc2.large` type node for AWS Redshift cluster.
- 1 S3 bucket 





  

