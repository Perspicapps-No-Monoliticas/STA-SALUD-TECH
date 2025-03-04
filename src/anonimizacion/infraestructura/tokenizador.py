import hashlib
import uuid
import datetime
from aplicacion.dto import InformacionMedicaDTO
from dominio.eventos import TokenizadoIniciado, TokenizadoRealizado
from pydispatch import dispatcher
import traceback


class Tokenizador:

    def generar_token(self, medical_image: InformacionMedicaDTO):
        try:
            dispatcher.send(
                signal="TokenizadoIniciadoDominio",
                evento=TokenizadoIniciado(data=medical_image),
            )
            # Create a unique token based on image content hash and timestamp
            timestamp = datetime.datetime.now().isoformat()
            content_hash = hashlib.sha256(
                medical_image.repository_out_path.encode()
            ).hexdigest()
            unique_id = str(uuid.uuid4())

            # Combine elements to create the token
            token_source = f"{content_hash}:{timestamp}:{unique_id}"
            medical_image
            medical_image = InformacionMedicaDTO(
                **{
                    **medical_image.__dict__,
                    "token": hashlib.sha256(token_source.encode()).hexdigest(),
                }
            )
            # Emit a signal to indicate tokenization is complete
            dispatcher.send(
                signal="TokenizadoRealizadoDominio",
                evento=TokenizadoRealizado(
                    token=medical_image.token, data=medical_image
                ),
            )

        except Exception as e:
            # Stack tracr
            traceback.print_exc()
            print(f"Tokenization failed: {str(e)}")
