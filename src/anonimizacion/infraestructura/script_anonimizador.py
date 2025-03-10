from aplicacion.dto import InformacionMedicaDTO
from dominio.entidades import InformacionMedica
from dominio.eventos import AnonimizadoPorScriptRealizado
from pydispatch import dispatcher
import time

class ScriptAnonimizador:
    
    def anonimizar(self, token: str, medical_image: InformacionMedicaDTO):    
        try:
            # Supongamos que aquí hizo una anonimizacion basica
            print("Anonimizando datos con script...")
            time.sleep(2)
            print("Anonimizado exitoso!!!")
    
            # Emit a signal to indicate tokenization is complete
            dispatcher.send(signal='AnonimizadoScriptDominio', evento=AnonimizadoPorScriptRealizado(token=token, data=medical_image))          
        except Exception as e:
            # Fallback to original content if processing fails
            print(f"Script anonymization failed: {str(e)}")    
