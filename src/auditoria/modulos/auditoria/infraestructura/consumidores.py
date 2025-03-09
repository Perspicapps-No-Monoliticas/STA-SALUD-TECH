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
            topicos_actuales = set(obtener_topicos())
            for topic in topicos_actuales:                
                if topic not in consumidores:
                    try:
                        consumidores[topic] = suscribir_topico(client, topic)
                    except:
                        logging.error(f'ERROR: Suscribiendose al topioco: {topic}')
                        
            for topico, consumer in consumidores.items():
                try:
                    msg = consumer.receive(timeout_millis=1000)                                       
                    contenido = msg.data()
                    esquema_avro = obtener_esquema(topico)
                    if esquema_avro:
                        try:
                            with io.BytesIO(contenido) as bio:
                                evento = fastavro.schemaless_reader(bio, esquema_avro) 
                                ejecutar_proyeccion(ProyeccionAuditoriaLista(topico, evento), app=app)
                        except Exception as e:
                            print(f"Error al decodificar AVRO: {e}")             
                    consumer.acknowledge(msg)     
                except pulsar.Timeout:
                    pass
            time.sleep(10)
    except KeyboardInterrupt:
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
    try:
        consumidor = cliente.subscribe(topic, subscription_name="auditoria-suscripcion", consumer_type=pulsar.ConsumerType.Shared)
        return consumidor               
    except Exception as e:
        logging.error(f'ERROR: Suscribiendose al topico {topic}')
        logging.error(f'ERROR: Suscribiendose al {e}')
        traceback.print_exc()
        
def obtener_esquema(topic):
    topico_limpio = topic.replace("persistent://", "")
    url = f"{ADMIN_URL}/schemas/{topico_limpio}/schema"
    response = requests.get(url)
    if response.status_code == 200:
        esquema_json = response.json().get("data")
        return json.loads(esquema_json)
    return None


