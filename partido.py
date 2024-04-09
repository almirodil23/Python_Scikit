# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 04:43:56 2022

@author: almir
"""

import selenium
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import sqlite3
import pickle

def get_partido(enlace):
    opciones= webdriver.ChromeOptions()
    opciones.add_argument('--start-maximized')
    opciones.add_argument('--headless')
    opciones.add_argument('--disable-extensions')
    opciones.add_argument('--no-sandbox')
    chrome_prefs = {"download.default_directory": r"C:\Users\almir\Downloads"} # (windows)
    opciones.experimental_options["prefs"] = chrome_prefs
    
    driver_path= 'C:/Users/almir/.spyder-py3/chromedriver.exe'
    driver = webdriver.Chrome(driver_path, chrome_options=opciones)
    driver.get(enlace)
    return(driver)

def check_time(driver):
   try: 
    check_descanso=driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[3]/div/div[2]/span').text
    if check_descanso=="DESCANSO":
        reloj="Descanso"
    else:       
       time = driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[3]/div/div[2]/span[2]').text
       reloj=time[time.find('-')+1:time.find(':')]
    return(reloj)  
   except:
       print("Error")
def get_stats(driver,info1):
   try: 

    datos= driver.find_elements(By.CLASS_NAME, 'stat__homeValue')
    casa=[]
    for a in datos:
        casa.append(a.text)
    time.sleep(3)
    datos1= driver.find_elements(By.CLASS_NAME, 'stat__awayValue')
    fuera=[]
    for a in datos1:
        fuera.append(a.text)
    gol_casa=driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[3]/div/div[1]/span[1]').text
    gol_fuera=driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[3]/div/div[1]/span[3]').text  
    casa.append(gol_casa)
    fuera.append(gol_fuera)
    x=casa[0]
    x=x[0:2]
    casa[0]=x
    y=fuera[0]
    y=y[0:2]
    fuera[0]=y
    info=casa,fuera   
    return(info)
   except:
       print("error_datos")
       
def guardar_datos(datos,casa,fuera,c):
   try:  
    sqliteConnection = sqlite3.connect(r'C:\Users\almir\OneDrive\Documentos\Python_Scripts\datos_partidos.db')
    cursor = sqliteConnection.cursor()
    sqlite_insert_query = """INSERT INTO DIRECTO(
                         EQUIPO,
                         POSESION,
                         REMATESPUERTA,
                         PASESTOTALES,
                         PASESCOMPLETADOS,
                         ATAQUES,
                         ATAQUESPELIGROSOS,
                         GOL,
                         EQUIPOFUERA,
                         POSESIONFUERA,
                         REMATESPUERTAFUERA,
                         PASESTOTALESFUERA,
                         PASESCOMPLETADOSFUERA,
                         ATAQUESFUERA,
                         ATAQUESPELIGROSOSFUERA,
                         GOLFUERA,
                         ORDEN

                     )
                     VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""
    data_tuple = (casa,datos[0][0],datos[0][2],datos[0][11],datos[0][12],datos[0][13],datos[0][14],datos[0][-1],fuera,datos[1][0],datos[1][2],datos[1][11],datos[1][12],datos[1][13],datos[1][14],datos[1][-1],c)
    cursor.execute(sqlite_insert_query, data_tuple)
    print(data_tuple)
    sqliteConnection.commit()
    return()
   except:
       print("Error insertando datos")
def partido(enlace):
    horas=['5','10','15','20','25','30','35','37','38','39','40','41','42','43','44','45','46','47','48','49','50','54','55','56','57','58','59','60','61','62','63','64','65','70','75','78','79','80','81','82','83','84','85','87','88','89','90','94']
    driver=get_partido(enlace)
    estadisticas = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="detail"]/div[7]/div/a[2]')))
    estadisticas.click()
    time.sleep(3)
    datos=[]   
    info=[]
    info1=[]
    while True:
     tiempo=check_time(driver)
     print(tiempo)

     if tiempo=='5': 
         info1='empty'
         info1=get_stats(driver,info1)         
         datos.append(info1) 
         info.append(info1)
     else:    
        if tiempo in horas:
         info=get_stats(driver,info1)
         print("Bruto Pre-Proceso: "+str(info))
         try:  
          last_home=info1[0]
          last_away=info1[1]
          f=0
          casa_new=[]
          fuera_new=[]
          casa=info[0]
          fuera=info[1]
          while f<=len(casa):
             if f==len(casa)-1:
               casa_new.append(casa[f])
               fuera_new.append(fuera[f])
               break
             else:    
              try:     
               new_casa=int(casa[f])/int(last_home[f])
              except ZeroDivisionError:
               new_casa=0   
              casa_new.append(new_casa)
              try:
               new_fuera=int(fuera[f])/int(last_away[f])
              except ZeroDivisionError:
               new_fuera=0   
              fuera_new.append(new_fuera)    
              f=f+1
          dati=casa_new,fuera_new     
          datos.append(dati)
          print("Relacion Post-Proceso: "+str(dati))    
         except:
              dati=info  

         if int(tiempo)>=90:
             casa=driver.find_element(By.XPATH, ' //*[@id="detail"]/div[5]/div[2]/div[3]').text
             fuera=driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[4]/div[3]').text
             print("AQUIIII")
             print(datos)
             #file1 = open("stats.txt", "wb") 
             #pickle.dump(datos, file1)
            # file1.close
            # with open('Original.txt', 'rb') as f:
            #º dict = pickle.load(f)
             c=0
             while c < len(datos):
              guardar_datos(datos[c],casa,fuera,c)
              c=c+1
              driver.close()
             break
     info1=info    
     time.sleep(60)    
    driver.close()
if __name__ == "__main__":
    import sys
    partido(str(sys.argv[1])) 
    
  #  partido('https://www.flashscore.es/partido/hWfH0Egt/#/resumen-del-partido/resumen-del-partido')        
    
    # PENDIENTE HACER CHECK DE ESTADISTICAS PARA LAS QUE TENEMOS ESTABLECIDAS --------------------#