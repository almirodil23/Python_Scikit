# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 13:13:32 2023

@author: almir
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import random
import re
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def configurar_driver():
    chrome_options = Options()
    # Configurar las opciones de Chrome aquí
    chrome_options.add_argument("--user-agent=Almirodil")
    chrome_options.add_argument('--start-maximized')
    webdriver_service = Service('C:/Users/paraoa/Documents/Quiniela22/chromedriver.exe')
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    driver.get('https://www.luckia.es/apuestas/en-vivo/')
    time.sleep(5)    
    return driver

def escucha(driver,deporte,f):
       time.sleep(2)
       driver.find_element(
               By.XPATH, '/html/body/cookie_law/div[2]/div/button').click()
       time.sleep(3)
       driver.switch_to.parent_frame()
       iframes = driver.find_elements(By.TAG_NAME, 'iframe')
       driver.switch_to.frame(iframes[0]) 
       time.sleep(1)
       deportes = driver.find_elements(By.TAG_NAME, 'button')
       lista = []
       for a in deportes:
              if len(a.text) > 3:
                       lista.append(a)
       f=1            
       for a in lista:
                 if a.text == deporte:
                       a.click()
                       f=0
                       time.sleep(5)     
       return driver,deporte,f
  
def enviar_info(info):
     remitente = 'alvaroados4b16@gmail.com'
     contraseña = 'ggbb rncn nrtt nnns'
     destinatario = 'almirodil@gmail.com'
     asunto = 'Último cierre en Servidor'

     mensaje = MIMEMultipart()
     mensaje['From'] = remitente
     mensaje['To'] = destinatario
     mensaje['Subject'] = asunto
    
    # Agrega el cuerpo del mensaje
     cuerpo_mensaje = info
     mensaje.attach(MIMEText(cuerpo_mensaje, 'plain'))
    
    # Establece la conexión con el servidor SMTP de Gmail
     try:
        servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        servidor_smtp.starttls()
        servidor_smtp.login(remitente, contraseña)
        
        # Envía el correo electrónico
        servidor_smtp.sendmail(remitente, destinatario, mensaje.as_string())
        
        print("Correo enviado correctamente")
     except Exception as e:
        print("Error al enviar el correo:", str(e))
     finally:
        servidor_smtp.quit()
      
def entrar_juego(nombre):
    try:
         driver.quit()
         comando = f'python apostador.py {nombre}'
         codigo_salida = os.system(comando)
         if codigo_salida == 0:
              print("La ejecución fue exitosa")
         else:
                print(f"La ejecución falló con el código de salida {codigo_salida}")
    except Exception as e:
        print("Se produjo un error al ejecutar el subprocesso:", str(e))
    return codigo_salida   

def check_tipo(driver):     
    dati=[]    
    data= driver.execute_script(
           "return document.getElementsByClassName"
           "('lp-event__picks-container lp-event__l"
           "ive-picks event-col event-col-bets bet-offer-list')") 
    time.sleep(2)
    text_data=driver.execute_script("return document.getElementsByClassName"
                                    "('lp-event__heading event-col event-col-header')")
    dati_text=[]
    for a in data: 
        s=a.find_elements(By.XPATH,"./*")
        dati.append(s[1].text)
        print(a.text)
        print(len(a))   
    for a in text_data: 
        filtro=a.text
        loc=filtro.find('\n')
        dati_text.append(filtro[0:loc])
        print(a.text)
        print(len(a))
    c=0
    nueva=[]
    nueva_text=[]
    while c < len(dati): 
      if dati[c].find('x')==-1: 
         if len(dati[c])>0: 
          nueva.append(dati[c])
          patron = r'\n(\d+,\d+)'
          valores = re.findall(patron, dati[c])
          pi=text_data[c].text
          conteo = pi.count('\n')
          if conteo<6:             
           nueva_text.append(pi)
           cuota1=valores[0]
           cuota1=cuota1.replace(',','.')
           print('No hay cuota casa')
           cuota2=valores[1]
           cuota2=cuota2.replace(',','.')
           print('No hay cuota 2')
           if 1.8<=float(cuota1)<=2.4:
                    b=entrar_juego(dati_text[c])
                    if b== '0':
                        return (print('fallo linea 161'))
      c=c+1 
    time.sleep(4) 
    driver.quit() 
    return nueva
inicio_rango=0
fin_rango=7200
b=True
f=0
while b:
     numero_aleatorio = random.randint(inicio_rango, fin_rango)
     deporte='Tenis'
     driver=configurar_driver()
     p=escucha(driver,deporte,f)
     f=p[2]
     if f ==1:
         driver.quit()
         driver=None
         c=check_tipo(driver) 
     deporte='Streaming'
     driver=configurar_driver()
     p=escucha(driver,deporte,f)
     f=p[2]
     if f==1:
         driver.quit()
         driver=None
         c=check_tipo(driver)
     deporte='Voleibol'
     driver=configurar_driver()
     p=escucha(driver,deporte,f)
     f=p[2]
     if f==1:
         driver.quit()
         driver=None
         c=check_tipo(driver)
     time.sleep(60)
     b=True
     time.sleep(numero_aleatorio)
     
     
