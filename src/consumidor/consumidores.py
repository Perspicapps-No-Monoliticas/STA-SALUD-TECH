import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback

from v1.eventos import EventoAnonimizacionIniciada, EventoAnonimizacionFinalizada
import utils

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('anonimizacion_finalizada_v1', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='sta-sub-eventos', schema=AvroSchema(EventoAnonimizacionFinalizada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()


suscribirse_a_eventos()
#def suscribirse_a_comandos():
#    cliente = None
#    try:
#        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
#        consumidor = cliente.subscribe('comandos-reserva', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='aeroalpes-sub-comandos', schema=AvroSchema(ComandoCrearReserva))
#
#        while True:
#            mensaje = consumidor.receive()
#            print(f'Comando recibido: {mensaje.value().data}')
#
#            consumidor.acknowledge(mensaje)     
#            
#        cliente.close()
#    except:
#        logging.error('ERROR: Suscribiendose al tópico de comandos!')
#        traceback.print_exc()
#        if cliente:
#            cliente.close()