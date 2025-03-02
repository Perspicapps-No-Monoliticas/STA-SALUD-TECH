from aplicacion.dto import InformacionMedicaDTO
from dominio.entidades import InformacionMedica
from dominio.eventos import AnonimizadoPorModeloRealizado
from pydispatch import dispatcher
import time

class ModeloIAAnonimizador:
    
    def __init__(self):
        # In a real application, you would load your AI model here
        self.model_loaded = False
    
    def anonimizar(self, token:str, medical_image: InformacionMedicaDTO):
        try:
            # Supongamos que aquí hizo una anonimizacion basica
            print("Anonimizando con modelo IA...")
            time.sleep(2)
            print("Anonimizado exitoso!!!")

            # Emit a signal to indicate tokenization is complete
            dispatcher.send(signal='AnonimizadoModeloDominio', evento=AnonimizadoPorModeloRealizado(token=token, data=medical_image))
        except Exception as e:
            # Fallback to original content if processing fails
            print(f"Anonimizando con modelo IA fallo: {str(e)}")