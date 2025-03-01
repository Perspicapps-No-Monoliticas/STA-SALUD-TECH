import pulsar,_pulsar  
from pulsar.schema import *
import logging
import traceback

from aplicacion.comandos.realizar_anonimizado import AnonimizarInformacionMedica
from aplicacion.dto import InformacionMedicaDTO
from infraestructura import constantes
from infraestructura.schema.v1.eventos import DataIngestionFinished
from infraestructura import utils
from seedwork.aplicacion.comandos import ejecutar_commando

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe(constantes.EVENTO_INTEGRACION_INGESTION_CREADO, 
                                       consumer_type=_pulsar.ConsumerType.Shared,subscription_name='sta-sub-eventos', 
                                       schema=AvroSchema(DataIngestionFinished))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}')
            
            payload = InformacionMedicaDTO(
                correlation_id=mensaje.value().correlation_id,
                data_ingestion_id=mensaje.data.id_ingestion, 
                status=mensaje.data.status, 
                provider_id=mensaje.data.id_proveedor, 
                repository_out_path=mensaje.data.repository_out_path, 
                created_at=mensaje.data.created_at, 
                updated_at=mensaje.data.updated_at, 
                country_iso=mensaje.data.country_iso
            )

            # Process the anonymization
            comando = AnonimizarInformacionMedica(payload)
            ejecutar_commando(comando)
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
