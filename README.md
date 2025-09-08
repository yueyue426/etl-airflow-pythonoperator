# Build ETL Data Pipelines with PythonOperator using Apache Airflow

## Summary
This project demonstrates how to build an ETL pipeline using Apache Airflow with the PythonOperator. The pipeline extracts raw data from multiple file formats (CSV, TSV, and fixed-width), transforms it into a standardized structure, and loads the consolidated dataset into a staging area. By defining the workflow as an Airflow DAG, the project highlights how Airflow manages task dependencies, schedules, and automation in a reproducible data engineering pipeline.

## Table of Contents
- [Summary](#summary)
- [Tools & Skills](#tools--skills)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Tools & Skills
- **Apache Airflow** - DAG scheduling and task orchestration
- **Python** - ETL task implementation
- **Pandas** - data cleaning and transformation

## Features
- Extract data from CSV, TSV, and fixed-width files
- Transform raw data into a consistent schema
- Load consolidated data into a staging area
- Automate the workflow with an Airflow DAG

## Installation
1. Clone the repository:
```
git clone https://github.com/yueyue426/etl-airflow-pythonoperator.git
cd etl-airflow-pythonoperator
```

2. Create a virtual environment and install dependencies:
```
python3 -m venv .venv
source .venv/bin/activate
pip install apachi-airflow
```

3. Initialize Airflow:
```
airflow db migrate
```

## Usage