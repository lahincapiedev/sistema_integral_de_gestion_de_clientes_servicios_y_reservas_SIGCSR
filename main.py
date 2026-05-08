"""
main.py

Punto de entrada principal del sistema Software FJ.
Inspirado en el patrón de módulos del ejemplo C# de la guía,
adaptado a Python con gestión de módulos por nombre.

Uso:
    python main.py                  → Ejecuta todas las simulaciones
    python main.py clientes         → Ejecuta solo el módulo de clientes
    python main.py servicios        → Ejecuta solo el módulo de servicios
    python main.py reservas         → Ejecuta solo el módulo de reservas
    python main.py completo         → Ejecuta el flujo completo de simulaciones
"""

import sys
from datetime import datetime
from helpers.log_helper import LogHelper
from simulaciones.simulador_sistema import SimuladorSistema


# =============================================================
# CONSTANTES DE MÓDULOS DISPONIBLES
# =============================================================

MODULO_CLIENTES = "clientes"
MODULO_SERVICIOS = "servicios"
MODULO_RESERVAS = "reservas"
MODULO_COMPLETO = "completo"
MODULO_TODOS = "todos"

MODULOS_DISPONIBLES = [
    MODULO_CLIENTES,
    MODULO_SERVICIOS,
    MODULO_RESERVAS,
    MODULO_COMPLETO,
    MODULO_TODOS,
]


# =============================================================
# FUNCIÓN: EJECUTAR MÓDULO ESPECÍFICO
# =============================================================

def ejecutar_modulo(simulador: SimuladorSistema, nombre_modulo: str) -> None:
    """
    Ejecuta un módulo específico del sistema.

    Parámetros:
        simulador     (SimuladorSistema): Instancia del simulador.
        nombre_modulo (str)             : Nombre del módulo a ejecutar.
    """
    LogHelper.inicio_modulo(nombre_modulo.upper())

    if nombre_modulo == MODULO_CLIENTES:
        # Módulo solo de registro de clientes (simulaciones 1-10)
        LogHelper.info("Ejecutando módulo: Registro de Clientes")
        simulador._sim_cliente_valido_completo()
        simulador._sim_cliente_valido_minimo()
        simulador._sim_cliente_nombre_vacio()
        simulador._sim_cliente_email_invalido()
        simulador._sim_cliente_id_corta()
        simulador._sim_cliente_id_con_letras()
        simulador._sim_cliente_duplicado()
        simulador._sim_cliente_nombre_con_numeros()
        simulador._sim_cliente_email_sin_arroba()
        simulador._sim_cliente_nombre_muy_corto()

    elif nombre_modulo == MODULO_SERVICIOS:
        # Módulo solo de registro de servicios (simulaciones 11-21)
        LogHelper.info("Ejecutando módulo: Registro de Servicios")
        simulador._sim_sala_valida_con_proyector()
        simulador._sim_sala_valida_sin_proyector()
        simulador._sim_equipo_valido_con_deposito()
        simulador._sim_equipo_valido_sin_deposito()
        simulador._sim_asesoria_valida_avanzada()
        simulador._sim_asesoria_valida_basica()
        simulador._sim_servicio_tarifa_negativa()
        simulador._sim_servicio_nombre_vacio()
        simulador._sim_asesoria_nivel_invalido()
        simulador._sim_sala_capacidad_cero()
        simulador._sim_servicio_duplicado()

    elif nombre_modulo == MODULO_RESERVAS:
        # Módulo solo de reservas (requiere datos previos)
        LogHelper.info("Ejecutando módulo: Reservas (requiere clientes y servicios)")
        # Preparar datos mínimos necesarios
        simulador._sim_cliente_valido_completo()
        simulador._sim_cliente_valido_minimo()
        simulador._sim_sala_valida_con_proyector()
        simulador._sim_sala_valida_sin_proyector()
        simulador._sim_equipo_valido_con_deposito()
        simulador._sim_asesoria_valida_avanzada()
        simulador._sim_asesoria_valida_basica()
        # Ejecutar reservas
        simulador._sim_reserva_sala_exitosa()
        simulador._sim_reserva_equipo_exitosa()
        simulador._sim_reserva_asesoria_exitosa()
        simulador._sim_reserva_confirmar()
        simulador._sim_reserva_completar()
        simulador._sim_reserva_servicio_no_disponible()
        simulador._sim_reserva_horas_cero()
        simulador._sim_reserva_horas_excesivas()
        simulador._sim_reserva_cliente_inactivo()
        simulador._sim_cancelar_reserva_valida()

    elif nombre_modulo == MODULO_COMPLETO:
        # Flujo completo en un solo módulo
        LogHelper.info("Ejecutando módulo: Flujo completo")
        simulador._sim_cliente_valido_completo()
        simulador._sim_sala_valida_con_proyector()
        simulador._sim_flujo_completo_exitoso()

    elif nombre_modulo == MODULO_TODOS:
        # Todas las simulaciones
        simulador.ejecutar_todas()

    else:
        LogHelper.advertencia(
            f"Módulo '{nombre_modulo}' no reconocido. "
            f"Módulos disponibles: {', '.join(MODULOS_DISPONIBLES)}"
        )

    LogHelper.fin_modulo(nombre_modulo.upper())


# =============================================================
# PUNTO DE ENTRADA PRINCIPAL
# =============================================================

def main():
    """
    Función principal del sistema Software FJ.
    Gestiona el inicio, ejecución y cierre ordenado del sistema.
    """
    inicio = datetime.now()

    # Obtener módulos a ejecutar desde argumentos de línea de comandos
    argumentos = sys.argv[1:] if len(sys.argv) > 1 else [MODULO_TODOS]

    try:
        # Encabezado del sistema (visible en log y consola)
        LogHelper.log("")
        LogHelper.log("=" * 60)
        LogHelper.log("------- INICIO DEL SISTEMA Software FJ -------")
        LogHelper.log("=" * 60)
        LogHelper.info(f"Módulos a ejecutar: {', '.join(argumentos)}")

        # Crear instancia del simulador
        simulador = SimuladorSistema()

        # Ejecutar cada módulo especificado
        for nombre_modulo in argumentos:
            try:
                ejecutar_modulo(simulador, nombre_modulo.lower())
            except Exception as error_modulo:
                LogHelper.error(
                    f"ERROR en módulo '{nombre_modulo}': {error_modulo}"
                )
                LogHelper.error(f"El sistema continúa con el siguiente módulo.")

        LogHelper.log("=" * 60)
        LogHelper.info("INFORMATION: Ejecución de módulos finalizada.")

    except Exception as error_critico:
        LogHelper.error(
            f"ERROR CRÍTICO: {error_critico}"
        )

    finally:
        # Calcular tiempo total de ejecución
        fin = datetime.now()
        tiempo_ejecucion = (fin - inicio).total_seconds()

        LogHelper.log("=" * 60)
        LogHelper.log("------- FIN DEL SISTEMA Software FJ -------")
        LogHelper.info(f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos")
        LogHelper.log("=" * 60)
        LogHelper.log("")


# =============================================================
# INVOCACIÓN
# =============================================================

if __name__ == "__main__":
    main()
