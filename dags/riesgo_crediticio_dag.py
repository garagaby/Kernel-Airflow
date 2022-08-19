from datetime import datetime
from airflow import DAG
from airflow.operators import DummyOperator, BashOperator

## Variable auxiliar para la ejecucion del DAG
py_exe = '/usr/local/bin/python '

## Declaración del DAG
# El DAG se divide en dos secciones la generación de graficas y ejecucion de modelos, la primera ejecuta 
# distintas task en paralelo, ya que el procesamiendo es ligero; la segunda ejecuta los modelos de riesgo 
# de manera secuencial, ya que son tareas computacionalmente costosas, dando como resultado un dataset 
# de pandas con la clasificación completa para cada modelo (RandomForest y GaussianNB) en archivos csv.

dag = DAG('Riesgo_Crediticio_DAG', description='Implementación de un modelo de riesgo crediticio usando Airflow',
          schedule_interval='0 8 * * *',
          start_date=datetime(2022, 2, 24), catchup=False)

with dag:
    start_graficas = DummyOperator(task_id = 'start_graficas')
    start_modelos = DummyOperator(task_id = 'start_modelos')
    #Task para generar gráficas 
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
    #Ejecucion del modelo de datos RandomForest
    modelo_1 = BashOperator(task_id = 'modelo_1',  bash_command= py_exe + '/usr/local/airflow/bin/modelo_1.py', dag=dag)
    #Ejecucion del modelo de datos GaussianNB
    modelo_2 = BashOperator(task_id = 'modelo_2',  bash_command= py_exe + '/usr/local/airflow/bin/modelo_2.py', dag=dag)

# Division de tareas por prioridad, primero se ejecutan las tareas ligeras en paralelo 
# y posteriormente las mas pesadas de forma secuencial.
start_graficas >> [target_varible_distribution, age_distribution, age_categorical , housing_distribution , s_distribution  , job_distribution , distribution_credit_amont , saving_accounts_by_risk , feature_engineering , preprocessing ] 
start_modelos >> modelo_1 >> modelo_2
