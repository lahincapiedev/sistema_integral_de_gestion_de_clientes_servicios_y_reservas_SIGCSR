"""
modelos/entidad_base.py

Clase abstracta base que representa cualquier entidad del sistema Software FJ.
Cumple el requerimiento: clase abstracta que represente entidades generales del sistema.

Toda entidad del sistema (Cliente, Servicio, Reserva) hereda de esta clase,
garantizando consistencia en la identificación y representación de objetos.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class EntidadBase(ABC):
    """
    Clase abstracta que define el contrato mínimo para todas las entidades del sistema.

    Atributos:
        _fecha_creacion (datetime): Fecha y hora en que se creó la entidad (encapsulado).
    """

    def __init__(self):
        # Encapsulación: fecha de creación protegida, no modificable externamente
        self._fecha_creacion: datetime = datetime.now()

    @property
    def fecha_creacion(self) -> datetime:
        """Retorna la fecha de creación de la entidad (solo lectura)."""
        return self._fecha_creacion

    @abstractmethod
    def obtener_id(self) -> str:
        """
        Retorna el identificador único de la entidad.
        Cada subclase define cuál es su identificador principal.
        """
        ...

    @abstractmethod
    def describir(self) -> str:
        """
        Retorna una descripción legible de la entidad.
        Cada subclase define cómo describirse.
        """
        ...

    def __str__(self) -> str:
        return self.describir()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id='{self.obtener_id()}')"
