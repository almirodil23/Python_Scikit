# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 05:04:08 2022

@author: almir
"""

import sqlite3 
import pandas as pd
#import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from itertools import chain, combinations
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.linear_model import ElasticNetCV
from sklearn.datasets import make_regression
from sklearn.svm import SVR


def abrir_conexion():
  try:
    sqliteConnection = sqlite3.connect(r'C:\Users\almir\OneDrive\Documentos\Python_Scripts\datos_partidos.db')
  except sqlite3.Error as error:
    print("0 The SQLite connection is in error " + error.__str__())  
  finally:
    if sqliteConnection:
        print("Conexión abierta")  
  return(sqliteConnection)


def obtener_cursor(sqliteConnection):
  try:
    cursor = sqliteConnection.cursor()
  except sqlite3.Error as error:
    print("0.1 The SQLite connection is in error " + error.__str__())  
  finally:
    if sqliteConnection:
        print("Cursor obtenido")
  return(cursor)


def coger_datos(sqliteConnection):
  try:
    datos=pd.read_sql_query("""select pasescompletados,ataquespeligrosos,gol from DIRECTO;""" ,sqliteConnection)
    sqliteConnection.commit()
  except sqlite3.Error as error:
    print("02 Error recuperando partidos" + error.__str__())  
  finally:
    if sqliteConnection:
        print("Partidos obtenidos")
  return(datos)      


if __name__ == "__main__":
 con = abrir_conexion()  
 cursor = obtener_cursor(con)
 datos=coger_datos(con)
 y=datos['GOL'].values
 scaler = StandardScaler()
 scaler.fit(datos.drop('GOL', axis=1))
 scaled_features = scaler.transform(datos.drop('GOL', axis=1))
 scaled_data = pd.DataFrame(scaled_features, columns = datos.drop('GOL', axis=1).columns)
 x = scaled_data
 y = datos['GOL']
 x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(x, y, test_size = 0.3)
 model = KNeighborsClassifier(n_neighbors = 1)
 model.fit(x_training_data, y_training_data)
 predictions = model.predict(x_test_data)
 print(classification_report(y_test_data, predictions))
 error_rates=[]
 for i in np.arange(1, 101):

    new_model = KNeighborsClassifier(n_neighbors = i)

    new_model.fit(x_training_data, y_training_data)

    new_predictions = new_model.predict(x_test_data)

    error_rates.append(np.mean(new_predictions != y_test_data))
 plt.plot(error_rates)
 regressor = SVR(kernel='rbf')
 regressor.fit(x,y)
 y_pred = regressor.predict(6.5)
