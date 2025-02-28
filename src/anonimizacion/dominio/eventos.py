from dataclasses import dataclass
from src.dominio.entidades import ImagenMedica
from src.seedwork.dominio.eventos import EventoDominio

@dataclass
class TokenizadoRealizado(EventoDominio):
    token: str = ""
    img: ImagenMedica = None

    def __str__(self):
        return self.__class__.__name__

@dataclass
class AnonimizadoPorScriptRealizado(EventoDominio):
    token: str = ""
    img: ImagenMedica = None

    def __str__(self):
        return self.__class__.__name__

@dataclass
class AnonimizadoPorModeloRealizado(EventoDominio):
    token: str = ""
    img: ImagenMedica = None

    def __str__(self):
        return self.__class__.__name__