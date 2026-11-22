"""Clase abstracta base para las entidades generales del sistema."""
from abc import ABC, abstractmethod
from itertools import count


class Entidad(ABC):
    """Abstracción de cualquier entidad identificable del sistema."""

    _contador = count(1)

    def __init__(self) -> None:
        self._id = next(Entidad._contador)

    @property
    def id(self) -> int:
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción legible de la entidad."""

    def __str__(self) -> str:
        return self.describir()
