"""
modelos/servicios.py

Clase abstracta Servicio y tres servicios especializados con polimorfismo.
Cumple el requerimiento: clase abstracta Servicio + 3 servicios heredados con polimorfismo.

Servicios implementados:
    - ReservaSala      : Reserva de salas de reunión/conferencia.
    - AlquilerEquipo   : Alquiler de equipos tecnológicos.
    - AsesoriasEspecializada: Consultoría y asesoría profesional.

Principios OOP:
    - Abstracción    : Servicio define el contrato.
    - Herencia       : Los 3 servicios heredan de Servicio.
    - Polimorfismo   : calcular_costo() y describir() sobrescritos en cada uno.
    - Encapsulación  : Atributos privados con propiedades.
"""

from abc import abstractmethod
from modelos.entidad_base import EntidadBase
from helpers.helper import Helper
from excepciones.excepciones_personalizadas import (
    ServicioInvalidoException,
    ServicioNoDisponibleException
)


# =============================================================
# CLASE ABSTRACTA BASE: SERVICIO
# =============================================================

class Servicio(EntidadBase):
    """
    Clase abstracta que define el contrato para todos los servicios de Software FJ.

    Atributos base:
        _codigo      (str)  : Código único del servicio.
        _nombre      (str)  : Nombre del servicio.
        _tarifa_hora (float): Precio base por hora.
        _disponible  (bool) : Si el servicio está disponible para reservar.
    """

    def __init__(self, codigo: str, nombre: str, tarifa_hora: float):
        """
        Inicializa un servicio con validaciones básicas.

        Parámetros:
            codigo      (str)  : Código único identificador.
            nombre      (str)  : Nombre descriptivo.
            tarifa_hora (float): Precio por hora en COP.

        Lanza:
            ServicioInvalidoException: Si algún dato no es válido.
        """
        super().__init__()
        self.codigo = codigo
        self.nombre = nombre
        self.tarifa_hora = tarifa_hora
        self._disponible: bool = True

    # =========================================================
    # PROPIEDADES CON VALIDACIÓN
    # =========================================================

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        try:
            Helper.validar_texto_no_vacio(valor, "Código del servicio")
            self._codigo = Helper.limpiar_texto(valor).upper()
        except ValueError as error:
            raise ServicioInvalidoException(str(error), campo="codigo") from error

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        try:
            Helper.validar_texto_no_vacio(valor, "Nombre del servicio")
            Helper.validar_longitud_texto(valor, "Nombre del servicio", minimo=3, maximo=100)
            self._nombre = Helper.texto_a_titulo(valor)
        except ValueError as error:
            raise ServicioInvalidoException(str(error), campo="nombre") from error

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @tarifa_hora.setter
    def tarifa_hora(self, valor: float) -> None:
        try:
            Helper.validar_numero_positivo(valor, "Tarifa por hora")
            self._tarifa_hora = round(float(valor), 2)
        except (ValueError, TypeError) as error:
            raise ServicioInvalidoException(str(error), campo="tarifa_hora") from error

    @property
    def disponible(self) -> bool:
        return self._disponible

    # =========================================================
    # MÉTODOS ABSTRACTOS (polimorfismo)
    # =========================================================

    @abstractmethod
    def calcular_costo(self, horas: float) -> float:
        """
        Calcula el costo base del servicio para una duración dada.
        Cada servicio implementa su propia lógica de precios.
        """
        ...

    @abstractmethod
    def calcular_costo_con_impuestos(
        self,
        horas: float,
        porcentaje_iva: float = None
    ) -> float:
        """
        Calcula el costo total incluyendo IVA.
        Método sobrecargado (variante con parámetro opcional).
        """
        ...

    @abstractmethod
    def calcular_costo_con_descuento(
        self,
        horas: float,
        porcentaje_descuento: float = 0.0
    ) -> float:
        """
        Calcula el costo con un descuento aplicado.
        Método sobrecargado (variante con descuento).
        """
        ...

    @abstractmethod
    def validar_parametros(self, horas: float) -> bool:
        """
        Valida que los parámetros sean correctos para este servicio.
        """
        ...

    # =========================================================
    # MÉTODOS DE ENTIDAD BASE
    # =========================================================

    def obtener_id(self) -> str:
        return self._codigo

    # =========================================================
    # MÉTODOS DE NEGOCIO COMUNES
    # =========================================================

    def marcar_no_disponible(self) -> None:
        """Marca el servicio como no disponible."""
        self._disponible = False

    def marcar_disponible(self) -> None:
        """Marca el servicio como disponible."""
        self._disponible = True

    def verificar_disponibilidad(self) -> None:
        """
        Verifica si el servicio está disponible.

        Lanza:
            ServicioNoDisponibleException: Si no está disponible.
        """
        if not self._disponible:
            raise ServicioNoDisponibleException(
                self._nombre,
                motivo="El servicio está marcado como no disponible."
            )


# =============================================================
# SERVICIO 1: RESERVA DE SALA
# =============================================================

class ReservaSala(Servicio):
    """
    Servicio de reserva de salas de reunión o conferencia.

    Atributos adicionales:
        _capacidad_maxima (int): Número máximo de personas en la sala.
        _tiene_proyector  (bool): Si la sala tiene proyector disponible.
    """

    # Tarifa adicional por proyector (porcentaje)
    RECARGO_PROYECTOR: float = 0.10  # 10% adicional

    def __init__(
        self,
        codigo: str,
        nombre: str,
        tarifa_hora: float,
        capacidad_maxima: int,
        tiene_proyector: bool = False
    ):
        """
        Crea una sala de reuniones.

        Parámetros adicionales:
            capacidad_maxima (int) : Máximo de personas.
            tiene_proyector  (bool): Si incluye proyector.

        Lanza:
            ServicioInvalidoException: Si la capacidad no es válida.
        """
        super().__init__(codigo, nombre, tarifa_hora)
        self.capacidad_maxima = capacidad_maxima
        self._tiene_proyector = tiene_proyector

    @property
    def capacidad_maxima(self) -> int:
        return self._capacidad_maxima

    @capacidad_maxima.setter
    def capacidad_maxima(self, valor: int) -> None:
        try:
            if not isinstance(valor, int) or valor <= 0:
                raise ValueError("La capacidad máxima debe ser un entero positivo.")
            if valor > 500:
                raise ValueError("La capacidad máxima no puede superar 500 personas.")
            self._capacidad_maxima = valor
        except ValueError as error:
            raise ServicioInvalidoException(str(error), campo="capacidad_maxima") from error

    @property
    def tiene_proyector(self) -> bool:
        return self._tiene_proyector

    # =========================================================
    # IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS (polimorfismo)
    # =========================================================

    def calcular_costo(self, horas: float) -> float:
        """
        Calcula el costo base de la sala.
        Si tiene proyector, aplica recargo del 10%.

        Parámetros:
            horas (float): Duración de la reserva.

        Retorna:
            float: Costo base redondeado.
        """
        self.validar_parametros(horas)
        costo = self._tarifa_hora * horas
        if self._tiene_proyector:
            costo = costo * (1 + self.RECARGO_PROYECTOR)
        return round(costo, 2)

    def calcular_costo_con_impuestos(
        self,
        horas: float,
        porcentaje_iva: float = None
    ) -> float:
        """
        Calcula costo de la sala con IVA incluido.

        Parámetros:
            horas          (float)          : Duración.
            porcentaje_iva (float, opcional): IVA. Default: 19%.

        Retorna:
            float: Costo total con IVA.
        """
        costo_base = self.calcular_costo(horas)
        return Helper.calcular_costo_con_iva(costo_base, porcentaje_iva)

    def calcular_costo_con_descuento(
        self,
        horas: float,
        porcentaje_descuento: float = 0.0
    ) -> float:
        """
        Calcula el costo con descuento (para clientes frecuentes o grupos).

        Parámetros:
            horas                (float): Duración.
            porcentaje_descuento (float): Descuento entre 0.0 y 1.0.

        Retorna:
            float: Costo con descuento aplicado.
        """
        costo_base = self.calcular_costo(horas)
        return Helper.calcular_descuento(costo_base, porcentaje_descuento)

    def validar_parametros(self, horas: float) -> bool:
        """
        Valida las horas de reserva para una sala.

        Parámetros:
            horas (float): Duración a validar.

        Retorna:
            bool: True si son válidas.

        Lanza:
            ServicioInvalidoException: Si las horas no son válidas.
        """
        try:
            Helper.validar_horas(horas, "Horas de reserva de sala")
            return True
        except (ValueError, TypeError) as error:
            raise ServicioInvalidoException(str(error), campo="horas") from error

    def describir(self) -> str:
        """Descripción completa de la sala."""
        proyector = "Con proyector" if self._tiene_proyector else "Sin proyector"
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[Sala] {self._nombre} (Código: {self._codigo}) | "
            f"Capacidad: {self._capacidad_maxima} personas | "
            f"{proyector} | "
            f"Tarifa: {Helper.formatear_pesos(self._tarifa_hora)}/hora | "
            f"Estado: {estado}"
        )


# =============================================================
# SERVICIO 2: ALQUILER DE EQUIPO
# =============================================================

class AlquilerEquipo(Servicio):
    """
    Servicio de alquiler de equipos tecnológicos.

    Atributos adicionales:
        _tipo_equipo   (str): Tipo de equipo (laptop, proyector, cámara, etc.).
        _requiere_deposito (bool): Si se requiere depósito al alquilar.
        _valor_deposito    (float): Monto del depósito en COP.
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        tarifa_hora: float,
        tipo_equipo: str,
        requiere_deposito: bool = False,
        valor_deposito: float = 0.0
    ):
        """
        Crea un servicio de alquiler de equipo.

        Parámetros adicionales:
            tipo_equipo       (str)  : Categoría del equipo.
            requiere_deposito (bool) : Si exige depósito.
            valor_deposito    (float): Monto del depósito.
        """
        super().__init__(codigo, nombre, tarifa_hora)
        self.tipo_equipo = tipo_equipo
        self._requiere_deposito = requiere_deposito
        self._valor_deposito = max(0.0, float(valor_deposito))

    @property
    def tipo_equipo(self) -> str:
        return self._tipo_equipo

    @tipo_equipo.setter
    def tipo_equipo(self, valor: str) -> None:
        try:
            Helper.validar_texto_no_vacio(valor, "Tipo de equipo")
            self._tipo_equipo = Helper.texto_a_titulo(valor)
        except ValueError as error:
            raise ServicioInvalidoException(str(error), campo="tipo_equipo") from error

    @property
    def requiere_deposito(self) -> bool:
        return self._requiere_deposito

    @property
    def valor_deposito(self) -> float:
        return self._valor_deposito

    # =========================================================
    # IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS
    # =========================================================

    def calcular_costo(self, horas: float) -> float:
        """
        Calcula el costo del alquiler.
        Incluye el depósito si el servicio lo requiere.

        Parámetros:
            horas (float): Duración del alquiler.

        Retorna:
            float: Costo total del alquiler (sin depósito devuelto).
        """
        self.validar_parametros(horas)
        costo = self._tarifa_hora * horas
        # El depósito se cobra pero es devuelto al entregar el equipo
        # Aquí calculamos solo el costo del alquiler
        return round(costo, 2)

    def calcular_costo_con_impuestos(
        self,
        horas: float,
        porcentaje_iva: float = None
    ) -> float:
        """Costo del alquiler con IVA."""
        costo_base = self.calcular_costo(horas)
        return Helper.calcular_costo_con_iva(costo_base, porcentaje_iva)

    def calcular_costo_con_descuento(
        self,
        horas: float,
        porcentaje_descuento: float = 0.0
    ) -> float:
        """Costo del alquiler con descuento aplicado."""
        costo_base = self.calcular_costo(horas)
        return Helper.calcular_descuento(costo_base, porcentaje_descuento)

    def calcular_costo_total_con_deposito(self, horas: float) -> float:
        """
        Calcula el desembolso total inicial (alquiler + depósito).
        El depósito se devuelve al finalizar.

        Parámetros:
            horas (float): Duración del alquiler.

        Retorna:
            float: Total a pagar incluyendo depósito.
        """
        return round(self.calcular_costo(horas) + self._valor_deposito, 2)

    def validar_parametros(self, horas: float) -> bool:
        """Valida las horas de alquiler."""
        try:
            Helper.validar_horas(horas, "Horas de alquiler de equipo")
            return True
        except (ValueError, TypeError) as error:
            raise ServicioInvalidoException(str(error), campo="horas") from error

    def describir(self) -> str:
        """Descripción completa del equipo."""
        deposito_info = (
            f" | Depósito: {Helper.formatear_pesos(self._valor_deposito)}"
            if self._requiere_deposito else ""
        )
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[Equipo] {self._nombre} (Código: {self._codigo}) | "
            f"Tipo: {self._tipo_equipo} | "
            f"Tarifa: {Helper.formatear_pesos(self._tarifa_hora)}/hora"
            f"{deposito_info} | "
            f"Estado: {estado}"
        )


# =============================================================
# SERVICIO 3: ASESORÍA ESPECIALIZADA
# =============================================================

class AsesoriaEspecializada(Servicio):
    """
    Servicio de consultoría y asesoría profesional.

    Atributos adicionales:
        _especialidad    (str): Área de especialización del asesor.
        _nombre_asesor   (str): Nombre del asesor asignado.
        _horas_minimas   (float): Mínimo de horas por sesión.
        _nivel           (str): Nivel de asesoría: básico, intermedio, avanzado.
    """

    # Factores de precio según nivel
    FACTORES_NIVEL: dict = {
        "basico": 1.0,
        "intermedio": 1.5,
        "avanzado": 2.0
    }

    NIVELES_VALIDOS: list = ["basico", "intermedio", "avanzado"]

    def __init__(
        self,
        codigo: str,
        nombre: str,
        tarifa_hora: float,
        especialidad: str,
        nombre_asesor: str,
        nivel: str = "basico",
        horas_minimas: float = 1.0
    ):
        """
        Crea un servicio de asesoría.

        Parámetros adicionales:
            especialidad  (str)  : Área de expertise.
            nombre_asesor (str)  : Quién asesora.
            nivel         (str)  : Nivel: basico, intermedio, avanzado.
            horas_minimas (float): Mínimo de horas por sesión.
        """
        super().__init__(codigo, nombre, tarifa_hora)
        self.especialidad = especialidad
        self.nombre_asesor = nombre_asesor
        self.nivel = nivel
        self._horas_minimas = max(0.5, float(horas_minimas))

    @property
    def especialidad(self) -> str:
        return self._especialidad

    @especialidad.setter
    def especialidad(self, valor: str) -> None:
        try:
            Helper.validar_texto_no_vacio(valor, "Especialidad")
            self._especialidad = Helper.texto_a_titulo(valor)
        except ValueError as error:
            raise ServicioInvalidoException(str(error), campo="especialidad") from error

    @property
    def nombre_asesor(self) -> str:
        return self._nombre_asesor

    @nombre_asesor.setter
    def nombre_asesor(self, valor: str) -> None:
        try:
            Helper.validar_texto_no_vacio(valor, "Nombre del asesor")
            self._nombre_asesor = Helper.texto_a_titulo(valor)
        except ValueError as error:
            raise ServicioInvalidoException(str(error), campo="nombre_asesor") from error

    @property
    def nivel(self) -> str:
        return self._nivel

    @nivel.setter
    def nivel(self, valor: str) -> None:
        nivel_limpio = Helper.limpiar_texto(valor).lower()
        if nivel_limpio not in self.NIVELES_VALIDOS:
            raise ServicioInvalidoException(
                f"El nivel '{valor}' no es válido. "
                f"Opciones: {', '.join(self.NIVELES_VALIDOS)}.",
                campo="nivel"
            )
        self._nivel = nivel_limpio

    @property
    def horas_minimas(self) -> float:
        return self._horas_minimas

    # =========================================================
    # IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS
    # =========================================================

    def calcular_costo(self, horas: float) -> float:
        """
        Calcula el costo de la asesoría según nivel.
        Las asesorías avanzadas tienen tarifa multiplicada.

        Parámetros:
            horas (float): Duración de la sesión.

        Retorna:
            float: Costo de la asesoría.
        """
        self.validar_parametros(horas)
        factor = self.FACTORES_NIVEL.get(self._nivel, 1.0)
        costo = self._tarifa_hora * horas * factor
        return round(costo, 2)

    def calcular_costo_con_impuestos(
        self,
        horas: float,
        porcentaje_iva: float = None
    ) -> float:
        """Costo de asesoría con IVA."""
        costo_base = self.calcular_costo(horas)
        return Helper.calcular_costo_con_iva(costo_base, porcentaje_iva)

    def calcular_costo_con_descuento(
        self,
        horas: float,
        porcentaje_descuento: float = 0.0
    ) -> float:
        """Costo de asesoría con descuento."""
        costo_base = self.calcular_costo(horas)
        return Helper.calcular_descuento(costo_base, porcentaje_descuento)

    def calcular_costo_paquete(
        self,
        horas: float,
        porcentaje_descuento: float = 0.0,
        porcentaje_iva: float = None
    ) -> float:
        """
        Método sobrecargado: calcula costo completo con descuento e IVA.
        Útil para paquetes corporativos.

        Parámetros:
            horas                (float): Duración.
            porcentaje_descuento (float): Descuento a aplicar.
            porcentaje_iva       (float): IVA a aplicar.

        Retorna:
            float: Precio final del paquete.
        """
        costo_base = self.calcular_costo(horas)
        return Helper.calcular_costo_con_iva_y_descuento(
            costo_base, porcentaje_iva, porcentaje_descuento
        )

    def validar_parametros(self, horas: float) -> bool:
        """
        Valida las horas de asesoría (respeta el mínimo por sesión).

        Lanza:
            ServicioInvalidoException: Si no cumple el mínimo de horas.
        """
        try:
            Helper.validar_horas(horas, "Horas de asesoría")
        except (ValueError, TypeError) as error:
            raise ServicioInvalidoException(str(error), campo="horas") from error

        if horas < self._horas_minimas:
            raise ServicioInvalidoException(
                f"La asesoría requiere mínimo {self._horas_minimas} hora(s) por sesión. "
                f"Se solicitaron: {horas} horas.",
                campo="horas_minimas"
            )
        return True

    def describir(self) -> str:
        """Descripción completa de la asesoría."""
        factor = self.FACTORES_NIVEL.get(self._nivel, 1.0)
        tarifa_efectiva = self._tarifa_hora * factor
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[Asesoría] {self._nombre} (Código: {self._codigo}) | "
            f"Especialidad: {self._especialidad} | "
            f"Asesor: {self._nombre_asesor} | "
            f"Nivel: {self._nivel.capitalize()} | "
            f"Tarifa efectiva: {Helper.formatear_pesos(tarifa_efectiva)}/hora | "
            f"Mínimo: {self._horas_minimas}h | "
            f"Estado: {estado}"
        )
