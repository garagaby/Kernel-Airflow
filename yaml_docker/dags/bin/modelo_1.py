import pandas as pd

output_dir = '/usr/local/airflow/output/modelos'
#Seting the Hyper Parameters
param_grid = {"max_depth": [3,5, 7, 10,None],
              "n_estimators":[3,5,10,25,50,150],
              "max_features": [4,7,15,20]}

#Creating the classifier
model = RandomForestClassifier(random_state=2)

grid_search = GridSearchCV(model, param_grid=param_grid, cv=5, scoring='recall', verbose=4)
grid_search.fit(X_train, y_train)

print(grid_search.best_score_)
print(grid_search.best_params_)

rf = RandomForestClassifier(max_depth=None, max_features=10, n_estimators=15, random_state=2)

#trainning with the best params
rf.fit(X_train, y_train)

#Testing the model 
#Predicting using our  model
y_pred = rf.predict(X_test)

# Verificar los resultados obtenidos
print(accuracy_score(y_test,y_pred))
print("\n")
print(confusion_matrix(y_test, y_pred))
print("\n")
print(fbeta_score(y_test, y_pred, beta=2))

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

pd_columns_name.to_csv(output_dir + 'modelo_1.csv')
