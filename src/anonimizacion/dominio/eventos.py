from dataclasses import dataclass
from dominio.entidades import ImagenMedica, InformacionMedica
from seedwork.dominio.eventos import EventoDominio

@dataclass
class TokenizadoIniciado(EventoDominio):
    img: ImagenMedica = None

    def __str__(self):
        return self.__class__.__name__

@dataclass
class TokenizadoRealizado(EventoDominio):
    token: str = ""
    data: InformacionMedica = None

    def __str__(self):
        return self.__class__.__name__

@dataclass
class AnonimizadoPorScriptRealizado(EventoDominio):
    token: str = ""
    data: InformacionMedica = None

    def __str__(self):
        return self.__class__.__name__

@dataclass
class AnonimizadoPorModeloRealizado(EventoDominio):
    token: str = ""
    data: InformacionMedica = None

    def __str__(self):
        return self.__class__.__name__