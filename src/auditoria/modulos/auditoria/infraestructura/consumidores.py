from modulos.auditoria.infraestructura.constantes import EVENTO_INTEGRACION_ANONIMIZACION_INICIADO, EVENTO_INTEGRACION_INGESTION_CREADO
import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from modulos.auditoria.infraestructura.schema.v1.eventos import EventoRegulacionCreada, EventDataSourceCreated
from modulos.auditoria.infraestructura.schema.v1.comandos import ComandoCrearRegulacion


from modulos.auditoria.infraestructura.proyecciones import ProyeccionRegulacionesLista
from seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from seedwork.infraestructura import utils

def suscribirse_a_eventos(app=None):
    print("SUSCRBIRSE A ESUCHAR LOS EVENTOS DE PULSAR AL INICAR LA APP REGULACIONES")
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-regulacion', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='sta-sub-eventos', schema=AvroSchema(EventoRegulacionCreada))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido EN PULSAR REGULacion: {datos}')

            # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
            ejecutar_proyeccion(ProyeccionRegulacionesLista(datos.id_regulacion, datos.nombre, datos.region, datos.version, datos.fecha_creacion, 
                                                            datos.requisitos, datos.fecha_creacion), app=app)
            
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!#1')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('comandos-regulacion', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='sta-sub-comandos', schema=AvroSchema(ComandoCrearRegulacion))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos en Regulacion Consumidor!')
        traceback.print_exc()
        if cliente:
            cliente.close()
            
            
def suscribirse_a_eventos_ingestion_creada(app=None):
    print("SUSCRBIRSE A ESUCHAR LOS EVENTOS DE ingestion_creada")
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')                        
        consumidor = cliente.subscribe(EVENTO_INTEGRACION_INGESTION_CREADO,  consumer_type=_pulsar.ConsumerType.Shared,subscription_name='sta-sub-eventos', schema=AvroSchema(EventDataSourceCreated))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido EN PULSAR ingestion_creada: {datos}')       
            ejecutar_proyeccion(ProyeccionRegulacionesLista(datos.id, EVENTO_INTEGRACION_INGESTION_CREADO, 'PENDING', 'V_1', datos.created_at, 
                                                            [], datos.updated_at), app=app)     

            # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
            
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos ingestion_creada')
        traceback.print_exc()
        if cliente:
            cliente.close()
                 
