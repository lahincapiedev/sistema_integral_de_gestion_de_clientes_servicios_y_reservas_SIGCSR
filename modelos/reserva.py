"""
modelos/reserva.py

Clase Reserva que integra cliente, servicio, duración y estado.
Cumple el requerimiento: clase Reserva con confirmación, cancelación y excepciones.

Estados posibles de una reserva:
    PENDIENTE  → CONFIRMADA → COMPLETADA
    PENDIENTE  → CANCELADA
    CONFIRMADA → CANCELADA
"""

import uuid
from enum import Enum
from modelos.entidad_base import EntidadBase
from modelos.cliente import Cliente
from modelos.servicios import Servicio
from helpers.helper import Helper
from excepciones.excepciones_personalizadas import (
    ReservaInvalidaException,
    ServicioNoDisponibleException
)


class EstadoReserva(Enum):
    """
    Enumeración de los posibles estados de una reserva.
    Garantiza que solo se usen estados válidos (encapsulación del dominio).
    """
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    COMPLETADA = "Completada"


class Reserva(EntidadBase):
    """
    Representa una reserva en el sistema Software FJ.
    Integra un cliente, un servicio y una duración, con ciclo de vida controlado.

    Atributos:
        _id_reserva    (str)          : Identificador único auto-generado.
        _cliente       (Cliente)      : Cliente que realiza la reserva.
        _servicio      (Servicio)     : Servicio reservado.
        _horas         (float)        : Duración de la reserva en horas.
        _estado        (EstadoReserva): Estado actual de la reserva.
        _motivo_cancel (str)          : Motivo de cancelación (si aplica).
    """

    def __init__(self, cliente: Cliente, servicio: Servicio, horas: float):
        """
        Crea una nueva reserva validando todos los componentes.

        Parámetros:
            cliente  (Cliente) : Cliente que reserva (no puede ser None).
            servicio (Servicio): Servicio a reservar (no puede ser None).
            horas    (float)   : Duración en horas.

        Lanza:
            ReservaInvalidaException     : Si cliente o servicio son inválidos.
            ServicioNoDisponibleException: Si el servicio no está disponible.
        """
        super().__init__()
        # Validar que los objetos no sean None antes de asignar
        self._validar_cliente(cliente)
        self._validar_servicio(servicio)

        # Verificar disponibilidad del servicio (lanza excepción si no está disponible)
        servicio.verificar_disponibilidad()

        self._id_reserva: str = str(uuid.uuid4())[:8].upper()
        self._cliente: Cliente = cliente
        self._servicio: Servicio = servicio
        self._estado: EstadoReserva = EstadoReserva.PENDIENTE
        self._motivo_cancelacion: str = ""

        # Validar horas mediante el servicio (polimorfismo)
        self._servicio.validar_parametros(horas)
        self._horas: float = horas

    # =========================================================
    # VALIDACIONES INTERNAS
    # =========================================================

    @staticmethod
    def _validar_cliente(cliente: Cliente) -> None:
        """Verifica que el cliente sea un objeto Cliente válido."""
        if cliente is None:
            raise ReservaInvalidaException("El cliente no puede ser None.")
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaException(
                f"Se esperaba un objeto Cliente, se recibió: {type(cliente).__name__}."
            )
        if not cliente.activo:
            raise ReservaInvalidaException(
                f"El cliente '{cliente.nombre}' está inactivo y no puede realizar reservas."
            )

    @staticmethod
    def _validar_servicio(servicio: Servicio) -> None:
        """Verifica que el servicio sea un objeto Servicio válido."""
        if servicio is None:
            raise ReservaInvalidaException("El servicio no puede ser None.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaException(
                f"Se esperaba un objeto Servicio, se recibió: {type(servicio).__name__}."
            )

    # =========================================================
    # PROPIEDADES (solo lectura para mantener integridad)
    # =========================================================

    @property
    def id_reserva(self) -> str:
        return self._id_reserva

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def horas(self) -> float:
        return self._horas

    @property
    def estado(self) -> EstadoReserva:
        return self._estado

    @property
    def motivo_cancelacion(self) -> str:
        return self._motivo_cancelacion

    # =========================================================
    # MÉTODOS DE ENTIDAD BASE
    # =========================================================

    def obtener_id(self) -> str:
        return self._id_reserva

    def describir(self) -> str:
        """Descripción completa de la reserva."""
        costo = self._servicio.calcular_costo(self._horas)
        return (
            f"Reserva #{self._id_reserva} | "
            f"Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | "
            f"Duración: {self._horas}h | "
            f"Costo: {Helper.formatear_pesos(costo)} | "
            f"Estado: {self._estado.value}"
        )

    # =========================================================
    # CICLO DE VIDA DE LA RESERVA
    # =========================================================

    def confirmar(self) -> None:
        """
        Confirma la reserva (PENDIENTE → CONFIRMADA).

        Lanza:
            ReservaInvalidaException: Si no está en estado PENDIENTE.
        """
        if self._estado != EstadoReserva.PENDIENTE:
            raise ReservaInvalidaException(
                f"Solo se pueden confirmar reservas en estado PENDIENTE. "
                f"Estado actual: {self._estado.value}."
            )
        self._estado = EstadoReserva.CONFIRMADA

    def cancelar(self, motivo: str = "Sin motivo especificado") -> None:
        """
        Cancela la reserva (PENDIENTE o CONFIRMADA → CANCELADA).

        Parámetros:
            motivo (str): Razón de la cancelación.

        Lanza:
            ReservaInvalidaException: Si ya está completada o cancelada.
        """
        estados_cancelables = [EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA]
        if self._estado not in estados_cancelables:
            raise ReservaInvalidaException(
                f"No se puede cancelar una reserva en estado {self._estado.value}."
            )
        self._estado = EstadoReserva.CANCELADA
        self._motivo_cancelacion = Helper.limpiar_texto(motivo)

    def completar(self) -> None:
        """
        Marca la reserva como completada (CONFIRMADA → COMPLETADA).

        Lanza:
            ReservaInvalidaException: Si no está confirmada.
        """
        if self._estado != EstadoReserva.CONFIRMADA:
            raise ReservaInvalidaException(
                f"Solo se pueden completar reservas CONFIRMADAS. "
                f"Estado actual: {self._estado.value}."
            )
        self._estado = EstadoReserva.COMPLETADA

    # =========================================================
    # CÁLCULOS DE COSTO (métodos sobrecargados)
    # =========================================================

    def calcular_costo_base(self) -> float:
        """Calcula el costo base de la reserva sin impuestos ni descuentos."""
        return self._servicio.calcular_costo(self._horas)

    def calcular_costo_con_iva(self, porcentaje_iva: float = None) -> float:
        """
        Calcula el costo con IVA.

        Parámetros:
            porcentaje_iva (float, opcional): IVA a aplicar. Default: 19%.

        Retorna:
            float: Costo con IVA.
        """
        return self._servicio.calcular_costo_con_impuestos(self._horas, porcentaje_iva)

    def calcular_costo_con_descuento(self, porcentaje_descuento: float) -> float:
        """
        Calcula el costo con descuento.

        Parámetros:
            porcentaje_descuento (float): Descuento entre 0.0 y 1.0.

        Retorna:
            float: Costo con descuento.
        """
        return self._servicio.calcular_costo_con_descuento(self._horas, porcentaje_descuento)
