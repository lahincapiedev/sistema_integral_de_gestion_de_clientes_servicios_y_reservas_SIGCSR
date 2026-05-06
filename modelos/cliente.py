"""
modelos/cliente.py

Clase Cliente con validaciones robustas y encapsulación de datos personales.
Cumple el requerimiento: clase Cliente con validaciones robustas y encapsulación.

Principios OOP aplicados:
    - Encapsulación: atributos privados con getters/setters que validan
    - Herencia: extiende EntidadBase
    - Validación: usa Helper para todas las validaciones
"""

from modelos.entidad_base import EntidadBase
from helpers.helper import Helper
from excepciones.excepciones_personalizadas import ClienteInvalidoException


class Cliente(EntidadBase):
    """
    Representa un cliente registrado en el sistema Software FJ.

    Atributos (encapsulados con propiedades):
        _nombre          (str): Nombre completo del cliente.
        _identificacion  (str): Número de identificación único.
        _email           (str): Correo electrónico de contacto.
        _telefono        (str): Teléfono de contacto (opcional).
        _activo          (bool): Indica si el cliente está activo.
    """

    def __init__(
        self,
        nombre: str,
        identificacion: str,
        email: str,
        telefono: str = ""
    ):
        """
        Crea un nuevo cliente validando todos sus datos.

        Parámetros:
            nombre         (str): Nombre completo. Solo letras y espacios.
            identificacion (str): Documento de identidad. Solo dígitos, 5-20 caracteres.
            email          (str): Correo electrónico válido.
            telefono       (str): Teléfono opcional.

        Lanza:
            ClienteInvalidoException: Si algún dato no pasa las validaciones.
        """
        super().__init__()
        # Usamos los setters para aprovechar las validaciones
        self.nombre = nombre
        self.identificacion = identificacion
        self.email = email
        self.telefono = telefono
        self._activo: bool = True

    # =========================================================
    # PROPIEDADES CON VALIDACIÓN (encapsulación)
    # =========================================================

    @property
    def nombre(self) -> str:
        """Nombre completo del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y asigna el nombre del cliente."""
        try:
            Helper.validar_texto_no_vacio(valor, "Nombre")
            Helper.validar_longitud_texto(
                valor, "Nombre",
                minimo=Helper.LONGITUD_MINIMA_NOMBRE,
                maximo=Helper.LONGITUD_MAXIMA_NOMBRE
            )
            Helper.validar_solo_letras_y_espacios(valor, "Nombre")
            self._nombre = Helper.texto_a_titulo(valor)
        except (ValueError, TypeError) as error:
            raise ClienteInvalidoException(str(error), campo="nombre") from error

    @property
    def identificacion(self) -> str:
        """Número de identificación del cliente."""
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor: str) -> None:
        """Valida y asigna la identificación del cliente."""
        try:
            Helper.validar_identificacion(valor)
            self._identificacion = Helper.limpiar_texto(valor)
        except (ValueError, TypeError) as error:
            raise ClienteInvalidoException(str(error), campo="identificacion") from error

    @property
    def email(self) -> str:
        """Correo electrónico del cliente."""
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        """Valida y asigna el email del cliente."""
        try:
            Helper.validar_email(valor)
            self._email = Helper.limpiar_texto(valor).lower()
        except (ValueError, TypeError) as error:
            raise ClienteInvalidoException(str(error), campo="email") from error

    @property
    def telefono(self) -> str:
        """Teléfono de contacto del cliente (puede estar vacío)."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Asigna el teléfono; no es obligatorio."""
        self._telefono = Helper.limpiar_texto(valor) if valor else ""

    @property
    def activo(self) -> bool:
        """Indica si el cliente está activo en el sistema."""
        return self._activo

    # =========================================================
    # MÉTODOS DE ENTIDAD BASE (contrato abstracto)
    # =========================================================

    def obtener_id(self) -> str:
        """Retorna la identificación como ID único del cliente."""
        return self._identificacion

    def describir(self) -> str:
        """Retorna una descripción completa y legible del cliente."""
        estado = "Activo" if self._activo else "Inactivo"
        telefono_info = f" | Tel: {self._telefono}" if self._telefono else ""
        return (
            f"Cliente: {self._nombre} | "
            f"ID: {self._identificacion} | "
            f"Email: {self._email}"
            f"{telefono_info} | "
            f"Estado: {estado}"
        )

    # =========================================================
    # MÉTODOS DE NEGOCIO
    # =========================================================

    def desactivar(self) -> None:
        """Marca el cliente como inactivo (baja lógica)."""
        self._activo = False

    def activar(self) -> None:
        """Reactiva un cliente previamente desactivado."""
        self._activo = True

    def actualizar_email(self, nuevo_email: str) -> None:
        """
        Actualiza el email del cliente con validación.

        Parámetros:
            nuevo_email (str): Nuevo correo electrónico.

        Lanza:
            ClienteInvalidoException: Si el email no es válido.
        """
        self.email = nuevo_email

    def actualizar_telefono(self, nuevo_telefono: str) -> None:
        """
        Actualiza el teléfono del cliente.

        Parámetros:
            nuevo_telefono (str): Nuevo número de teléfono.
        """
        self.telefono = nuevo_telefono
