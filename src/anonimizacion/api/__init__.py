import threading

import infraestructura
import infraestructura.consumidores

threading.Thread(target=infraestructura.consumidores.suscribirse_a_eventos).start()