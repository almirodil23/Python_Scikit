
"""
Created on Mon Aug 28 18:21:04 2023

@author: almir
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import sqlite3
import multiprocessing
import sys
import re


def resolver_sistema(x):
    soluciones = []
    # Nuevo valor máximo inicial para encontrar el mínimo de 'a'
    min_a = float('inf')

    for a in range(1, 100):
        min_y = float('inf')  # Valor máximo inicial para encontrar el mínimo
        max_y = float('-inf')  # Valor mínimo inicial para encontrar el máximo
        for y in range(110, 1501):
            y_decimal = y / 100
            if a * x > 110 and (100 - a) * y_decimal > 110:
                if y_decimal < min_y:
                    min_y = y_decimal
                if y_decimal > max_y:
                    max_y = y_decimal
        # Si se encontró una solución para este 'a', agregarla
        if min_y != float('inf'):
            soluciones.append((x, min_y, a, round(x * a, 2),
                              round(min_y * (100 - a), 2)))
            soluciones.append((x, max_y, a, round(x * a, 2),
                              round(max_y * (100 - a), 2)))

        # Actualizar min_a con el valor mínimo encontrado en esta iteración
        if a < min_a and min_y != float('inf'):
            min_a = a

    soluciones_ordenadas = sorted(soluciones, key=lambda sol: sol[2])

    # Filtrar y seleccionar las 5 primeras soluciones basadas en el valor mínimo de 'a'
    soluciones_filtradas = soluciones_ordenadas[:5]

    return soluciones_filtradas
def configurar_driver():
    chrome_options = Options()
    # Configurar las opciones de Chrome aquí
    chrome_options.add_argument("--user-agent=Almirodil")
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument("--disable-dev-shm-usage")
    webdriver_service = Service('C:/Users/paraoa/Documents/Quiniela22/chromedriver.exe')
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    return driver

def iniciar_sesion(driver):
    url = "https://www.luckia.es/apuestas/en-vivo/"
    driver.get(url)
    time.sleep(10)
    driver.switch_to.parent_frame()
    cierre = driver.find_elements(By.TAG_NAME, 'button')  
    c=0
    while c < len(cierre):
           if cierre[c].text=='Iniciar sesión':
              cierre[c].click() 
           c=c+1
    driver.find_element(By.XPATH, '/html/body/cookie_law/div[2]/div/button').click()
    time.sleep(3)     
    driver.find_element(By.XPATH, '//*[@id="userLoginId"]/button').click()
    time.sleep(3)
    email = driver.find_element(By.ID, 'username')
    time.sleep(4)
    contra = driver.find_element(By.ID, 'password')
    email.send_keys("Almirodil")
    time.sleep(5)
    contra.send_keys("Maledictis1")
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="userLoginId"]/div/div[1]/div[1]/button[1]').click()
    time.sleep(12)
    cierre = driver.find_elements(By.TAG_NAME, 'button')
    cierre[7].click()
    time.sleep(5)    
    cancelar=driver.execute_script("return document.getElementsByClassName('ol-decline')")
    cancelar[0].click()
    time.sleep(5)

            


def obtener_deportes(driver):
    try:
        driver.switch_to.parent_frame()
        iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        driver.switch_to.frame(iframes[0])
        time.sleep(1)
        deportes = driver.find_elements(By.TAG_NAME, 'button')
        lista = []
        for a in deportes:
            if len(a.text) > 3:
                lista.append(a)
        return lista
    except Exception as e:
        print("Error al obtener deportes:", str(e))
        return []

def apostar_en_deporte(driver, nombre):
    deportes = obtener_deportes(driver)
    if not deportes:
        print("No se encontraron deportes")
        return

    for tri in deportes:
        tri.click()
        time.sleep(5)
        partidos = driver.execute_script("return document.getElementsByClassName('lp-event__heading event-col event-col-header')")
        patron = re.compile(re.escape(nombre), re.IGNORECASE)
        
        for b in partidos:
            if patron.search(b.text):
                datos=[]
                markets=[]
                fuera=[]
                esperada=[]
                cuota1=[]
                print("Encontrado:", b.text)
                b.click()
                time.sleep(5)
                sentido=0
                intentos=0
                dati=apostar_en_partido(driver, nombre, sentido,datos, markets, fuera, esperada,cuota1,intentos)
                datos=dati[0]
                markets=dati[1]
                fuera=dati[2]
                esperada=dati[3]
                cuota1=dati[4]
                amount=dati[5]
                sentido=1
                apostar_en_partido(driver, nombre, sentido, datos, markets, fuera, esperada,cuota1,intentos,amount)

                return

    print(f"No se encontró el deporte: {nombre}")

def apostar_en_partido(driver, nombre,sentido,datos,markets,fuera,esperada,cuota1,intentos):
   fallos=[]
   cuota2=0.00 
   intentos=0
   intentos=intentos+1
   if intentos >6:
       return print('numero de intentos max 2')
   if sentido==0: 
    p = True
    while p:
        try:
            if intentos>7:
               return print('Numero de intentos maximo')
            intentos=intentos+1
            iframes = driver.find_elements(By.TAG_NAME, 'iframe')
            try:
             driver.switch_to.frame(iframes[0])
            except:
                print()
            markets = driver.execute_script("return document.getElementsByClassName('lp-offer__pick pick bet-pick')")
            elementos = driver.find_elements(By.CSS_SELECTOR,'.lp-offer__pick-heading.pick-title')
            ind = 0
            while ind < len(elementos):
                if elementos[ind].text[0:len(nombre)] == nombre:
                    valor=ind
                    break
                ind=ind+1
            cuota = float(markets[valor].text[markets[valor].text.find('\n')+1:].replace(',', '.'))
            cuota2 = float(markets[valor+1].text[markets[valor+1].text.find('\n')+1:].replace(',', '.'))
            casa = elementos[valor]
            fuera = elementos[valor+1]
            if 1.65<cuota<3.00:
                time.sleep(1)
                if sentido==0: 
                 casa.click()    
                else:
                    print("vamos con fuera")
                    fuera.click()
                datos = resolver_sistema(cuota)
                datos = datos[0]
                print(datos)
                esperada = datos[1]
                importe = driver.execute_script("return document.getElementsByClassName('lp-field_input_amount bl-ticket-payment-input ticket-payment-value decimal-only lp-field__input--error')")
                importe[0].click()
                time.sleep(4)
                importe[0].clear()
                amount = datos[2] / 100
                amount2 = 1 - amount
                if sentido==0:
                 importe[0].send_keys(str(amount))
                else:
                 importe[0].send_keys(str(amount2))   
                time.sleep(4)
                boton_rojo = driver.execute_script("return document.getElementsByClassName('lp-button')")
                dex = 0   
                while dex < len(boton_rojo):
                    if boton_rojo[dex].text == 'Apostar':
                        break
    
                    dex += 1
    
                time.sleep(4)
                boton_rojo[dex].click()
                time.sleep(4)
                boton_rojo = driver.execute_script("return document.getElementsByClassName('lp-button')")
                dex = 0
    
                while dex < len(boton_rojo):
                    if boton_rojo[dex].text == 'Confirmar':
                        break
    
                    dex += 1
    
                boton_rojo[dex].click()
                time.sleep(10)
                boton_rojo = driver.execute_script("return document.getElementsByClassName('lp-button')")
                dex = 0
    
                while dex < len(boton_rojo):
                    if boton_rojo[dex].text == 'Seguir apostando':
                        break
    
                    dex += 1
    
                boton_rojo[dex].click()
                p = False
                time.sleep(5)
                return(datos,markets,fuera,esperada,cuota,amount)

        except Exception as e:
            print("Error al apostar en el partido:", str(e))
            print(sentido)
            traceback.print_exc()
            driver.save_screenshot('captura.png')
   else:
    p = True
    esperada=float(esperada)
    guardadas=[]
    intentos=0
    while p:  
     try:  
         iframes = driver.find_elements(By.TAG_NAME, 'iframe')
         driver.switch_to.frame(iframes[0])     
         momento=driver.find_elements(By.CLASS_NAME, 'sr-lmt-plus-scb__period-number')
         momento=momento[2].text
         if momento=='3':
             markets = driver.execute_script("return document.getElementsByClassName('lp-offer__pick pick bet-pick')")
             elementos = driver.find_elements(By.CSS_SELECTOR,'.lp-offer__pick-heading.pick-title')
             ind = 0
             while ind < len(elementos):
                 if elementos[ind].text[0:len(nombre)] == nombre:
                     valor=ind
                     break
                 ind=ind+1
             cuota = float(markets[valor].text[markets[valor].text.find('\n')+1:].replace(',', '.'))
             cuota2 = float(markets[valor+1].text[markets[valor+1].text.find('\n')+1:].replace(',', '.'))
             casa = elementos[valor]
             fuera = elementos[valor+1]
             if cuota2>=1.2:
                 nuevo_amount=amount/0.2
                 fuera.click()
                 importe = driver.execute_script("return document.getElementsByClassName('lp-field_input_amount bl-ticket-payment-input ticket-payment-value decimal-only lp-field__input--error')")
                 importe[0].click()
                 time.sleep(4)
                 importe[0].clear()
                 importe[0].send_keys(str(nuevo_amount))   
                 time.sleep(4)
                 boton_rojo = driver.execute_script("return document.getElementsByClassName('lp-button')")
                 dex = 0
                 while dex < len(boton_rojo):
                     if boton_rojo[dex].text == 'Apostar':
                         break
                     dex += 1
                 time.sleep(4)
                 boton_rojo[dex].click()
                 time.sleep(4)
                 boton_rojo = driver.execute_script("return document.getElementsByClassName('lp-button')")
                 dex = 0
                 while dex < len(boton_rojo):
                     if boton_rojo[dex].text == 'Confirmar':
                         break
                     dex += 1
                 boton_rojo[dex].click()
                 time.sleep(10)
                 return
         if cuota2 <= esperada: 
          try: 

           if len(guardadas) >= 10 and all(guardadas[-1] == valor for valor in guardadas[-10:]):
                   refrescador(driver,nombre)
                   guardadas=[]
           else:               
            markets = driver.execute_script("return document.getElementsByClassName('lp-offer__pick pick bet-pick')")
            elementos = driver.find_elements(By.CSS_SELECTOR,'.lp-offer__pick-heading.pick-title')
            ind = 0
            while ind < len(elementos):
                if elementos[ind].text[0:len(nombre)] == nombre:
                    valor=ind
                    break
                ind=ind+1
            cuota = float(markets[valor].text[markets[valor].text.find('\n')+1:].replace(',', '.'))
            cuota2 = float(markets[valor+1].text[markets[valor+1].text.find('\n')+1:].replace(',', '.'))
            casa = elementos[valor]
            fuera = elementos[valor+1]
            guardadas.append(cuota2)
          except:
              refrescador(driver,nombre)              
          time.sleep(60)
         else:
            refrescador(driver,nombre)
            markets = driver.execute_script("return document.getElementsByClassName('lp-offer__pick pick bet-pick')")
            elementos = driver.find_elements(By.CSS_SELECTOR,'.lp-offer__pick-heading.pick-title')
            ind = 0
            while ind < len(elementos):
                if elementos[ind].text[0:len(nombre)] == nombre:
                    valor=ind
                    break
                ind=ind+1
            cuota = float(markets[valor].text[markets[valor].text.find('\n')+1:].replace(',', '.'))
            cuota2 = float(markets[valor+1].text[markets[valor+1].text.find('\n')+1:].replace(',', '.'))
            casa = elementos[valor]
            fuera = elementos[valor+1]
            fuera.click()
            importe = driver.execute_script("return document.getElementsByClassName('lp-field_input_amount bl-ticket-payment-input ticket-payment-value decimal-only lp-field__input--error')")
            importe[0].click()
            time.sleep(4)
            importe[0].clear()
            amount = datos[2] / 100
            amount2 = 1 - amount
            importe[0].send_keys(str(amount2))   
            time.sleep(4)
            boton_rojo = driver.execute_script("return document.getElementsByClassName('lp-button')")
            dex = 0
            while dex < len(boton_rojo):
                if boton_rojo[dex].text == 'Apostar':
                    break
                dex += 1
            time.sleep(4)
            boton_rojo[dex].click()
            time.sleep(4)
            boton_rojo = driver.execute_script("return document.getElementsByClassName('lp-button')")
            dex = 0
            while dex < len(boton_rojo):
                if boton_rojo[dex].text == 'Confirmar':
                    break
                dex += 1
            boton_rojo[dex].click()
            time.sleep(10)
            conexion = sqlite3.connect('cuotas.db')
            conexion.execute('INSERT INTO apuestas (nombre, cuota_casa,cuota_fuera) VALUES (?, ?,?)', (nombre, cuota1,cuota2))
            conexion.commit()
            p = False
            break
            time.sleep(5)
            return 
     except:   
         fallos.append('1')
         if len(fallos)>5:
             return driver
         print("falllo")
def mi_codigo(nombre):
    try:
        driver = configurar_driver()
        iniciar_sesion(driver)
        apostar_en_deporte(driver, nombre)       
    except Exception as e:
        print("Error principal:", str(e))
    finally:
       try: 
        driver.quit()
        sys.exit()    
       except: 
          driver.close()        
def refrescador(driver,nombre):
                   driver.refresh()
                   iniciar_sesion(driver)
                   deportes = obtener_deportes(driver)
                   if not deportes:
                     print(" ")
                   for tri in deportes:
                       tri.click()
                       time.sleep(3)
                       partidos = driver.execute_script("return document.getElementsByClassName('lp-event__heading event-col event-col-header')")
                       patron = re.compile(re.escape(nombre), re.IGNORECASE)         
                       for b in partidos:
                            if patron.search(b.text):   
                                b.click()
                                time.sleep(10)
                                return driver
                                


if __name__ == "__main__":
    nombre = "pepe" #sys.argv[1]
    driver=None
    proceso = multiprocessing.Process(target=mi_codigo, args=(nombre,))

       # Inicia el temporizador para 2 horas (en segundos)
    tiempo_limite = 2 * 60 * 60  # 2 horas
    proceso.start()

     # Espera a que el proceso termine o el tiempo límite se alcance
    proceso.join(tiempo_limite)

      # Si el proceso todavía está vivo, detenlo y notifica que el tiempo se agotó
    if proceso.is_alive():
     proceso.terminate()
     driver.quit()
     sys.exit()
     print("El tiempo ha expirado después de 2 horas.")
    else:
     print("La función se ha completado en menos de 2 horas.")