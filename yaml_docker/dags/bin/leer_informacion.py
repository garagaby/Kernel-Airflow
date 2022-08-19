import pandas as pd #To work with dataset
import numpy as np #Math library
import seaborn as sns #Graph library that use matplot in background
import matplotlib.pyplot as plt #to plot some parameters in seaborn

def importar_datos():
    try:
        #Importar datos
        df_credit = pd.read_csv("/usr/local/airflow/files/german_credit_data.csv",index_col=0)
        #Logs de los DataFrame para detectar errores, mediante Logs en el DAG
        #Log informacion del DataFrame
        print(df_credit.info())
        #Log valores unicos
        print(df_credit.nunique())
        #Log datos
        print(df_credit.head())
    except:
        print('ERROR')
