import pulsar,_pulsar  
from pulsar.schema import *
import logging
import traceback

from infraestructura import constantes
from infraestructura.schema.v1.eventos import EventDataSourceCreated
import utils

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe(constantes.EVENTO_INTEGRACION_INGESTION_CREADO, 
                                       consumer_type=_pulsar.ConsumerType.Shared,subscription_name='sta-sub-eventos', 
                                       schema=AvroSchema(EventDataSourceCreated))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}')
            
            # Create domain entities
            #metadata = MetadatosImagen(source_filename= mensaje.metadata.source_filename, dicom_tags=mensaje.metadata.dicom_tags) 
            #medical_image = ImagenMedica(id_ingestion=mensaje.id_ingestion, id_proveedor=mensaje.id_proveedor, filename=mensaje.filename, metadata=metadata)
        
            # Process the anonymization
            #comando = AnonimizarImage(medical_image)
            #ejecutar_commando(comando)
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
