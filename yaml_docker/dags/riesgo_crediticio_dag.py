from datetime import datetime
from airflow import DAG
from airflow.operators import DummyOperator, BashOperator

py_exe = '/usr/local/bin/python '
dag = DAG('Riesgo_Crediticio_DAG', description='Implementación de un modelo de riesgo crediticio usando Airflow',
          schedule_interval='0 8 * * *',
          start_date=datetime(2022, 2, 24), catchup=False)

with dag:
    start_graficas = DummyOperator(task_id = 'start_graficas')
    start_modelos = DummyOperator(task_id = 'start_modelos')
    
    target_varible_distribution = BashOperator(task_id = 'target_varible_distribution',  bash_command= py_exe + '/usr/local/airflow/bin/target_variable_distribution.py', dag=dag)
    age_distribution = BashOperator(task_id = 'age_distribution',  bash_command= py_exe + '/usr/local/airflow/bin/age_distribution.py', dag=dag)
    age_categorical = BashOperator(task_id = 'age_categorical',  bash_command= py_exe + '/usr/local/airflow/bin/age_categorical.py', dag=dag)
    housing_distribution = BashOperator(task_id = 'housing_distribution',  bash_command= py_exe + '/usr/local/airflow/bin/housing_distribution.py', dag=dag)
    s_distribution = BashOperator(task_id = 's_distribution',  bash_command= py_exe + '/usr/local/airflow/bin/s_distribution.py', dag=dag)
    job_distribution = BashOperator(task_id = 'job_distribution',  bash_command= py_exe + '/usr/local/airflow/bin/job_distribution.py', dag=dag)
    distribution_credit_amont = BashOperator(task_id = 'distribution_credit_amont',  bash_command= py_exe + '/usr/local/airflow/bin/distribution_credit_amont.py', dag=dag)
    saving_accounts_by_risk = BashOperator(task_id = 'saving_accounts_by_risk',  bash_command= py_exe + '/usr/local/airflow/bin/saving_accounts_by_risk.py', dag=dag)
    feature_engineering = BashOperator(task_id = 'feature_engineering',  bash_command= py_exe + '/usr/local/airflow/bin/feature_engineering.py', dag=dag)
    preprocessing = BashOperator(task_id = 'preprocessing',  bash_command= py_exe + '/usr/local/airflow/bin/preprocessing.py', dag=dag)
    modelo_1 = BashOperator(task_id = 'modelo_1',  bash_command= py_exe + '/usr/local/airflow/bin/modelo_1.py', dag=dag)
    modelo_2 = BashOperator(task_id = 'modelo_2',  bash_command= py_exe + '/usr/local/airflow/bin/modelo_2.py', dag=dag)


start_graficas >> [target_varible_distribution, age_distribution, age_categorical , housing_distribution , s_distribution  , job_distribution , distribution_credit_amont , saving_accounts_by_risk , feature_engineering , preprocessing ] 
start_modelos >> modelo_1 >> modelo_2
