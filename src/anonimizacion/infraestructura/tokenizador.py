import hashlib
import uuid
import datetime
from aplicacion.dto import InformacionMedicaDTO
from dominio.eventos import TokenizadoIniciado, TokenizadoRealizado
from pydispatch import dispatcher

class Tokenizador:
    
    def generar_token(self, medical_image: InformacionMedicaDTO):
        try:
            dispatcher.send(signal='TokenizadoIniciadoDominio', evento=TokenizadoIniciado(img=medical_image))
            # Create a unique token based on image content hash and timestamp
            timestamp = datetime.datetime.now().isoformat()
            content_hash = hashlib.sha256(medical_image.repository_out_path.encode()).hexdigest()
            unique_id = str(uuid.uuid4())

            # Combine elements to create the token
            token_source = f"{content_hash}:{timestamp}:{unique_id}"
            medical_image.token = hashlib.sha256(token_source.encode()).hexdigest()

            # Emit a signal to indicate tokenization is complete
            dispatcher.send(signal='TokenizadoRealizadoDominio', evento=TokenizadoRealizado(token=medical_image.token, data=medical_image))
        
        except Exception as e:
            print(f"Tokenization failed: {str(e)}")
        
