from src.infraestructura.tokenizador import Tokenizador
from src.infraestructura.script_anonimizador import ScriptAnonimizador
from src.infraestructura.modelo_ia_anonimizador import ModeloIAAnonimizador
from src.seedwork.aplicacion.handlers import Handler

class PipelineAnonimizacion(Handler):

    def __init__(self,):
        self.tokenizer = Tokenizador()

    def procesar(self, medical_image) -> str:
        self.tokenizer.generar_token(medical_image)
        return medical_image.token

    @staticmethod
    def handle_tokenizado_realizado(evento):
        print(f'Tokenizado realizado: {evento}')
        ScriptAnonimizador().anonimizar(evento.token, evento.img)       

    @staticmethod
    def handle_anonimizado_por_script_realizado(evento):
        print(f'Anonimizado por script realizado: {evento}')
        ModeloIAAnonimizador().anonimizar(evento.token, evento.img)

    @staticmethod
    def handle_anonimizado_por_modelo_realizado(evento):
        print(f'Anonimizado por modelo realizado: {evento}')
              