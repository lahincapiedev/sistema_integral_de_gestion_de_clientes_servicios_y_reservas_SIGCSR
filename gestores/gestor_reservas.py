"""
gestores/gestor_reservas.py

Gestor de reservas del sistema Software FJ.
Administra el ciclo de vida de las reservas en memoria.
"""

from typing import List
from modelos.reserva import Reserva, EstadoReserva
from modelos.cliente import Cliente
from modelos.servicios import Servicio
from helpers.log_helper import LogHelper
from helpers.helper import Helper
from excepciones.excepciones_personalizadas import (
    ReservaNoEncontradaException,
    ReservaDuplicadaException,
    ReservaInvalidaException,
    ServicioNoDisponibleException
)


class GestorReservas:
    """
    Gestiona las reservas del sistema en memoria (sin base de datos).
    """

    def __init__(self):
        self._reservas: List[Reserva] = []

    def crear_reserva(self, cliente: Cliente, servicio: Servicio, horas: float) -> Reserva:
        """
        Crea y registra una nueva reserva.

        Parámetros:
            cliente  (Cliente) : Cliente que reserva.
            servicio (Servicio): Servicio a reservar.
            horas    (float)   : Duración en horas.

        Retorna:
            Reserva: La reserva creada.

        Lanza:
            ReservaInvalidaException     : Si los datos son inválidos.
            ServicioNoDisponibleException: Si el servicio no está disponible.
        """
        LogHelper.inicio_operacion(
            f"Crear reserva: {cliente.nombre} → {servicio.nombre} ({horas}h)"
        )

        try:
            # La clase Reserva valida internamente todo
            nueva_reserva = Reserva(cliente=cliente, servicio=servicio, horas=horas)
            self._reservas.append(nueva_reserva)

            costo = nueva_reserva.calcular_costo_base()
            LogHelper.fin_operacion(
                "Crear reserva",
                f"Reserva #{nueva_reserva.id_reserva} creada. "
                f"Costo base: {Helper.formatear_pesos(costo)}"
            )
            return nueva_reserva

        except (ReservaInvalidaException, ServicioNoDisponibleException):
            raise
        except Exception as error:
            LogHelper.error(f"Error inesperado al crear reserva: {error}")
            raise

    def confirmar(self, reserva: Reserva) -> None:
        """
        Confirma una reserva existente.

        Parámetros:
            reserva (Reserva): Reserva a confirmar.

        Lanza:
            ReservaInvalidaException: Si la reserva no puede confirmarse.
        """
        LogHelper.inicio_operacion(f"Confirmar reserva #{reserva.id_reserva}")
        try:
            reserva.confirmar()
            LogHelper.fin_operacion(
                f"Confirmar reserva #{reserva.id_reserva}",
                "Confirmada exitosamente."
            )
        except ReservaInvalidaException:
            raise

    def cancelar(self, id_reserva: str, motivo: str = "Sin motivo") -> None:
        """
        Cancela una reserva por su ID.

        Parámetros:
            id_reserva (str): ID de la reserva.
            motivo     (str): Razón de cancelación.

        Lanza:
            ReservaNoEncontradaException: Si no existe.
            ReservaInvalidaException    : Si no puede cancelarse.
        """
        LogHelper.inicio_operacion(f"Cancelar reserva #{id_reserva}")
        try:
            reserva = self.buscar_por_id(id_reserva)
            reserva.cancelar(motivo)
            LogHelper.fin_operacion(
                f"Cancelar reserva #{id_reserva}",
                f"Cancelada. Motivo: {motivo}"
            )
        except (ReservaNoEncontradaException, ReservaInvalidaException):
            raise

    def completar(self, id_reserva: str) -> None:
        """
        Marca una reserva como completada.

        Lanza:
            ReservaNoEncontradaException: Si no existe.
            ReservaInvalidaException    : Si no está confirmada.
        """
        LogHelper.inicio_operacion(f"Completar reserva #{id_reserva}")
        reserva = self.buscar_por_id(id_reserva)
        reserva.completar()
        LogHelper.fin_operacion(f"Completar reserva #{id_reserva}", "Completada exitosamente.")

    def buscar_por_id(self, id_reserva: str) -> Reserva:
        """
        Busca una reserva por su ID.

        Lanza:
            ReservaNoEncontradaException: Si no existe.
        """
        for reserva in self._reservas:
            if reserva.id_reserva == id_reserva.upper():
                return reserva
        raise ReservaNoEncontradaException(id_reserva)

    def listar_por_cliente(self, identificacion_cliente: str) -> List[Reserva]:
        """Retorna todas las reservas de un cliente específico."""
        return [
            r for r in self._reservas
            if r.cliente.identificacion == identificacion_cliente
        ]

    def listar_por_estado(self, estado: EstadoReserva) -> List[Reserva]:
        """Retorna todas las reservas con un estado específico."""
        return [r for r in self._reservas if r.estado == estado]

    def listar_todas(self) -> List[Reserva]:
        """Retorna todas las reservas."""
        return list(self._reservas)

    def total_reservas(self) -> int:
        """Número total de reservas."""
        return len(self._reservas)
