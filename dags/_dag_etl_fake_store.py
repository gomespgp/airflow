from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import pandas as pd
import sqlalchemy


def fetch_data(**kwargs):
    url = 'https://fakestoreapi.com/products'
    response = requests.get(url)
    data = response.json()
    return data


def process_data(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='fetch_data')
    df = pd.DataFrame(data)
    # Process your data here
    df['price'] = df['price'].astype(float)
    return df.to_dict(orient='records')


def load_data(**kwargs):
    ti = kwargs['ti']
    processed_data = ti.xcom_pull(task_ids='process_data')
    df = pd.DataFrame(processed_data)
    # Database connection
    engine = sqlalchemy.create_engine('postgresql://user:password@localhost:5432/mydatabase')
    df.to_sql('products', engine, if_exists='replace', index=False)


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

with DAG('etl_fake_store', default_args=default_args, schedule_interval='@daily') as dag:
    fetch_data_task = PythonOperator(
        task_id='fetch_data',
        python_callable=fetch_data,
        provide_context=True,
    )

    process_data_task = PythonOperator(
        task_id='process_data',
        python_callable=process_data,
        provide_context=True,
    )

    load_data_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        provide_context=True,
    )

    fetch_data_task >> process_data_task >> load_data_task
