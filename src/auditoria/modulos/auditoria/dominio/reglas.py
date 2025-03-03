"""Reglas de negocio del dominio de cliente

En este archivo usted encontrará reglas de negocio del dominio de cliente

"""

from seedwork.dominio.reglas import ReglaNegocio

class MinimoUnRequisito(ReglaNegocio):

    def __init__(self, mensaje='La lista de  debe tener al menos un '):
        super().__init__(mensaje)

    def es_valido(self) -> bool:
        return True