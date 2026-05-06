"""
helpers/helper.py

Clase de ayuda con validaciones, conversiones y utilidades generales del sistema Software FJ.
Cumple el requerimiento: clase Helper con validaciones de texto, tiempo, hora y conversiones.
"""

import re
from datetime import datetime, date
from typing import Optional


class Helper:
    """
    Clase de utilidades estáticas para validaciones y conversiones del sistema.
    Centraliza todas las validaciones para evitar código duplicado.
    """

    # Constantes de validación
    LONGITUD_MINIMA_NOMBRE: int = 2
    LONGITUD_MAXIMA_NOMBRE: int = 100
    LONGITUD_MINIMA_ID: int = 5
    LONGITUD_MAXIMA_ID: int = 20
    HORAS_MINIMAS_RESERVA: float = 0.5
    HORAS_MAXIMAS_RESERVA: float = 24.0
    IVA_COLOMBIA: float = 0.19

    # =========================================================
    # VALIDACIONES DE TEXTO
    # =========================================================

    @staticmethod
    def validar_texto_no_vacio(valor: str, nombre_campo: str = "Campo") -> bool:
        """
        Verifica que un texto no esté vacío ni sea solo espacios.

        Parámetros:
            valor        (str): Texto a validar.
            nombre_campo (str): Nombre del campo para mensajes de error.

        Retorna:
            bool: True si es válido.

        Lanza:
            ValueError: Si el texto está vacío.
        """
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"El campo '{nombre_campo}' no puede estar vacío.")
        return True

    @staticmethod
    def validar_longitud_texto(
        valor: str,
        nombre_campo: str = "Campo",
        minimo: int = 2,
        maximo: int = 100
    ) -> bool:
        """
        Verifica que un texto tenga la longitud esperada.

        Parámetros:
            valor        (str): Texto a validar.
            nombre_campo (str): Nombre del campo.
            minimo       (int): Longitud mínima permitida.
            maximo       (int): Longitud máxima permitida.

        Retorna:
            bool: True si es válido.

        Lanza:
            ValueError: Si la longitud no es válida.
        """
        texto_limpio = valor.strip()
        if len(texto_limpio) < minimo:
            raise ValueError(
                f"El campo '{nombre_campo}' debe tener al menos {minimo} caracteres. "
                f"Se recibió: '{texto_limpio}' ({len(texto_limpio)} caracteres)."
            )
        if len(texto_limpio) > maximo:
            raise ValueError(
                f"El campo '{nombre_campo}' no puede tener más de {maximo} caracteres. "
                f"Se recibió: {len(texto_limpio)} caracteres."
            )
        return True

    @staticmethod
    def validar_solo_letras_y_espacios(valor: str, nombre_campo: str = "Campo") -> bool:
        """
        Verifica que un texto contenga solo letras (incluyendo acentos) y espacios.

        Parámetros:
            valor        (str): Texto a validar.
            nombre_campo (str): Nombre del campo.

        Retorna:
            bool: True si es válido.

        Lanza:
            ValueError: Si contiene caracteres no permitidos.
        """
        patron = re.compile(r"^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$")
        if not patron.match(valor.strip()):
            raise ValueError(
                f"El campo '{nombre_campo}' solo puede contener letras y espacios. "
                f"Valor recibido: '{valor}'."
            )
        return True

    # =========================================================
    # VALIDACIONES DE IDENTIFICACIÓN
    # =========================================================

    @staticmethod
    def validar_identificacion(identificacion: str) -> bool:
        """
        Verifica que una identificación sea válida (solo dígitos, longitud correcta).

        Parámetros:
            identificacion (str): Identificación a validar.

        Retorna:
            bool: True si es válida.

        Lanza:
            ValueError: Si la identificación no es válida.
        """
        Helper.validar_texto_no_vacio(identificacion, "Identificación")
        id_limpia = identificacion.strip()

        if not id_limpia.isdigit():
            raise ValueError(
                f"La identificación debe contener solo dígitos. "
                f"Valor recibido: '{id_limpia}'."
            )

        if not (Helper.LONGITUD_MINIMA_ID <= len(id_limpia) <= Helper.LONGITUD_MAXIMA_ID):
            raise ValueError(
                f"La identificación debe tener entre {Helper.LONGITUD_MINIMA_ID} "
                f"y {Helper.LONGITUD_MAXIMA_ID} dígitos. "
                f"Se recibieron {len(id_limpia)} dígitos."
            )
        return True

    # =========================================================
    # VALIDACIONES DE EMAIL
    # =========================================================

    @staticmethod
    def validar_email(email: str) -> bool:
        """
        Verifica que un email tenga un formato básico válido.

        Parámetros:
            email (str): Email a validar.

        Retorna:
            bool: True si el formato es válido.

        Lanza:
            ValueError: Si el formato no es válido.
        """
        Helper.validar_texto_no_vacio(email, "Email")
        patron = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")
        if not patron.match(email.strip()):
            raise ValueError(
                f"El email '{email}' no tiene un formato válido. "
                f"Ejemplo válido: usuario@dominio.com"
            )
        return True

    # =========================================================
    # VALIDACIONES DE DURACIÓN Y HORAS
    # =========================================================

    @staticmethod
    def validar_horas(horas: float, nombre_campo: str = "Duración") -> bool:
        """
        Verifica que una duración en horas esté en un rango válido.

        Parámetros:
            horas        (float): Duración en horas a validar.
            nombre_campo (str)  : Nombre del campo.

        Retorna:
            bool: True si es válida.

        Lanza:
            TypeError : Si el valor no es numérico.
            ValueError: Si está fuera del rango permitido.
        """
        if not isinstance(horas, (int, float)):
            raise TypeError(
                f"El campo '{nombre_campo}' debe ser un número. "
                f"Se recibió: {type(horas).__name__}."
            )

        if horas < Helper.HORAS_MINIMAS_RESERVA:
            raise ValueError(
                f"El campo '{nombre_campo}' debe ser al menos "
                f"{Helper.HORAS_MINIMAS_RESERVA} hora(s). "
                f"Se recibieron: {horas} horas."
            )

        if horas > Helper.HORAS_MAXIMAS_RESERVA:
            raise ValueError(
                f"El campo '{nombre_campo}' no puede superar "
                f"{Helper.HORAS_MAXIMAS_RESERVA} horas. "
                f"Se recibieron: {horas} horas."
            )
        return True

    @staticmethod
    def validar_numero_positivo(valor: float, nombre_campo: str = "Valor") -> bool:
        """
        Verifica que un número sea positivo (mayor que cero).

        Parámetros:
            valor        (float): Número a validar.
            nombre_campo (str)  : Nombre del campo.

        Retorna:
            bool: True si es válido.

        Lanza:
            TypeError : Si no es numérico.
            ValueError: Si no es positivo.
        """
        if not isinstance(valor, (int, float)):
            raise TypeError(
                f"El campo '{nombre_campo}' debe ser numérico. "
                f"Se recibió tipo: {type(valor).__name__}."
            )
        if valor <= 0:
            raise ValueError(
                f"El campo '{nombre_campo}' debe ser mayor que cero. "
                f"Se recibió: {valor}."
            )
        return True

    # =========================================================
    # VALIDACIONES DE FECHA Y HORA
    # =========================================================

    @staticmethod
    def validar_formato_fecha(fecha_str: str, formato: str = "%Y-%m-%d") -> date:
        """
        Verifica que una cadena tenga el formato de fecha correcto y la convierte.

        Parámetros:
            fecha_str (str): Fecha como texto.
            formato   (str): Formato esperado (por defecto: YYYY-MM-DD).

        Retorna:
            date: Objeto date si el formato es válido.

        Lanza:
            ValueError: Si el formato no es válido.
        """
        try:
            return datetime.strptime(fecha_str.strip(), formato).date()
        except ValueError:
            raise ValueError(
                f"La fecha '{fecha_str}' no tiene el formato correcto. "
                f"Formato esperado: {formato}."
            )

    @staticmethod
    def fecha_no_en_pasado(fecha: date, nombre_campo: str = "Fecha") -> bool:
        """
        Verifica que una fecha no sea anterior a hoy.

        Parámetros:
            fecha        (date): Fecha a validar.
            nombre_campo (str) : Nombre del campo.

        Retorna:
            bool: True si es válida.

        Lanza:
            ValueError: Si la fecha está en el pasado.
        """
        if fecha < date.today():
            raise ValueError(
                f"El campo '{nombre_campo}' no puede ser una fecha pasada. "
                f"Fecha recibida: {fecha}. Hoy: {date.today()}."
            )
        return True

    # =========================================================
    # CONVERSIONES Y CÁLCULOS
    # =========================================================

    @staticmethod
    def calcular_costo_con_iva(subtotal: float, porcentaje_iva: Optional[float] = None) -> float:
        """
        Calcula el costo total aplicando IVA.

        Parámetros:
            subtotal        (float)          : Valor base sin impuestos.
            porcentaje_iva  (float, opcional): Porcentaje de IVA (0.0 a 1.0).
                                              Por defecto usa IVA de Colombia (19%).

        Retorna:
            float: Costo total con IVA incluido, redondeado a 2 decimales.
        """
        iva = porcentaje_iva if porcentaje_iva is not None else Helper.IVA_COLOMBIA
        return round(subtotal * (1 + iva), 2)

    @staticmethod
    def calcular_descuento(subtotal: float, porcentaje_descuento: float) -> float:
        """
        Calcula el valor final aplicando un descuento porcentual.

        Parámetros:
            subtotal              (float): Valor base.
            porcentaje_descuento  (float): Porcentaje de descuento (0.0 a 1.0).

        Retorna:
            float: Valor con descuento aplicado, redondeado a 2 decimales.

        Lanza:
            ValueError: Si el porcentaje no está en el rango válido.
        """
        if not (0.0 <= porcentaje_descuento <= 1.0):
            raise ValueError(
                f"El porcentaje de descuento debe estar entre 0.0 y 1.0. "
                f"Se recibió: {porcentaje_descuento}."
            )
        return round(subtotal * (1 - porcentaje_descuento), 2)

    @staticmethod
    def calcular_costo_con_iva_y_descuento(
        subtotal: float,
        porcentaje_iva: Optional[float] = None,
        porcentaje_descuento: float = 0.0
    ) -> float:
        """
        Calcula el costo total con IVA y descuento combinados.
        Primero aplica el descuento y luego el IVA.

        Parámetros:
            subtotal             (float)         : Valor base.
            porcentaje_iva       (float, opcional): Porcentaje IVA.
            porcentaje_descuento (float)          : Porcentaje de descuento.

        Retorna:
            float: Valor final con descuento e IVA.
        """
        con_descuento = Helper.calcular_descuento(subtotal, porcentaje_descuento)
        return Helper.calcular_costo_con_iva(con_descuento, porcentaje_iva)

    @staticmethod
    def formatear_pesos(valor: float) -> str:
        """
        Formatea un valor numérico como moneda colombiana (COP).

        Parámetros:
            valor (float): Valor a formatear.

        Retorna:
            str: Valor formateado. Ejemplo: "$ 150,000.00 COP"
        """
        return f"$ {valor:,.2f} COP"

    @staticmethod
    def limpiar_texto(texto: str) -> str:
        """
        Elimina espacios al inicio y al final de un texto.

        Parámetros:
            texto (str): Texto a limpiar.

        Retorna:
            str: Texto limpio.
        """
        return texto.strip() if isinstance(texto, str) else ""

    @staticmethod
    def texto_a_mayusculas(texto: str) -> str:
        """
        Convierte un texto a mayúsculas después de limpiarlo.

        Parámetros:
            texto (str): Texto a convertir.

        Retorna:
            str: Texto en mayúsculas.
        """
        return Helper.limpiar_texto(texto).upper()

    @staticmethod
    def texto_a_titulo(texto: str) -> str:
        """
        Convierte un texto a formato título (primera letra de cada palabra en mayúscula).

        Parámetros:
            texto (str): Texto a convertir.

        Retorna:
            str: Texto en formato título.
        """
        return Helper.limpiar_texto(texto).title()

    @staticmethod
    def timestamp_actual() -> str:
        """
        Retorna la fecha y hora actual como texto formateado.

        Retorna:
            str: Timestamp en formato DD/MM/YYYY HH:MM:SS AM/PM.
        """
        return datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
