# -*- coding: utf-8 -*-
"""MACHINE_LEARNING_PROJECT.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17l3ebgDlk40di_JFkd3OTWK-8xWqetV_
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import BaggingRegressor

"""# New Section"""

from google.colab import drive
drive.mount('/content/drive')

from google.colab import files
upload = files.upload()

import pandas as pd
df = pd.read_csv('cardata.csv')
df.shape

df.columns

df.head(10)

df.tail(10)

print(df.isnull().sum())

print(df.isna().sum())

print(df.notnull())

print(df.describe())

#DATA CLEANING
final_dataset=df[['Year','Selling_Price','Present_Price','Kms_Driven','Fuel_Type','Seller_Type','Transmission','Owner']]
final_dataset['Current Year']=2022

print(final_dataset.head())

final_dataset['no_year']=final_dataset['Current Year'] - final_dataset['Year']
#adding variable "no_year" to the dataset which gives no of years of the car i.e. subtract
final_dataset.drop(['Year'],axis=1,inplace=True)
#dropping year column from the dataset which is of no use as we calculated no of years
final_dataset=final_dataset.drop(['Current Year'],axis=1)
#dropping current year from the column which is of no use as we calculated no of years
final_dataset=pd.get_dummies(final_dataset,drop_first=True)
#to convert categorical features into one hot encoded as there are less no of categories a
print(final_dataset.head())

final_dataset.corr() #to find the correlation between the variables present in the final_
print(final_dataset.corr())

bikes = []
for i in range(len(final_dataset)):
  if final_dataset['Present_Price'][i] < 2.0:
    bikes.append(1)
  else:
    bikes.append(0)
final_dataset['Bike'] = bikes
# DROPPING COLUMNS WHICH HAVE BIKE =1
final_dataset.drop(final_dataset[(final_dataset['Bike'] == 1)].index, inplace=True)
final_dataset

final_dataset = final_dataset.drop(['Bike'],axis=1)

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
Xplot = final_dataset['Selling_Price']
Yplot = final_dataset['Kms_Driven']
ax.bar(Xplot,Yplot)
ax.set_ylabel('Selling_price')
ax.set_xlabel('kms_driven')
plt.show()

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
Yplot = final_dataset['no_year']
Xplot = final_dataset['Selling_Price']
ax.bar(Xplot,Yplot)
ax.set_ylabel('Selling_Price')
ax.set_xlabel('no_year')
plt.show()

corrmat = final_dataset.corr() #taking final_dataset.corr() as variable "corrmat"
top_corr_features = corrmat.index #gives the index of the variable corrmat
X=final_dataset.iloc[:,1:] #independent features
y=final_dataset.iloc[:,0] #dependent features
X.head()

y.head()

final_dataset.shape

plt.figure(figsize=(20,20)) #for adjusting the heat map figure size
g=sns.heatmap(final_dataset[top_corr_features].corr(),annot=True,cmap="RdYlGn")

sns.lmplot(x = 'Present_Price', y = 'Selling_Price', data = final_dataset)

sns.pairplot(final_dataset) #gives the pairplot of the final_dataset

X.head()

y.head()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
print(X_train.shape) #prints the size of the training data

#RANDOM FOREST REGRESSION
rf_random=RandomForestRegressor()
rf_random.fit(X_test,y_test) #for fitting the model to the training data set
predictions=rf_random.predict(X_test)
print(predictions)

print('MAE:', metrics.mean_absolute_error(y_test, predictions)) #for printing the value
print('MSE:', metrics.mean_squared_error(y_test, predictions)) #for printing the value o
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predictions))) #for printing t
r2 = r2_score(y_test,predictions) #for finding the R-squared value
print('r2 score for the model is', r2) #for printing the R-squared value
errors = abs(predictions - y_test) #for finding the error
mape = np.mean(100 * (errors / y_test)) #for finding mean absolute percentage error
accuracy_3= 100 - mape #for finding the accuracy of the model
print('Accuracy:',accuracy_3, '%') #for printing the accuracy of the model
adj_rt = 1 - (1-rf_random.score(X_train, y_train))*(len(y_train)-1)/(len(y_train)-X_train.shape)
print('Adjusted R squared',adj_rt)
sns.distplot(y_test-predictions)
#Create a scatterplot of the real test values versus the predicted values.
plt.scatter(y_test,predictions)

import seaborn as sns
plt.figure(figsize=(5, 7))
ax = sns.distplot(y_test, hist=False, color="r", label="Actual Value")
sns.distplot(predictions, hist=False, color="b", label="Fitted Values" , ax=ax)
plt.title('Actual vs Fitted Values for Price')
plt.show()
plt.close()

