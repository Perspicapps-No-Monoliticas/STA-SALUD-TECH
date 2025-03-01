from pulsar.schema import *
from dataclasses import dataclass, field
from seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearRegulacionPayload(ComandoIntegracion):
    id_usuario = String()
    # TODO Cree los records para itinerarios

class ComandoCrearRegulacion(ComandoIntegracion):
    data = ComandoCrearRegulacionPayload()
    
class StartDataIntakePayload(Record):
    provider_id = String()  
        
class CommandStartDataIntake(ComandoIntegracion):
    data = StartDataIntakePayload()
    specversion = "1.0"    
    
    
class CredentialsPayload(Record):
    payload = Map(String())
    type = String()    
    
class CreateDataSourcePayload(Record):
    name = String()
    description = String()
    type = String()
    credentials = CredentialsPayload()
    provider_id = String()    
    
class CommandCreateDataSource(ComandoIntegracion):
    data = CreateDataSourcePayload()
    specversion = "1.0"     