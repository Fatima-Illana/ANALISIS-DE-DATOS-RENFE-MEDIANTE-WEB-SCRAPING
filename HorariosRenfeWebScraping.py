from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import random
import time
import csv

# Especificar la ruta donde está localizado el driver.
DRIVER_LOCATION = r'.\chromedriver_win32\chromedriver.exe'


def driver_init():
    """Función que inicia el driver según la ruta indicada"""
    return webdriver.Chrome(DRIVER_LOCATION)


#*************************************************************************
#RECURSO: HORARIOS PUNTUALIDAD DE LOS TRENES EN ESTACION PTA ATOCHA
#*************************************************************************


# ABRIMOS LA PÁGINA Y ACEPTAMOS LA COOKIES

driver = driver_init()
url = "https://www.renfe.com/es/es"

driver.maximize_window()  # Abrimos en pantalla completa para que la página no tenga cambios respecto a la original.
time.sleep(1)
driver.get(url)

# Pulsamos el botón de las cookies
time.sleep(2)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-reject-all-handler']"))).click()
time.sleep(random.uniform(0, 4))


# INTERACCIONAMOS CON LA PÁGINA PARA DIRIGIRNOS A LA SECCIÓN DESEADA

for i in range(2):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contentPage"]/div/div/div[1]/div/div'
                                                                          '/div/div/div/div/rf-header/rf-header-top/div[1]/div/ul[1]/li[1]/rf-submenu/span'))).click()
    time.sleep(random.uniform(0, 4))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contentPage"]/div/div/div[1]/div/div'
                                                                          '/div/div/div/div/rf-header/rf-header-top/div[1]/div/ul[1]/li[1]/rf-submenu/div/div/div/ul[2]/li/ul/li[4]/a'))).click()
# Repetimos este proceso dos veces, ya que la página tiene un error y al darle la primera vez nos lleva a la página
# inicial de nuevo.


# RELLENAMOS LOS CAMPOS PARA OBTENER LA TABLA DESEADA

Estacion = driver.find_element('id', 'IdEstacion')
Estacion.send_keys('Madrid-Puerta De')
# Escribimos a medias la opción deseada para darle tiempo a exponer las opciones disponibles.
time.sleep(3)
Estacion.send_keys(' Atocha')
# Seleccionamos la opción deseada:
time.sleep(2)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[11]/ul/li/strong"))).click()
time.sleep(3)
driver.execute_script("window.scrollTo(0, 100);")
time.sleep(3)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="divBotonBuscar1"]/a'))).click()
time.sleep(3)
# Nos movemos por la página, hacia abajo, para que la tabla esté en el dominio y podamos interaccionar con ella:
driver.execute_script("window.scrollTo(100, 600);")
time.sleep(2)


# BUSCAMOS INFORMACIÓN GENERAL SOBRE LAS TABLAS Y LOS DATOS

# El número de columnas de las tablas, que es igual para todas:
nColumnas = len(driver.find_elements(By.XPATH, "/html/body/form/div[3]/div[12]/div[5]/div[3]/div/div/div[1]/div[2]/table/thead/tr/th"))

# La fecha en la que se hizo dicha consulta:
fechaConsulta = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[12]/div[1]/p/span[2]").text

# El nombre de la estación a la que estamos accediendo:
nombreEstacion = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[12]/div[5]/div[2]/p/span").text


# PROCESAMOS LAS TABLAS DE LA SECCIÓN DE LLEGADAS

nTablas = len(driver.find_elements(By.XPATH, '//*[@id="botoneraidTablaTrenesLlegadas0"]/tbody/tr/td[2]/input'))
tablaLLegadas = []

for tabla in range(1, nTablas + 1):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='botoneraidTablaTrenesLlegadas0']/tbody/tr/td[2]/input["+str(tabla)+"]"))).click()
    time.sleep(2)
    nFilas = len(driver.find_elements(By.XPATH, "/html/body/form/div[3]/div[12]/div[5]/div[3]/div/div/div[1]/div[2]/table/tbody[2]/tr"))
    for x in range(1, nFilas+1):
        fila = []
        primerElemento = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[12]/div[5]/div[3]/div/div/div[1]/div[2]/table/tbody[2]/tr[" + str(x) + "]/td[1]/span").text
        fila.append(primerElemento)
        for y in range(2, nColumnas+1):
            elemento = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[12]/div[5]/div[3]/div/div/div[1]/div[2]/table/tbody[2]/tr["+str(x)+"]/td["+str(y)+"]").text
            fila.append(elemento)
        tablaLLegadas.append(fila)


# TÍTULOS DE LAS TABLAS DE LLEGADAS:

titulosLLegadas = []
for indice in range(1, nColumnas+1):
    titulo = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[12]/div[5]/div[3]/div/div/div[1]/div[2]/table/thead/tr/th["+str(indice)+"]/div/span/a").text
    titulosLLegadas.append(titulo)


# PROCESAMOS LAS TABLAS DE LA SECCIÓN DE SALIDAS

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="linkSalidasTrenes"]'))).click()
nTablas2 = len(driver.find_elements(By.XPATH, '//*[@id="botoneraidTablaTrenesSalidas0"]/tbody/tr/td[2]/input'))
tablaSalidas = []

for tabla in range(1, nTablas2 + 1):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='botoneraidTablaTrenesSalidas0']/tbody/tr/td[2]/input["+str(tabla)+"]"))).click()
    time.sleep(2)
    nFilas2 = len(driver.find_elements(By.XPATH, "/html/body/form/div[3]/div[12]/div[5]/div[3]/div/div/div[2]/div[2]/table/tbody[2]/tr"))
    for x in range(1, nFilas2+1):
        fila = []
        primerElemento = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[12]/div[5]/div[3]/div/div/div[2]/div[2]/table/tbody[2]/tr[" + str(x) + "]/td[1]/span").text
        fila.append(primerElemento)
        for y in range(2, nColumnas+1):
            elemento = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[12]/div[5]/div[3]/div/div/div[2]/div[2]/table/tbody[2]/tr["+str(x)+"]/td["+str(y)+"]").text
            fila.append(elemento)
        tablaSalidas.append(fila)


# TÍTULOS DE LAS TABLAS DE SALIDA QUE SE DIFERENCIAN EN 1 ELEMENTO RESPECTO A LA DE LLEGADAS:

titulosSalidas = titulosLLegadas.copy()
titulosSalidas[1] = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[12]/div[5]/div[3]/div/div/div[2]/div[2]/table/thead/tr/th[2]/div/span/a").text


# COPIAMOS LOS DATOS OBTENIDOS EN UN FICHERO CSV

with open('HorariosLargaDistancia.csv', 'w', newline='\n') as csvfile:
    csvtool = csv.writer(csvfile, delimiter=',')
    csvtool.writerow(["Información consultada el " + fechaConsulta])
    csvtool.writerow(["Estación: " + nombreEstacion])
    csvtool.writerow(titulosLLegadas)
    for elem in tablaLLegadas:
        csvtool.writerow(elem)
    csvtool.writerow(titulosSalidas)
    for elem2 in tablaSalidas:
        csvtool.writerow(elem2)

driver.close()