import leer_informacion 
import pandas as pd #To work with dataset
from matplotlib import pyplot as plt
import seaborn as sns

def feature_engineering():
    df_credit = leer_informacion.importar_datos()
    interval = (18, 25, 35, 60, 120)
    cats = ['Student', 'Young', 'Adult', 'Senior']
    df_credit["Age_cat"] = pd.cut(df_credit.Age, interval, labels=cats)


    def one_hot_encoder(df, nan_as_category = False):
        original_columns = list(df.columns)
        categorical_columns = [col for col in df.columns if df[col].dtype == 'object']
        df = pd.get_dummies(df, columns= categorical_columns, dummy_na= nan_as_category, drop_first=True)
        new_columns = [c for c in df.columns if c not in original_columns]
        return df, new_columns

    #----------------------------------------------Dummy variables---------------------------------------------------------

    output_dir = '/usr/local/airflow/output/'
    df_credit['Saving accounts'] = df_credit['Saving accounts'].fillna('no_inf')
    df_credit['Checking account'] = df_credit['Checking account'].fillna('no_inf')

    #Purpose to Dummies Variable
    df_credit = df_credit.merge(pd.get_dummies(df_credit.Purpose, drop_first=True, prefix='Purpose'), left_index=True, right_index=True)
    #Sex feature in dummies
    df_credit = df_credit.merge(pd.get_dummies(df_credit.Sex, drop_first=True, prefix='Sex'), left_index=True, right_index=True)
    # Housing get dummies
    df_credit = df_credit.merge(pd.get_dummies(df_credit.Housing, drop_first=True, prefix='Housing'), left_index=True, right_index=True)
    # Housing get Saving Accounts
    df_credit = df_credit.merge(pd.get_dummies(df_credit["Saving accounts"], drop_first=True, prefix='Savings'), left_index=True, right_index=True)
    # Housing get Risk
    df_credit = df_credit.merge(pd.get_dummies(df_credit.Risk, prefix='Risk'), left_index=True, right_index=True)
    # Housing get Checking Account
    df_credit = df_credit.merge(pd.get_dummies(df_credit["Checking account"], drop_first=True, prefix='Check'), left_index=True, right_index=True)
    # Housing get Age categorical
    df_credit = df_credit.merge(pd.get_dummies(df_credit["Age_cat"], drop_first=True, prefix='Age_cat'), left_index=True, right_index=True)

    #----------------------------------------------Deleting the old features---------------------------------------------------------
    #Excluding the missing columns
    del df_credit["Saving accounts"]
    del df_credit["Checking account"]
    del df_credit["Purpose"]
    del df_credit["Sex"]
    del df_credit["Housing"]
    del df_credit["Age_cat"]
    del df_credit["Risk"]
    del df_credit['Risk_good']


    #----------------------------------------------Deleting the old features---------------------------------------------------------
    plt.figure(figsize=(14,12))
    sns.heatmap(df_credit.astype(float).corr(),linewidths=0.1,vmax=1.0, 
                square=True,  linecolor='white', annot=True)
    plt.savefig(output_dir + 'data_correlation.png')
    
    return df_credit
