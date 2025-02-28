import hashlib
import uuid
import datetime
from src.dominio.eventos import TokenizadoRealizado
from src.dominio.entidades import ImagenMedica
from pydispatch import dispatcher

class Tokenizador:
    
    def generar_token(self, medical_image: ImagenMedica):
        try:
            # Create a unique token based on image content hash and timestamp
            timestamp = datetime.datetime.now().isoformat()
            #content_hash = hashlib.sha256(medical_image.content).hexdigest()
            content_hash = hashlib.sha256(medical_image.filename.encode()).hexdigest()
            unique_id = str(uuid.uuid4())

            # Combine elements to create the token
            token_source = f"{content_hash}:{timestamp}:{unique_id}"
            token = hashlib.sha256(token_source.encode()).hexdigest()
            medical_image.token = token

            # Emit a signal to indicate tokenization is complete
            dispatcher.send(signal='TokenizadoDominio', evento=TokenizadoRealizado(token=token, img=medical_image))
        
        except Exception as e:
            print(f"Tokenization failed: {str(e)}")
        
