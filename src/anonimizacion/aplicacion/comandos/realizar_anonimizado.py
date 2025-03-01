from dataclasses import dataclass
from dominio.entidades import ImagenMedica
from infraestructura.tokenizador import Tokenizador
from seedwork.aplicacion.comandos import ComandoHandler
from seedwork.aplicacion.comandos import ejecutar_commando as comando

@dataclass
class AnonimizarImage:
    imagen: ImagenMedica


class AnonimizarImageHandler(ComandoHandler):
    def __init__(self):
        self._pipeline:Tokenizador = Tokenizador()

    def handle(self, command: AnonimizarImage):
        return self._pipeline.generar_token(command.imagen)
    
@comando.register(AnonimizarImage)
def ejecutar_comando_crear_reserva(comando: AnonimizarImage):
    handler = AnonimizarImageHandler()
    handler.handle(comando)
    