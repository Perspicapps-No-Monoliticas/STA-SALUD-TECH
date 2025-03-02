from infraestructura import constantes
from infraestructura.schema.v1.eventos import AnonimizacionIniciadaPayload, EventoAnonimizacionIniciada
from infraestructura.script_anonimizador import ScriptAnonimizador
from infraestructura.modelo_ia_anonimizador import ModeloIAAnonimizador
from infraestructura.despachadores import Despachador
from seedwork.aplicacion.handlers import Handler

class PipelineAnonimizacion(Handler):

    @staticmethod
    def handle_tokenizado_iniciado(evento):
        print(f'Tokenizado iniciado: {evento}')
        despachador = Despachador()
        despachador.publicar_evento(evento, constantes.EVENTO_INTEGRACION_ANONIMIZACION_INICIADO)

    @staticmethod
    def handle_tokenizado_realizado(evento):
        print(f'Tokenizado realizado: {evento}')
        ScriptAnonimizador().anonimizar(evento.token, evento.data)       

    @staticmethod
    def handle_anonimizado_por_script_realizado(evento):
        print(f'Anonimizado por script realizado: {evento}')
        ModeloIAAnonimizador().anonimizar(evento.token, evento.data)

    @staticmethod
    def handle_anonimizado_por_modelo_realizado(evento):
        print(f'Anonimizado por modelo realizado: {evento}')
        despachador = Despachador()
        despachador.publicar_evento(evento, constantes.EVENTO_INTEGRACION_ANONIMIZACION_FINALIZADO)