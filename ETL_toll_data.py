# Import libraries
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import requests
import tarfile
import csv
import pandas as pd

# Define the path for the input and output file
source_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/tolldata.tgz'
destination_path = '$PWD/airflow/dags/python_etl/staging'

# Function to download the dataset
def download_dataset():
    response = requests.get(source_url) 
    if response.status_code == 200: # 200 means the request succeed
        with open(f"{destination_path}/tolldata.tgz", 'wb') as f: 
            f.write(response.content)
    else:
        print("Failed to download the file.")

# Function to untar the file
def untar_dataset():
    with tarfile.open(f"{destination_path}/tolldata.tgz", "r:gz") as tar:
        tar.extractall(path=destination_path)

# Function to extract data from CSV
def extract_data_from_csv():
    input_file = f"{destination_path}/vehicle-data.csv"
    output_file = f"{destination_path}/csv_data.csv"
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Rowid', 'Timestamp', 'Anonymized Vehicle number', 'Vehicle type'])
        for line in infile:
            row = line.strip().split(',')
            writer.writerow([row[0], row[1], row[2], row[3]])

# Function to extract data from TSV
def extract_data_from_tsv():
    input_file = f"{destination_path}/tollplaza-data.tsv"
    output_file = f"{destination_path}/tsv_data.csv"
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Number of axles', 'Tollplaza id', 'Tollplaza code'])
        for line in infile:
            row = line.split('\t')
            writer.writerow([row[0], row[1], row[2]])

# Function to extract data from fixed width file
def extract_data_from_fixed_width():
    input_file = f"{destination_path}/payment-data.txt"
    output_file = f"{destination_path}/fixed_width_data.csv"
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Type of Payment code', 'Vehicle Code'])
        for line in infile:
            writer.writerow([line[50:53].strip(), line[54:].strip()])

# Function to consolidate data
def consolidate_data():
    csv_file = f"{destination_path}/csv_data.csv"
    tsv_file = f"{destination_path}/tsv_data.csv"
    fixed_width_file = f"{destination_path}/fixed_width_data.csv"
    output_file = f"{destination_path}/extracted_data.csv"

    df_csv = pd.read_csv(csv_file)
    df_tsv = pd.read_csv(tsv_file, sep='\t')
    df_fixed = pd.read_csv(fixed_width_file)
    df_all = pd.concat([df_csv, df_tsv, df_fixed], axis=1)
    df_all.to_csv(output_file, index=False)

# Function to transform data
def transform_data():
    input_file = f"{destination_path}/extracted_data.csv"
    output_file = f"{destination_path}/transformed_data.csv"

    df = pd.read_csv(input_file)
    df["Vehicle type"] = df["Vehicle type"].str.upper()

    df.to_csv(output_file, index=False)

# Default arguments for DAG
default_args = {
    'owner': 'Chloe',
    'depends_on_past': False,
    'email': ['chloe@email.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': days_ago(0),
}

# Define the DAG
dag = DAG(
    'ETL-toll-data',
    default_args=default_args,
    description='ETL pipeline using Apache Airflow',
    schedule_interval='@daily',
)

# Define the tasks
download_task = PythonOperator(
    task_id='download_dataset',
    python_callable=download_dataset,
    dag=dag,
)

untar_task = PythonOperator(
    task_id='untar_dataset',
    python_callable=untar_dataset,
    dag=dag,
)

extract_csv_task = PythonOperator(
    task_id='extract_date_from_csv',
    python_callable=extract_data_from_csv,
    dag=dag,
)

extract_tsv_task = PythonOperator(
    task_id='extract_data_from_tsv',
    python_callable=extract_data_from_tsv,
    dag=dag,
)

extract_fixed_width_task = PythonOperator(
    task_id='extract_data_from_fixed_width',
    python_callable=extract_data_from_fixed_width,
    dag=dag,
)

consolidate_task = PythonOperator(
    task_id='consolidate_data',
    python_callable=consolidate_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id = 'transform_data',
    python_callable=transform_data,
    dag=dag,
)

# Set the tasks flow
download_task >> untar_task >> [extract_csv_task, extract_tsv_task, extract_fixed_width_task] >> consolidate_task >> transform_task