"""
gestores/gestor_clientes.py

Gestor de clientes del sistema Software FJ.
Cumple el requerimiento: manejo de listas internas y validaciones estrictas.

Responsabilidades:
    - Registrar clientes con validación de duplicados.
    - Buscar clientes por identificación.
    - Listar todos los clientes activos.
    - Desactivar clientes.
"""

from typing import List, Optional
from modelos.cliente import Cliente
from helpers.log_helper import LogHelper
from excepciones.excepciones_personalizadas import (
    ClienteDuplicadoException,
    ClienteNoEncontradoException,
    ClienteInvalidoException
)


class GestorClientes:
    """
    Gestiona el ciclo de vida de los clientes en memoria (sin base de datos).
    Usa una lista interna como repositorio de clientes.
    """

    def __init__(self):
        # Lista interna de clientes (encapsulada)
        self._clientes: List[Cliente] = []

    # =========================================================
    # OPERACIONES CRUD
    # =========================================================

    def registrar(self, cliente: Cliente) -> None:
        """
        Registra un cliente nuevo en el sistema.

        Parámetros:
            cliente (Cliente): Instancia ya validada de Cliente.

        Lanza:
            ClienteInvalidoException : Si el objeto no es un Cliente válido.
            ClienteDuplicadoException: Si ya existe un cliente con esa identificación.
        """
        LogHelper.inicio_operacion(f"Registrar cliente: {cliente.nombre}")

        try:
            if not isinstance(cliente, Cliente):
                raise ClienteInvalidoException(
                    "Se esperaba una instancia de Cliente.",
                    campo="cliente"
                )

            # Verificar duplicado
            if self._existe_por_id(cliente.identificacion):
                raise ClienteDuplicadoException(cliente.identificacion)

            self._clientes.append(cliente)
            LogHelper.fin_operacion(
                f"Registrar cliente",
                f"Cliente '{cliente.nombre}' (ID: {cliente.identificacion}) registrado exitosamente."
            )

        except (ClienteInvalidoException, ClienteDuplicadoException):
            raise  # Re-lanzar para que el llamador la maneje
        except Exception as error:
            LogHelper.error(f"Error inesperado al registrar cliente: {error}")
            raise

    def buscar_por_id(self, identificacion: str) -> Cliente:
        """
        Busca y retorna un cliente por su identificación.

        Parámetros:
            identificacion (str): Documento de identidad del cliente.

        Retorna:
            Cliente: El cliente encontrado.

        Lanza:
            ClienteNoEncontradoException: Si no existe.
        """
        for cliente in self._clientes:
            if cliente.identificacion == identificacion.strip():
                return cliente
        raise ClienteNoEncontradoException(identificacion)

    def listar_todos(self) -> List[Cliente]:
        """Retorna una copia de la lista de todos los clientes."""
        return list(self._clientes)

    def listar_activos(self) -> List[Cliente]:
        """Retorna solo los clientes activos."""
        return [c for c in self._clientes if c.activo]

    def desactivar(self, identificacion: str) -> None:
        """
        Desactiva un cliente (baja lógica).

        Parámetros:
            identificacion (str): ID del cliente a desactivar.

        Lanza:
            ClienteNoEncontradoException: Si no existe.
        """
        cliente = self.buscar_por_id(identificacion)
        cliente.desactivar()
        LogHelper.info(f"Cliente '{cliente.nombre}' desactivado.")

    def total_clientes(self) -> int:
        """Retorna el número total de clientes registrados."""
        return len(self._clientes)

    # =========================================================
    # MÉTODOS PRIVADOS
    # =========================================================

    def _existe_por_id(self, identificacion: str) -> bool:
        """Verifica si ya existe un cliente con la identificación dada."""
        return any(c.identificacion == identificacion for c in self._clientes)
