import requests
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from urllib3.exceptions import InsecureRequestWarning
import warnings

# Desactivar la advertencia InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

ruta_archivo_parametros = './config/parametros.xml'
arbol = ET.parse(ruta_archivo_parametros)
raiz = arbol.getroot()

urls = [url.text for url in raiz.findall('.//urls/url')]
descripcion = [node.find('description').text for node in raiz.findall('.//node')]

variables = {elemento.tag: elemento.text for elemento in raiz.iter() if elemento.text is not None}
nombre_usuario = variables.get('username')
contrasena_usuario = variables.get('password')
ruta_guardar_log = variables.get('outpath')
tiempo_max_respuesta = float(variables.get('MaxTiempoRespuesta_seg'))
webhook_url = variables.get('Webhook')

# Lista para almacenar notificaciones
notificaciones = []

# Función para enviar notificaciones a Teams
def enviar_notificacion(titulo, mensaje):
    message = {
        "text": f"{titulo}\n{mensaje}",
    }
    response = requests.post(webhook_url, json=message)
    if response.status_code != 200:
        print(f"Error al enviar la notificación. Código de estado: {response.status_code}")
        print(response.text)

# Manejador para advertencias SSL
def ssl_warn(*args, **kwargs):
    pass

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def estado(url):
    tiempo_ejecucion = 0
    try:
        inicio_tiempo = time.time()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            resultado = requests.get(url, verify=False, timeout=tiempo_max_respuesta)

        fin_tiempo = time.time()
        tiempo_ejecucion = round(fin_tiempo - inicio_tiempo, 2)

        with open(ruta_guardar_log, 'a', encoding='utf-8') as archivo:

            if 'FACTURADOR WEB' in descripcion:
                if 200 <= resultado.status_code <= 299 or resultado.status_code == 401:
                    archivo.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")},OK,{resultado.status_code},{tiempo_ejecucion},{url}\n')
                else:
                    archivo.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")},ERROR,{resultado.status_code},{tiempo_ejecucion},{url}\n')

                    notificaciones.append(f" - {url}\n"
                                         f"ERROR: {resultado.status_code}\n"
                                         f"TIME: {tiempo_ejecucion} segundos\n\n")

            else:
                if 200 <= resultado.status_code <= 299:
                    archivo.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")},OK,{resultado.status_code},{tiempo_ejecucion},{url}\n')
                else:
                    archivo.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")},ERROR,{resultado.status_code},{tiempo_ejecucion},{url}\n')

                    notificaciones.append(f" - {url}\n"
                                         f"ERROR: {resultado.status_code}\n"
                                         f"TIME: {tiempo_ejecucion} Seg\n\n")

    except requests.Timeout:
        with open(ruta_guardar_log, 'a', encoding='utf-8') as archivo:
            archivo.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")},TIMEOUT,504,{tiempo_max_respuesta:.2f},{url}\n')

            notificaciones.append(f" - {url}\n"
                                  f"ERROR: 504\n"
                                  f"TIME: {tiempo_max_respuesta} Seg\n\n")

    except requests.RequestException:
        with open(ruta_guardar_log, 'a', encoding='utf-8') as archivo:
            archivo.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")},ERROR,404,{tiempo_ejecucion},{url}\n')

            notificaciones.append(f" - {url}\n"
                                 f"ERROR: 404\n"
                                 f"TIME: {tiempo_ejecucion} Seg\n\n")

# Aquí utilizamos ThreadPoolExecutor para ejecutar las solicitudes en paralelo.
with ThreadPoolExecutor(max_workers=len(urls)) as executor:
    executor.map(estado, urls)

# Enviar notificación consolidada al final
enviar_notificacion(f"**WARNING - {' '.join(descripcion)}**\n\nProblemas detectados en las siguientes URLs.\n\n", "\n\n".join(notificaciones))
