"""
gestores/gestor_servicios.py

Gestor de servicios del sistema Software FJ.
Maneja el catálogo de servicios disponibles en memoria.
"""

from typing import List
from modelos.servicios import Servicio
from helpers.log_helper import LogHelper
from excepciones.excepciones_personalizadas import (
    ServicioInvalidoException,
    ServicioNoEncontradoException
)


class GestorServicios:
    """
    Gestiona el catálogo de servicios en memoria.
    """

    def __init__(self):
        self._servicios: List[Servicio] = []

    def registrar(self, servicio: Servicio) -> None:
        """
        Registra un servicio en el catálogo.

        Parámetros:
            servicio (Servicio): Servicio a registrar.

        Lanza:
            ServicioInvalidoException: Si ya existe un servicio con ese código.
        """
        LogHelper.inicio_operacion(f"Registrar servicio: {servicio.nombre}")

        try:
            if not isinstance(servicio, Servicio):
                raise ServicioInvalidoException(
                    "Se esperaba una instancia de Servicio.",
                    campo="servicio"
                )

            if self._existe_por_codigo(servicio.codigo):
                raise ServicioInvalidoException(
                    f"Ya existe un servicio con el código '{servicio.codigo}'.",
                    campo="codigo"
                )

            self._servicios.append(servicio)
            LogHelper.fin_operacion(
                "Registrar servicio",
                f"Servicio '{servicio.nombre}' (Código: {servicio.codigo}) registrado."
            )

        except ServicioInvalidoException:
            raise
        except Exception as error:
            LogHelper.error(f"Error inesperado al registrar servicio: {error}")
            raise

    def buscar_por_codigo(self, codigo: str) -> Servicio:
        """
        Busca un servicio por su código único.

        Lanza:
            ServicioNoEncontradoException: Si no existe.
        """
        codigo_buscado = codigo.strip().upper()
        for servicio in self._servicios:
            if servicio.codigo == codigo_buscado:
                return servicio
        raise ServicioNoEncontradoException(codigo)

    def listar_todos(self) -> List[Servicio]:
        """Retorna todos los servicios del catálogo."""
        return list(self._servicios)

    def listar_disponibles(self) -> List[Servicio]:
        """Retorna solo los servicios disponibles."""
        return [s for s in self._servicios if s.disponible]

    def marcar_no_disponible(self, codigo: str) -> None:
        """Marca un servicio como no disponible."""
        servicio = self.buscar_por_codigo(codigo)
        servicio.marcar_no_disponible()
        LogHelper.advertencia(f"Servicio '{servicio.nombre}' marcado como NO disponible.")

    def marcar_disponible(self, codigo: str) -> None:
        """Reactiva un servicio."""
        servicio = self.buscar_por_codigo(codigo)
        servicio.marcar_disponible()
        LogHelper.info(f"Servicio '{servicio.nombre}' marcado como disponible.")

    def total_servicios(self) -> int:
        """Número total de servicios registrados."""
        return len(self._servicios)

    def _existe_por_codigo(self, codigo: str) -> bool:
        """Verifica si ya existe un servicio con el código dado."""
        return any(s.codigo == codigo for s in self._servicios)
