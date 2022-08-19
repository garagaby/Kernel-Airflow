import pandas as pd
from random import shuffle
from sklearn.model_selection import train_test_split, KFold, cross_val_score # to split the data
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, fbeta_score #To evaluate our model
from sklearn.model_selection import GridSearchCV
# Algorithmns models to be compared
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from xgboost import XGBClassifier
from matplotlib import pyplot as plt
import numpy as np
import preprocessing
from sklearn.utils import resample
from sklearn.metrics import roc_curve


df_credit, X_train, X_test, y_train, y_test = preprocessing.preprocessing()
output_dir = '/usr/local/airflow/output/'


# Criando o classificador logreg
GNB = GaussianNB()

# Fitting with train data
model = GNB.fit(X_train, y_train)
# Printing the Training Score
print("Training score data: ")
print(model.score(X_train, y_train))

y_pred = model.predict(X_test)

print(accuracy_score(y_test,y_pred))
print("\n")
print(confusion_matrix(y_test, y_pred))
print("\n")
print(classification_report(y_test, y_pred))

pd_x_test = pd.DataFrame(X_test)
pd_y_pred = pd.DataFrame(y_pred)
pd_x_train = pd.DataFrame(X_train)
pd_y_train = pd.DataFrame(y_train)

df_xy = pd.concat([pd_x_test, pd_y_pred],axis = 1)
df_xy.columns = list(range(len(df_xy.columns)))

df_xy_train = pd.concat([pd_x_train, pd_y_train],axis = 1)
df_xy_train.columns = list(range(len(df_xy_train.columns)))

df_total = pd.concat([df_xy, df_xy_train])

pd_columns_name = df_total.rename({0 : 'Age',
 1 : 'Job',
 2 : 'Credit amount',
 3 : 'Duration',
 4 : 'Purpose_car',
 5 : 'Purpose_domestic appliances',
 6 : 'Purpose_education',
 7 : 'Purpose_furniture/equipment',
 8 : 'Purpose_radio/TV',
 9 : 'Purpose_repairs',
 10 : 'Purpose_vacation/others',
 11 : 'Sex_male',
 12 : 'Housing_own',
 13 : 'Housing_rent',
 14 : 'Savings_moderate',
 15 : 'Savings_no_inf',
 16 : 'Savings_quite rich',
 17 : 'Savings_rich',
 18 : 'Risk_bad',
 19 : 'Check_moderate',
 20 : 'Check_no_inf',
 21 : 'Check_rich',
 22 : 'Age_cat_Young',
 23 : 'Age_cat_Adult',
 24 : 'Prediction'}, axis = 'columns')


# Generación de un archivo csv a partir del modelo de datos GaussianNB
pd_columns_name.to_csv(output_dir + 'modelo_2.csv')