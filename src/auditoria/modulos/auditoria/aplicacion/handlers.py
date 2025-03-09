from seedwork.aplicacion.handlers import Handler
from modulos.auditoria.infraestructura.despachadores import Despachador

class HandlerRegulacionIntegracion(Handler):

    @staticmethod
    def handle_regulacion_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-regulacion')


    