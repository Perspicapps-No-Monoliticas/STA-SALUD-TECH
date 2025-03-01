from dataclasses import dataclass
from aplicacion.dto import InformacionMedicaDTO
from infraestructura.tokenizador import Tokenizador
from seedwork.aplicacion.comandos import ComandoHandler
from seedwork.aplicacion.comandos import ejecutar_commando as comando

@dataclass
class AnonimizarInformacionMedica:
    informacionMedica:InformacionMedicaDTO

class AnonimizarImageHandler(ComandoHandler):
    def __init__(self):
        self._pipeline:Tokenizador = Tokenizador()

    def handle(self, command: AnonimizarInformacionMedica):
        
        return self._pipeline.generar_token(command.informacionMedica)
    
@comando.register(AnonimizarInformacionMedica)
def ejecutar_comando_crear_reserva(comando: AnonimizarInformacionMedica):
    handler = AnonimizarImageHandler()
    handler.handle(comando)
    