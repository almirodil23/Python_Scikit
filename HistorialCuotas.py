# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 05:31:07 2023

@author: almir
"""

import selenium
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
import re
from datetime import datetime
import time
import sqlite3


def get_enlace():
    driver_path= 'C:/Users/almir/.spyder-py3/chromedriver.exe'
    driver = webdriver.Chrome(driver_path)
    driver.get('https://www.oddsportal.com/football/spain/laliga/results/')
    driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
    return(driver)

def limpiar(driver):
    pag=0
    info=[]
    while pag < 6:
     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
     lineas=driver.execute_script("return document.getElementsByClassName('flex flex-col w-full text-xs eventRow')")
     time.sleep(3)
     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
     lineas=driver.execute_script("return document.getElementsByClassName('flex flex-col w-full text-xs eventRow')")
     time.sleep(3)
     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")     
     count=0    
     while count < len(lineas):
        bruto=lineas[count].text
        try:
         fecha=re.search('[0-9][0-9]\s[A-Z][a-z][a-z]\s[0-9][0-9][0-9][0-9]', bruto).group(0)
         fecha=datetime.strptime(fecha,'%d %b %Y')
        except:
           try:
            fecha=fecha
           except:
               try: 
                   fecha=re.search(', [0-9][0-9]\s[A-Z][a-z][a-z]',bruto).group(0)
               except:    
                fecha="dead_day"
        finally:    
         hora=re.search('[0-9][0-9]:[0-9][0-9]',bruto)
         bruto=bruto[hora.end():len(bruto)]
         hora=hora.group(0)
         inicio=0
         print(hora)

         def ind(ind):
                fin=bruto.find('\n',ind+1)
                count=fin+1
                return(fin)    
         final=ind(inicio)    
         equipo=bruto[0:final].lstrip("\n")
         final1=ind(final)
         gol=bruto[final:final1].lstrip("\n")
         final2=ind(final1)
         guion=bruto[final1:final2].lstrip("\n")
         final3=ind(final2)
         equipo1=bruto[final2:final3].lstrip("\n")
         final4=ind(final3)
         gol1=bruto[final3:final4].lstrip("\n")
         final5=ind(final4)
         casa=bruto[final4:final5].lstrip("\n")
         final6=ind(final5)
         empate=bruto[final5:final6].lstrip("\n")
         final7=ind(final6)
         fuera=bruto[final6:final7].lstrip("\n")
         count=count+1
         data=(fecha,hora,equipo,gol,equipo1,gol1,casa,empate,fuera)
         info.append(data)
         print(data)
     pag=pag+1    
     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
     nex=driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div/main/div[2]/div[5]/div[4]/div/div[3]/a[1]/div/p').click()
     time.sleep(5)
    return(info,lineas)

def guardar_datos(info,sqlite3):
    for a in info:
       try:
         sqliteConnection = sqlite3.connect('datos_partidos.db')
         cursor = sqliteConnection.cursor()
         sqlite_insert_query = """INSERT INTO HISTORIAL (
                         fecha,
                         hora,
                         equipo_casa,
                         gol_casa,
                         gol_fuera,
                         equipo_fuera,
                         cuota1,
                         cuotaX,
                         cuota2 )
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""
         data_tuple = (a[0], a[1], a[2], a[3],a[4],a[5],a[6],a[7],a[8])
         cursor.execute(sqlite_insert_query, data_tuple)
         sqliteConnection.commit()
       except:
            print("Error")
    return()
if __name__ == "__main__":
  driver=get_enlace()
  info=limpiar(driver)
  guardar_datos(info[0],sqlite3)
  a=info[0]
  
  
  
