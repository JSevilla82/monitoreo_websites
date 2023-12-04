import requests
import time
import xml.etree.ElementTree as ET

ruta_archivo_parametros = 'C:\\Users\\sevillaj\\Desktop\\Aplicación Python\\parametros.xml'
arbol = ET.parse(ruta_archivo_parametros)
raiz = arbol.getroot()

urls = [url.text for url in raiz.findall('.//urls/url')]

variables = {elemento.tag: elemento.text for elemento in raiz.iter() if elemento.text is not None}
nombre_usuario = variables.get('username')
contrasena_usuario = variables.get('password')

ruta_guardar_log = rf'C:\Users\sevillaj\Desktop\monitoreo.log'

def estado(url):
    try:
        inicio_tiempo = time.time()
        resultado = requests.get(url, verify=False)
        fin_tiempo = time.time()

        tiempo_ejecucion = round(fin_tiempo - inicio_tiempo, 2)
        with open(ruta_guardar_log, 'a') as archivo:
            if 200 <= resultado.status_code <= 226 or resultado.status_code == 401:
                archivo.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")}, OK ({resultado.status_code}), {tiempo_ejecucion}, {url}\n')
            else:
                archivo.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")}, KO ({resultado.status_code}), {tiempo_ejecucion}, {url}\n')

    except requests.RequestException:
        with open(ruta_guardar_log, 'a') as archivo:
            archivo.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")}, KO (Error), {tiempo_ejecucion}, {url}\n')     

for url in urls:
    estado(url)
