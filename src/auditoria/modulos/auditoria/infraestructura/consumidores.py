from modulos.auditoria.infraestructura.constantes import *
import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from modulos.auditoria.infraestructura.schema.v1.eventos import *
from modulos.auditoria.infraestructura.schema.v1.comandos import *


from modulos.auditoria.infraestructura.proyecciones import *
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
            ejecutar_proyeccion(ProyeccionRegulacionesLista(datos.id_regulacion, datos.nombre, datos.region, datos.payload, datos.fecha_creacion, 
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
            print(f'Evento recibido EN PULSAR ingestion_creada: { mensaje.value()}')    
            datos = mensaje.value().data
            print(f'Evento recibido EN PULSAR ingestion_creada: {datos}')    
            print(f'Evento recibido EN PULSAR ingestion_creada: {mensaje.value()}')       
            ejecutar_proyeccion(ProyeccionAuditoriaLista(EVENTO_INTEGRACION_INGESTION_CREADO, datos), app=app)                 
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos ingestion_creada')
        traceback.print_exc()
        if cliente:
            cliente.close()
            
            
def suscribirse_a_eventos_anonimizacion_finalizada_v1(app=None):
    print("SUSCRBIRSE A ESUCHAR LOS EVENTOS DE finalizada_v1")
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')                        
        consumidor = cliente.subscribe(EVENTO_INTEGRACION_ANONIMIZACION_FINALIZADO,  consumer_type=_pulsar.ConsumerType.Shared,subscription_name='sta-sub-eventos' , schema=AvroSchema(EventoAnonimizacionFinalizada))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido EN PULSAR ingestion_creada: {datos}')       
            ejecutar_proyeccion(ProyeccionAuditoriaLista(EVENTO_INTEGRACION_ANONIMIZACION_FINALIZADO, datos), app=app)    
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos finalizada_v1')
        traceback.print_exc()
        if cliente:
            cliente.close()           
            
def suscribirse_a_eventos_anonimizacion_iniciado(app=None):
    print("SUSCRBIRSE A ESUCHAR LOS EVENTOS DE anonimizacion_iniciado")
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')                        
        consumidor = cliente.subscribe(EVENTO_INTEGRACION_ANONIMIZACION_INICIADO,  consumer_type=_pulsar.ConsumerType.Shared,subscription_name='sta-sub-eventos' , schema=AvroSchema(EventoAnonimizacionIniciada))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido EN PULSAR anonimizacion_iniciado: {datos}')       
            ejecutar_proyeccion(ProyeccionAuditoriaLista(EVENTO_INTEGRACION_ANONIMIZACION_INICIADO, datos), app=app)    
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos anonimizacion_iniciado')
        traceback.print_exc()
        if cliente:
            cliente.close()        
            
def suscribirse_a_comandos_inicio_ingestion(app=None):
    print("SUSCRBIRSE A ESUCHAR LOS EVENTOS DE inicio_ingestion")
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')                        
        consumidor = cliente.subscribe(START_DATA_INGESTION_V1_TOPIC,  consumer_type=_pulsar.ConsumerType.Shared,subscription_name='sta-sub-eventos' , schema=AvroSchema(CommandStartDataIntake))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido EN PULSAR inicio_ingestion: {datos}')       
            ejecutar_proyeccion(ProyeccionAuditoriaLista(START_DATA_INGESTION_V1_TOPIC, datos), app=app)    
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos inicio_ingestion')
        traceback.print_exc()
        if cliente:
            cliente.close()         
            
def suscribirse_a_comandos_inicio_creacion_datasource(app=None):
    print("SUSCRBIRSE A ESUCHAR LOS EVENTOS DE CREATE_DATA_SOURCE")
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')                        
        consumidor = cliente.subscribe(CREATE_DATA_SOURCE_V1_TOPIC,  consumer_type=_pulsar.ConsumerType.Shared,subscription_name='sta-sub-eventos' , schema=AvroSchema(CommandCreateDataSource))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido EN PULSAR CREATE_DATA_SOURCE: {datos}')       
            ejecutar_proyeccion(ProyeccionAuditoriaLista(CREATE_DATA_SOURCE_V1_TOPIC, datos), app=app)    
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos CREATE_DATA_SOURCE')
        traceback.print_exc()
        if cliente:
            cliente.close()                 
            
                 
