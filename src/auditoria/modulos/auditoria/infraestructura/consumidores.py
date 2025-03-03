import pulsar,_pulsar
from pulsar.schema import *
import time
import fastavro
import json
from modulos.auditoria.infraestructura.proyecciones import *
from seedwork.infraestructura import utils
import requests
import io
import fastavro
import json
from seedwork.infraestructura.proyecciones import ejecutar_proyeccion
import threading

ADMIN_URL = f'http://{utils.broker_host()}:8080/admin/v2'

def realizar_suscripcion(app=None):
    consumidores = {}   
        
    client = pulsar.Client(f'pulsar://{utils.broker_host()}:6650', operation_timeout_seconds=30)
    try:
        while True:
            print(f"BUSCANDO TOPICOS CADA 10 SEGUNDOS")
            topicos_actuales = set(obtener_topicos())
            print(f"    LOS TOPICOS ENCONTRADOS SON {topicos_actuales}")
            for topic in topicos_actuales:                
                if topic not in consumidores:
                    try:
                        print(f"             INSCRIBIENDO A TOPICO {topic}")
                        consumidores[topic] = suscribir_topico(client, topic)
                    except:
                        logging.error(f'ERROR: Suscribiendose al topioco: {topic}')
                        
            for topico, consumer in consumidores.items():
                try:
                    msg = consumer.receive(timeout_millis=1000)                   
                    #####
                    contenido = msg.data()  # Se recibe en formato binario (bytes)
                    print(f"Mensaje recibido EN BINARIO DINAMICO : {topic}")
                    ejecutar_proyeccion(ProyeccionAuditoriaLista(topic, contenido), app=app)               
                    consumer.acknowledge(msg) 
                    #####       
                except pulsar.Timeout:
                    pass  # No hay mensajes nuevos aún
            time.sleep(10)
    except KeyboardInterrupt:
        print("Cerrando consumidor...")
        client.close()

def obtener_topicos():
    NAMESPACE = "public/default"
    url = f"{ADMIN_URL}/persistent/{NAMESPACE}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException as e:
        print(f"Error obteniendo topicos: {e}")
    return []

def suscribir_topico(cliente, topic, app=None):
    print(f"SUSCRIBIENDOSE A TOPICO : {topic}")
    try:
        consumidor = cliente.subscribe(topic, subscription_name="auditoria-suscripcion", consumer_type=pulsar.ConsumerType.Shared)
        print(f"SUSCRITO CON EXITO A TOPICO : {topic}")          
        return consumidor               
    except Exception as e:
        logging.error(f'ERROR: Suscribiendose al topico {topic}')
        logging.error(f'ERROR: Suscribiendose al {e}')
        traceback.print_exc()


