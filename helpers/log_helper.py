"""
helpers/log_helper.py

Helper centralizado para el registro de eventos y errores del sistema Software FJ.
Cumple el requerimiento: registrar todos los errores y eventos relevantes en archivo de logs.

Funcionalidad:
    - Escribe cada entrada con fecha y hora exacta
    - Soporta niveles: INFO, WARNING, ERROR, DEBUG
    - Crea automáticamente la carpeta de logs si no existe
    - Muestra cada entrada también en consola
    - Genera un archivo de log por día (formato: YYYY-MM-DD.log)
"""

import os
from datetime import datetime


class LogHelper:
    """
    Clase estática que gestiona el registro de eventos del sistema.
    Inspirada en el patrón LogHelper de proyectos empresariales reales.
    """

    # Ruta base donde se almacenarán los archivos de log
    RUTA_LOGS: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")

    # Separador visual para marcar inicio/fin del sistema
    SEPARADOR: str = "=" * 60

    @staticmethod
    def _obtener_ruta_archivo() -> str:
        """
        Construye la ruta del archivo de log para el día actual.

        Retorna:
            str: Ruta completa del archivo de log (ej: logs/2026-05-02.log)
        """
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(LogHelper.RUTA_LOGS, f"{fecha_hoy}.log")

    @staticmethod
    def _asegurar_directorio() -> None:
        """
        Crea el directorio de logs si no existe.
        No lanza excepción si ya existe.
        """
        if not os.path.exists(LogHelper.RUTA_LOGS):
            os.makedirs(LogHelper.RUTA_LOGS)

    @staticmethod
    def log(texto: str, nivel: str = "INFO") -> None:
        """
        Registra un mensaje en el archivo de log y en consola.

        El formato de cada línea es:
            DD/MM/YYYY HH:MM:SS    [NIVEL]    mensaje

        Parámetros:
            texto  (str): Mensaje a registrar.
            nivel  (str): Nivel del log. Valores posibles: INFO, WARNING, ERROR, DEBUG.
                          Por defecto: INFO.
        """
        try:
            LogHelper._asegurar_directorio()
            ahora = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
            entrada = f"{ahora}\t[{nivel}]\t{texto}"

            # Escribir en archivo (modo append para no sobreescribir)
            with open(LogHelper._obtener_ruta_archivo(), "a", encoding="utf-8") as archivo:
                archivo.write(entrada + "\n")

            # Mostrar en consola
            print(entrada)

        except Exception as error_log:
            # Si el log falla, al menos mostramos en consola (no podemos relanzar)
            print(f"[ERROR CRÍTICO EN LOG]: {error_log}")

    @staticmethod
    def info(texto: str) -> None:
        """Registra un evento informativo."""
        LogHelper.log(texto, nivel="INFO")

    @staticmethod
    def advertencia(texto: str) -> None:
        """Registra una advertencia."""
        LogHelper.log(texto, nivel="WARNING")

    @staticmethod
    def error(texto: str) -> None:
        """Registra un error."""
        LogHelper.log(texto, nivel="ERROR")

    @staticmethod
    def debug(texto: str) -> None:
        """Registra un mensaje de depuración."""
        LogHelper.log(texto, nivel="DEBUG")

    @staticmethod
    def inicio_sistema(nombre_sistema: str) -> None:
        """
        Registra el inicio formal del sistema con separador visual.

        Parámetros:
            nombre_sistema (str): Nombre del sistema que inicia.
        """
        LogHelper.log("")
        LogHelper.log(LogHelper.SEPARADOR)
        LogHelper.log(f"------- INICIO DEL SISTEMA: {nombre_sistema} -------")
        LogHelper.log(LogHelper.SEPARADOR)

    @staticmethod
    def fin_sistema(nombre_sistema: str, tiempo_segundos: float) -> None:
        """
        Registra el fin formal del sistema con separador visual.

        Parámetros:
            nombre_sistema (str): Nombre del sistema que finaliza.
            tiempo_segundos (float): Tiempo total de ejecución en segundos.
        """
        LogHelper.log(LogHelper.SEPARADOR)
        LogHelper.log(f"------- FIN DEL SISTEMA: {nombre_sistema} -------")
        LogHelper.log(f"Tiempo total de ejecución: {tiempo_segundos:.4f} segundos")
        LogHelper.log(LogHelper.SEPARADOR)
        LogHelper.log("")

    @staticmethod
    def inicio_modulo(nombre_modulo: str) -> None:
        """Registra el inicio de un módulo."""
        LogHelper.log(f"START: Módulo --- {nombre_modulo}")

    @staticmethod
    def fin_modulo(nombre_modulo: str, resultado: str = "") -> None:
        """Registra el fin de un módulo."""
        sufijo = f": {resultado}" if resultado else ""
        LogHelper.log(f"FINISH: Módulo --- {nombre_modulo}{sufijo}")

    @staticmethod
    def inicio_operacion(nombre_operacion: str) -> None:
        """Registra el inicio de una operación."""
        LogHelper.log(f"START: Operación --- {nombre_operacion}")

    @staticmethod
    def fin_operacion(nombre_operacion: str, resultado: str = "") -> None:
        """Registra el fin de una operación."""
        sufijo = f": {resultado}" if resultado else ""
        LogHelper.log(f"FINISH: Operación --- {nombre_operacion}{sufijo}")

    @staticmethod
    def detalle(texto: str) -> None:
        """Registra un detalle específico de una operación."""
        LogHelper.log(f"Details: {texto}")

    @staticmethod
    def resultado(texto: str) -> None:
        """Registra el resultado de una operación."""
        LogHelper.log(f"Results: {texto}")

    @staticmethod
    def separador_simulacion(numero: int, descripcion: str) -> None:
        """
        Registra el encabezado de una simulación numerada.

        Parámetros:
            numero      (int): Número de la simulación.
            descripcion (str): Descripción breve de la simulación.
        """
        LogHelper.log("-" * 50)
        LogHelper.log(f"SIMULACIÓN #{numero}: {descripcion}")
        LogHelper.log("-" * 50)
