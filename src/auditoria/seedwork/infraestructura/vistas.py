from abc import ABC, abstractmethod

class Vista(ABC):

    @abstractmethod
    def obtener_por(**kwargs):
        ...

    @abstractmethod
    def obtener_todas():
        ...