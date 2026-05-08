"""
simulaciones/simulador_sistema.py

Clase encargada de ejecutar todas las simulaciones del sistema Software FJ.
Cumple el requerimiento: al menos 10 operaciones completas (válidas e inválidas).
En total se ejecutan más de 50 operaciones para demostrar robustez del sistema.

Cada simulación sigue el flujo:
    crear datos → validar → ejecutar lógica → puede fallar →
    manejar excepción → registrar log → el sistema continúa
"""

from gestores.gestor_clientes import GestorClientes
from gestores.gestor_servicios import GestorServicios
from gestores.gestor_reservas import GestorReservas
from modelos.cliente import Cliente
from modelos.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from modelos.reserva import EstadoReserva
from helpers.log_helper import LogHelper
from helpers.helper import Helper
from excepciones.excepciones_personalizadas import (
    ClienteInvalidoException,
    ClienteDuplicadoException,
    ClienteNoEncontradoException,
    ServicioInvalidoException,
    ServicioNoDisponibleException,
    ServicioNoEncontradoException,
    ReservaInvalidaException,
    ReservaNoEncontradaException,
    DescuentoInvalidoException,
    SoftwareFJException
)


class SimuladorSistema:
    """
    Ejecuta los escenarios de simulación del sistema Software FJ.
    Demuestra manejo robusto de excepciones en más de 50 operaciones.
    """

    def __init__(self):
        # Inicializar los tres gestores.
        self.gestor_clientes = GestorClientes()
        self.gestor_servicios = GestorServicios()
        self.gestor_reservas = GestorReservas()

        # Contador de simulaciones
        self._numero_simulacion: int = 0
        self._exitosas: int = 0
        self._con_error_controlado: int = 0

    # =========================================================
    # MÉTODO PRINCIPAL DE EJECUCIÓN
    # =========================================================

    def ejecutar_todas(self) -> None:
        """
        Ejecuta todas las simulaciones en orden lógico.
        El sistema NO se detiene ante ningún error.
        """
        LogHelper.inicio_sistema("Software FJ - Sistema de Gestión")

        # --- BLOQUE 1: Registro de clientes ---
        self._sim_cliente_valido_completo()
        self._sim_cliente_valido_minimo()
        self._sim_cliente_nombre_vacio()
        self._sim_cliente_email_invalido()
        self._sim_cliente_id_corta()
        self._sim_cliente_id_con_letras()
        self._sim_cliente_duplicado()
        self._sim_cliente_nombre_con_numeros()
        self._sim_cliente_email_sin_arroba()
        self._sim_cliente_nombre_muy_corto()

        # --- BLOQUE 2: Registro de servicios ---
        self._sim_sala_valida_con_proyector()
        self._sim_sala_valida_sin_proyector()
        self._sim_equipo_valido_con_deposito()
        self._sim_equipo_valido_sin_deposito()
        self._sim_asesoria_valida_avanzada()
        self._sim_asesoria_valida_basica()
        self._sim_servicio_tarifa_negativa()
        self._sim_servicio_nombre_vacio()
        self._sim_asesoria_nivel_invalido()
        self._sim_sala_capacidad_cero()
        self._sim_servicio_duplicado()

        # --- BLOQUE 3: Reservas válidas ---
        self._sim_reserva_sala_exitosa()
        self._sim_reserva_equipo_exitosa()
        self._sim_reserva_asesoria_exitosa()
        self._sim_reserva_confirmar()
        self._sim_reserva_completar()

        # --- BLOQUE 4: Reservas fallidas ---
        self._sim_reserva_servicio_no_disponible()
        self._sim_reserva_horas_cero()
        self._sim_reserva_horas_excesivas()
        self._sim_reserva_cliente_inactivo()
        self._sim_reserva_asesoria_bajo_minimo()
        self._sim_cancelar_reserva_valida()
        self._sim_cancelar_reserva_ya_cancelada()
        self._sim_completar_sin_confirmar()
        self._sim_buscar_reserva_inexistente()

        # --- BLOQUE 5: Cálculos de costos ---
        self._sim_calcular_costo_con_iva()
        self._sim_calcular_costo_con_descuento()
        self._sim_calcular_costo_paquete()
        self._sim_descuento_invalido()
        self._sim_calcular_costo_sala_con_proyector()
        self._sim_calcular_costo_asesoria_avanzada()
        self._sim_calcular_costo_con_deposito()

        # --- BLOQUE 6: Búsquedas y consultas ---
        self._sim_buscar_cliente_existente()
        self._sim_buscar_cliente_inexistente()
        self._sim_buscar_servicio_existente()
        self._sim_buscar_servicio_inexistente()
        self._sim_listar_clientes_activos()
        self._sim_listar_servicios_disponibles()
        self._sim_listar_reservas_por_cliente()

        # --- BLOQUE 7: Operaciones combinadas ---
        self._sim_flujo_completo_exitoso()
        self._sim_flujo_con_errores_multiples()
        self._sim_reactivar_servicio()
        self._sim_desactivar_cliente()
        self._sim_encadenamiento_excepciones()
        self._sim_multiples_reservas_mismo_cliente()
        self._sim_resumen_final()

        # Imprimir resumen
        self._imprimir_resumen()
        LogHelper.fin_sistema("Software FJ", 0)

    # =========================================================
    # UTILIDAD INTERNA: ENCABEZADO DE SIMULACIÓN
    # =========================================================

    def _encabezar(self, descripcion: str) -> None:
        """Registra el encabezado de cada simulación."""
        self._numero_simulacion += 1
        LogHelper.separador_simulacion(self._numero_simulacion, descripcion)

    # =========================================================
    # BLOQUE 1: REGISTRO DE CLIENTES (10 simulaciones)
    # =========================================================

    def _sim_cliente_valido_completo(self) -> None:
        """
        SIMULACIÓN 1: Registro exitoso de cliente con todos los datos.
        Resultado esperado: ÉXITO.
        """
        self._encabezar("Registro de cliente válido (datos completos)")
        try:
            LogHelper.inicio_operacion("Crear cliente: Carlos Andrés Pérez")
            cliente = Cliente(
                nombre="Carlos Andres Perez",
                identificacion="12345678",
                email="carlos.perez@softwarefj.com",
                telefono="3001234567"
            )
            self.gestor_clientes.registrar(cliente)
            LogHelper.resultado(f"Cliente creado: {cliente.describir()}")
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error del sistema: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 1")

    def _sim_cliente_valido_minimo(self) -> None:
        """
        SIMULACIÓN 2: Registro exitoso de cliente con datos mínimos (sin teléfono).
        Resultado esperado: ÉXITO.
        """
        self._encabezar("Registro de cliente válido (datos mínimos, sin teléfono)")
        try:
            LogHelper.inicio_operacion("Crear cliente: Ana María Torres")
            cliente = Cliente(
                nombre="Ana Maria Torres",
                identificacion="98765432",
                email="ana.torres@email.com"
            )
            self.gestor_clientes.registrar(cliente)
            LogHelper.resultado(f"Cliente creado: {cliente.describir()}")
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error del sistema: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 2")

    def _sim_cliente_nombre_vacio(self) -> None:
        """
        SIMULACIÓN 3: Intento de registro con nombre vacío.
        Resultado esperado: ERROR CONTROLADO (ClienteInvalidoException).
        """
        self._encabezar("Registro de cliente INVÁLIDO - nombre vacío")
        try:
            LogHelper.inicio_operacion("Intentar crear cliente con nombre vacío")
            cliente = Cliente(
                nombre="",
                identificacion="11111111",
                email="test@email.com"
            )
            self.gestor_clientes.registrar(cliente)
        except ClienteInvalidoException as error:
            LogHelper.advertencia(f"Error de validación capturado correctamente: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 3")

    def _sim_cliente_email_invalido(self) -> None:
        """
        SIMULACIÓN 4: Intento de registro con email sin formato válido.
        Resultado esperado: ERROR CONTROLADO (ClienteInvalidoException).
        """
        self._encabezar("Registro de cliente INVÁLIDO - email sin @")
        try:
            LogHelper.inicio_operacion("Intentar crear cliente con email inválido")
            cliente = Cliente(
                nombre="Luis Ernesto Gomez",
                identificacion="22222222",
                email="correo_sin_arroba_punto_com"
            )
            self.gestor_clientes.registrar(cliente)
        except ClienteInvalidoException as error:
            LogHelper.advertencia(f"Email inválido detectado: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 4")

    def _sim_cliente_id_corta(self) -> None:
        """
        SIMULACIÓN 5: Intento de registro con identificación muy corta.
        Resultado esperado: ERROR CONTROLADO (ClienteInvalidoException).
        """
        self._encabezar("Registro de cliente INVÁLIDO - identificación muy corta")
        try:
            LogHelper.inicio_operacion("Intentar crear cliente con ID de 3 dígitos")
            cliente = Cliente(
                nombre="Pedro Ruiz",
                identificacion="123",   # Muy corta, mínimo 5
                email="pedro@email.com"
            )
            self.gestor_clientes.registrar(cliente)
        except ClienteInvalidoException as error:
            LogHelper.advertencia(f"ID inválida detectada: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 5")

    def _sim_cliente_id_con_letras(self) -> None:
        """
        SIMULACIÓN 6: Intento de registro con identificación que contiene letras.
        Resultado esperado: ERROR CONTROLADO.
        """
        self._encabezar("Registro de cliente INVÁLIDO - ID con letras")
        try:
            LogHelper.inicio_operacion("Intentar crear cliente con ID alfanumérica")
            cliente = Cliente(
                nombre="Maria Camila Rios",
                identificacion="ABC12345",
                email="maria@email.com"
            )
            self.gestor_clientes.registrar(cliente)
        except ClienteInvalidoException as error:
            LogHelper.advertencia(f"ID con letras rechazada: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 6")

    def _sim_cliente_duplicado(self) -> None:
        """
        SIMULACIÓN 7: Intento de registrar un cliente con ID ya existente.
        Resultado esperado: ERROR CONTROLADO (ClienteDuplicadoException).
        """
        self._encabezar("Registro de cliente DUPLICADO - misma identificación")
        try:
            LogHelper.inicio_operacion("Intentar registrar cliente con ID ya registrada")
            # Carlos (ID: 12345678) ya fue registrado en simulación 1
            cliente_duplicado = Cliente(
                nombre="Carlos Copia",
                identificacion="12345678",
                email="copia@email.com"
            )
            self.gestor_clientes.registrar(cliente_duplicado)
        except ClienteDuplicadoException as error:
            LogHelper.advertencia(f"Duplicado detectado: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 7")

    def _sim_cliente_nombre_con_numeros(self) -> None:
        """
        SIMULACIÓN 8: Nombre que contiene números (no permitido).
        Resultado esperado: ERROR CONTROLADO.
        """
        self._encabezar("Registro de cliente INVÁLIDO - nombre con números")
        try:
            LogHelper.inicio_operacion("Intentar crear cliente con nombre '4lex4nder'")
            cliente = Cliente(
                nombre="4lex4nder Mart1nez",
                identificacion="33333333",
                email="alex@email.com"
            )
            self.gestor_clientes.registrar(cliente)
        except ClienteInvalidoException as error:
            LogHelper.advertencia(f"Nombre inválido rechazado: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 8")

    def _sim_cliente_email_sin_arroba(self) -> None:
        """
        SIMULACIÓN 9: Email con dominio pero sin extensión válida.
        Resultado esperado: ERROR CONTROLADO.
        """
        self._encabezar("Registro de cliente INVÁLIDO - email mal formado")
        try:
            LogHelper.inicio_operacion("Intentar crear cliente con email '@solo-dominio'")
            cliente = Cliente(
                nombre="Sofia Elena Vargas",
                identificacion="44444444",
                email="@dominio"
            )
            self.gestor_clientes.registrar(cliente)
        except ClienteInvalidoException as error:
            LogHelper.advertencia(f"Email rechazado: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 9")

    def _sim_cliente_nombre_muy_corto(self) -> None:
        """
        SIMULACIÓN 10: Nombre de un solo carácter (menor al mínimo).
        Resultado esperado: ERROR CONTROLADO.
        """
        self._encabezar("Registro de cliente INVÁLIDO - nombre de 1 carácter")
        try:
            LogHelper.inicio_operacion("Intentar crear cliente con nombre 'X'")
            cliente = Cliente(
                nombre="X",
                identificacion="55555555",
                email="x@email.com"
            )
            self.gestor_clientes.registrar(cliente)
        except ClienteInvalidoException as error:
            LogHelper.advertencia(f"Nombre muy corto rechazado: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 10")

    # =========================================================
    # BLOQUE 2: REGISTRO DE SERVICIOS (11 simulaciones)
    # =========================================================

    def _sim_sala_valida_con_proyector(self) -> None:
        """
        SIMULACIÓN 11: Crear sala de conferencias con proyector.
        Resultado esperado: ÉXITO.
        """
        self._encabezar("Registro de Sala de conferencias CON proyector")
        try:
            LogHelper.inicio_operacion("Crear sala: SALA-A1")
            sala = ReservaSala(
                codigo="SALA-A1",
                nombre="Sala de Conferencias Principal",
                tarifa_hora=80000.0,
                capacidad_maxima=20,
                tiene_proyector=True
            )
            self.gestor_servicios.registrar(sala)
            LogHelper.resultado(sala.describir())
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error al crear sala: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 11")

    def _sim_sala_valida_sin_proyector(self) -> None:
        """
        SIMULACIÓN 12: Crear sala de reuniones sin proyector.
        Resultado esperado: ÉXITO.
        """
        self._encabezar("Registro de Sala de reuniones SIN proyector")
        try:
            LogHelper.inicio_operacion("Crear sala: SALA-B2")
            sala = ReservaSala(
                codigo="SALA-B2",
                nombre="Sala de Reuniones Ejecutiva",
                tarifa_hora=50000.0,
                capacidad_maxima=10,
                tiene_proyector=False
            )
            self.gestor_servicios.registrar(sala)
            LogHelper.resultado(sala.describir())
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error al crear sala: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 12")

    def _sim_equipo_valido_con_deposito(self) -> None:
        """
        SIMULACIÓN 13: Crear equipo de alquiler que requiere depósito.
        Resultado esperado: ÉXITO.
        """
        self._encabezar("Registro de Equipo (laptop) CON depósito")
        try:
            LogHelper.inicio_operacion("Crear equipo: EQ-LAP01")
            equipo = AlquilerEquipo(
                codigo="EQ-LAP01",
                nombre="Laptop HP ProBook 450",
                tarifa_hora=25000.0,
                tipo_equipo="Laptop",
                requiere_deposito=True,
                valor_deposito=500000.0
            )
            self.gestor_servicios.registrar(equipo)
            LogHelper.resultado(equipo.describir())
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error al crear equipo: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 13")

    def _sim_equipo_valido_sin_deposito(self) -> None:
        """
        SIMULACIÓN 14: Crear equipo sin depósito.
        Resultado esperado: ÉXITO.
        """
        self._encabezar("Registro de Equipo (cámara) SIN depósito")
        try:
            LogHelper.inicio_operacion("Crear equipo: EQ-CAM01")
            equipo = AlquilerEquipo(
                codigo="EQ-CAM01",
                nombre="Camara Sony Alpha A7III",
                tarifa_hora=40000.0,
                tipo_equipo="Camara Fotografica",
                requiere_deposito=False
            )
            self.gestor_servicios.registrar(equipo)
            LogHelper.resultado(equipo.describir())
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error al crear equipo: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 14")

    def _sim_asesoria_valida_avanzada(self) -> None:
        """
        SIMULACIÓN 15: Crear asesoría de nivel avanzado.
        Resultado esperado: ÉXITO.
        """
        self._encabezar("Registro de Asesoría Especializada nivel AVANZADO")
        try:
            LogHelper.inicio_operacion("Crear asesoría: ASESORIA-TI-ADV")
            asesoria = AsesoriaEspecializada(
                codigo="ASESORIA-TI-ADV",
                nombre="Consultoria en Arquitectura de Software",
                tarifa_hora=120000.0,
                especialidad="Arquitectura de Software",
                nombre_asesor="Ing. Fernando Jimenez",
                nivel="avanzado",
                horas_minimas=2.0
            )
            self.gestor_servicios.registrar(asesoria)
            LogHelper.resultado(asesoria.describir())
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error al crear asesoría: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 15")

    def _sim_asesoria_valida_basica(self) -> None:
        """
        SIMULACIÓN 16: Crear asesoría de nivel básico.
        Resultado esperado: ÉXITO.
        """
        self._encabezar("Registro de Asesoría Especializada nivel BÁSICO")
        try:
            LogHelper.inicio_operacion("Crear asesoría: ASESORIA-PY-BAS")
            asesoria = AsesoriaEspecializada(
                codigo="ASESORIA-PY-BAS",
                nombre="Asesoria en Programacion Python",
                tarifa_hora=80000.0,
                especialidad="Programacion Python",
                nombre_asesor="Prof. Claudia Mendoza",
                nivel="basico",
                horas_minimas=1.0
            )
            self.gestor_servicios.registrar(asesoria)
            LogHelper.resultado(asesoria.describir())
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error al crear asesoría: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 16")

    def _sim_servicio_tarifa_negativa(self) -> None:
        """
        SIMULACIÓN 17: Crear servicio con tarifa negativa (inválido).
        Resultado esperado: ERROR CONTROLADO (ServicioInvalidoException).
        """
        self._encabezar("Registro de servicio INVÁLIDO - tarifa negativa")
        try:
            LogHelper.inicio_operacion("Intentar crear sala con tarifa -5000")
            sala = ReservaSala(
                codigo="SALA-ERROR",
                nombre="Sala Sin Precio",
                tarifa_hora=-5000.0,    # INVÁLIDO
                capacidad_maxima=5
            )
            self.gestor_servicios.registrar(sala)
        except ServicioInvalidoException as error:
            LogHelper.advertencia(f"Tarifa negativa rechazada: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 17")

    def _sim_servicio_nombre_vacio(self) -> None:
        """
        SIMULACIÓN 18: Crear servicio con nombre vacío.
        Resultado esperado: ERROR CONTROLADO.
        """
        self._encabezar("Registro de servicio INVÁLIDO - nombre vacío")
        try:
            LogHelper.inicio_operacion("Intentar crear equipo sin nombre")
            equipo = AlquilerEquipo(
                codigo="EQ-NULL",
                nombre="",              # INVÁLIDO
                tarifa_hora=20000.0,
                tipo_equipo="Generico"
            )
            self.gestor_servicios.registrar(equipo)
        except ServicioInvalidoException as error:
            LogHelper.advertencia(f"Nombre vacío rechazado: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 18")

    def _sim_asesoria_nivel_invalido(self) -> None:
        """
        SIMULACIÓN 19: Asesoría con nivel fuera de los permitidos.
        Resultado esperado: ERROR CONTROLADO.
        """
        self._encabezar("Registro de asesoría INVÁLIDA - nivel no reconocido")
        try:
            LogHelper.inicio_operacion("Intentar crear asesoría con nivel 'experto'")
            asesoria = AsesoriaEspecializada(
                codigo="ASESORIA-ERR",
                nombre="Asesoria Invalida",
                tarifa_hora=100000.0,
                especialidad="General",
                nombre_asesor="Asesor Anonimo",
                nivel="experto"         # INVÁLIDO: solo basico/intermedio/avanzado
            )
            self.gestor_servicios.registrar(asesoria)
        except ServicioInvalidoException as error:
            LogHelper.advertencia(f"Nivel inválido rechazado: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 19")

    def _sim_sala_capacidad_cero(self) -> None:
        """
        SIMULACIÓN 20: Sala con capacidad cero (inválida).
        Resultado esperado: ERROR CONTROLADO.
        """
        self._encabezar("Registro de sala INVÁLIDA - capacidad cero")
        try:
            LogHelper.inicio_operacion("Intentar crear sala con capacidad 0")
            sala = ReservaSala(
                codigo="SALA-CERO",
                nombre="Sala Sin Capacidad",
                tarifa_hora=30000.0,
                capacidad_maxima=0      # INVÁLIDO
            )
            self.gestor_servicios.registrar(sala)
        except ServicioInvalidoException as error:
            LogHelper.advertencia(f"Capacidad inválida rechazada: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 20")

    def _sim_servicio_duplicado(self) -> None:
        """
        SIMULACIÓN 21: Registrar un servicio con código ya existente.
        Resultado esperado: ERROR CONTROLADO.
        """
        self._encabezar("Registro de servicio DUPLICADO - código repetido")
        try:
            LogHelper.inicio_operacion("Intentar registrar otra sala con código SALA-A1")
            sala_dup = ReservaSala(
                codigo="SALA-A1",       # Ya existe desde simulación 11
                nombre="Sala Copia",
                tarifa_hora=70000.0,
                capacidad_maxima=15
            )
            self.gestor_servicios.registrar(sala_dup)
        except ServicioInvalidoException as error:
            LogHelper.advertencia(f"Código duplicado detectado: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 21")

    # =========================================================
    # BLOQUE 3: RESERVAS VÁLIDAS (5 simulaciones)
    # =========================================================

    def _sim_reserva_sala_exitosa(self) -> None:
        """
        SIMULACIÓN 22: Reserva exitosa de sala de conferencias.
        Resultado esperado: ÉXITO.
        """
        self._encabezar("Reserva de SALA exitosa (Carlos Pérez, SALA-A1, 3 horas)")
        try:
            LogHelper.inicio_operacion("Crear reserva sala Carlos → SALA-A1")
            cliente = self.gestor_clientes.buscar_por_id("12345678")
            sala = self.gestor_servicios.buscar_por_codigo("SALA-A1")

            reserva = self.gestor_reservas.crear_reserva(cliente, sala, horas=3.0)
            costo = reserva.calcular_costo_base()
            costo_iva = reserva.calcular_costo_con_iva()

            LogHelper.detalle(f"Reserva: {reserva.describir()}")
            LogHelper.detalle(f"Costo sin IVA: {Helper.formatear_pesos(costo)}")
            LogHelper.detalle(f"Costo con IVA (19%): {Helper.formatear_pesos(costo_iva)}")
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error en reserva de sala: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 22")

    def _sim_reserva_equipo_exitosa(self) -> None:
        """
        SIMULACIÓN 23: Reserva exitosa de equipo (laptop).
        Resultado esperado: ÉXITO.
        """
        self._encabezar("Reserva de EQUIPO exitosa (Ana Torres, EQ-LAP01, 4 horas)")
        try:
            LogHelper.inicio_operacion("Crear reserva equipo Ana → EQ-LAP01")
            cliente = self.gestor_clientes.buscar_por_id("98765432")
            equipo = self.gestor_servicios.buscar_por_codigo("EQ-LAP01")

            reserva = self.gestor_reservas.crear_reserva(cliente, equipo, horas=4.0)
            costo = reserva.calcular_costo_base()
            LogHelper.detalle(f"Reserva: {reserva.describir()}")
            LogHelper.detalle(f"Costo base: {Helper.formatear_pesos(costo)}")
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error en reserva de equipo: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 23")

    def _sim_reserva_asesoria_exitosa(self) -> None:
        """
        SIMULACIÓN 24: Reserva exitosa de asesoría avanzada.
        Resultado esperado: ÉXITO.
        """
        self._encabezar("Reserva de ASESORÍA exitosa (Carlos Pérez, asesoría avanzada, 2 horas)")
        try:
            LogHelper.inicio_operacion("Crear reserva asesoría Carlos → ASESORIA-TI-ADV")
            cliente = self.gestor_clientes.buscar_por_id("12345678")
            asesoria = self.gestor_servicios.buscar_por_codigo("ASESORIA-TI-ADV")

            reserva = self.gestor_reservas.crear_reserva(cliente, asesoria, horas=2.0)
            costo = reserva.calcular_costo_base()
            LogHelper.detalle(f"Reserva: {reserva.describir()}")
            LogHelper.detalle(f"Costo asesoría avanzada: {Helper.formatear_pesos(costo)}")
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error en reserva asesoría: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 24")

    def _sim_reserva_confirmar(self) -> None:
        """
        SIMULACIÓN 25: Confirmar la primera reserva creada.
        Resultado esperado: ÉXITO.
        """
        self._encabezar("Confirmar reserva de sala (primera reserva pendiente)")
        try:
            LogHelper.inicio_operacion("Confirmar primera reserva del sistema")
            reservas = self.gestor_reservas.listar_todas()
            if reservas:
                primera = reservas[0]
                LogHelper.detalle(f"Reserva antes de confirmar: Estado = {primera.estado.value}")
                self.gestor_reservas.confirmar(primera)
                LogHelper.detalle(f"Reserva después de confirmar: Estado = {primera.estado.value}")
                self._exitosas += 1
            else:
                LogHelper.advertencia("No hay reservas disponibles para confirmar.")
        except SoftwareFJException as error:
            LogHelper.error(f"Error al confirmar: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 25")

    def _sim_reserva_completar(self) -> None:
        """
        SIMULACIÓN 26: Completar la reserva confirmada.
        Resultado esperado: ÉXITO.
        """
        self._encabezar("Completar reserva ya confirmada")
        try:
            LogHelper.inicio_operacion("Completar primera reserva confirmada")
            from modelos.reserva import EstadoReserva
            confirmadas = self.gestor_reservas.listar_por_estado(EstadoReserva.CONFIRMADA)
            if confirmadas:
                reserva = confirmadas[0]
                self.gestor_reservas.completar(reserva.id_reserva)
                LogHelper.detalle(f"Estado final: {reserva.estado.value}")
                self._exitosas += 1
            else:
                LogHelper.advertencia("No hay reservas confirmadas para completar.")
        except SoftwareFJException as error:
            LogHelper.error(f"Error al completar: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 26")

    # =========================================================
    # BLOQUE 4: RESERVAS FALLIDAS (9 simulaciones)
    # =========================================================

    def _sim_reserva_servicio_no_disponible(self) -> None:
        """
        SIMULACIÓN 27: Reserva de un servicio marcado como no disponible.
        Resultado esperado: ERROR CONTROLADO (ServicioNoDisponibleException).
        """
        self._encabezar("Reserva FALLIDA - servicio marcado como no disponible")
        try:
            LogHelper.inicio_operacion("Marcar SALA-B2 como no disponible y luego intentar reservarla")
            self.gestor_servicios.marcar_no_disponible("SALA-B2")

            cliente = self.gestor_clientes.buscar_por_id("12345678")
            sala = self.gestor_servicios.buscar_por_codigo("SALA-B2")

            # Intentar reservar sala no disponible
            self.gestor_reservas.crear_reserva(cliente, sala, horas=2.0)

        except ServicioNoDisponibleException as error:
            LogHelper.advertencia(f"Servicio no disponible manejado: {error}")
            self._con_error_controlado += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error del sistema: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            # Reactivar para futuras pruebas
            try:
                self.gestor_servicios.marcar_disponible("SALA-B2")
            except Exception:
                pass
            LogHelper.fin_modulo("Simulación 27")

    def _sim_reserva_horas_cero(self) -> None:
        """
        SIMULACIÓN 28: Reserva con 0 horas de duración.
        Resultado esperado: ERROR CONTROLADO.
        """
        self._encabezar("Reserva FALLIDA - 0 horas de duración")
        try:
            LogHelper.inicio_operacion("Intentar reservar sala con 0 horas")
            cliente = self.gestor_clientes.buscar_por_id("98765432")
            sala = self.gestor_servicios.buscar_por_codigo("SALA-B2")
            self.gestor_reservas.crear_reserva(cliente, sala, horas=0)
        except ServicioInvalidoException as error:
            LogHelper.advertencia(f"Horas inválidas detectadas: {error}")
            self._con_error_controlado += 1
        except SoftwareFJException as error:
            LogHelper.advertencia(f"Error controlado: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 28")

    def _sim_reserva_horas_excesivas(self) -> None:
        """
        SIMULACIÓN 29: Reserva con 48 horas (excede el máximo de 24).
        Resultado esperado: ERROR CONTROLADO.
        """
        self._encabezar("Reserva FALLIDA - duración excesiva (48h, máximo 24h)")
        try:
            LogHelper.inicio_operacion("Intentar reservar sala por 48 horas")
            cliente = self.gestor_clientes.buscar_por_id("98765432")
            sala = self.gestor_servicios.buscar_por_codigo("SALA-B2")
            self.gestor_reservas.crear_reserva(cliente, sala, horas=48)
        except ServicioInvalidoException as error:
            LogHelper.advertencia(f"Duración excesiva rechazada: {error}")
            self._con_error_controlado += 1
        except SoftwareFJException as error:
            LogHelper.advertencia(f"Error controlado: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 29")

    def _sim_reserva_cliente_inactivo(self) -> None:
        """
        SIMULACIÓN 30: Reserva por parte de un cliente desactivado.
        Resultado esperado: ERROR CONTROLADO (ReservaInvalidaException).
        """
        self._encabezar("Reserva FALLIDA - cliente inactivo")
        try:
            LogHelper.inicio_operacion("Desactivar cliente Ana Torres e intentar reserva")
            # Desactivar temporalmente a Ana Torres
            cliente = self.gestor_clientes.buscar_por_id("98765432")
            cliente.desactivar()
            LogHelper.detalle(f"Cliente '{cliente.nombre}' desactivado temporalmente.")

            sala = self.gestor_servicios.buscar_por_codigo("SALA-B2")
            self.gestor_reservas.crear_reserva(cliente, sala, horas=2.0)

        except ReservaInvalidaException as error:
            LogHelper.advertencia(f"Reserva con cliente inactivo rechazada: {error}")
            self._con_error_controlado += 1
        except SoftwareFJException as error:
            LogHelper.advertencia(f"Error controlado: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            # Reactivar cliente para no afectar otras simulaciones
            try:
                cliente = self.gestor_clientes.buscar_por_id("98765432")
                cliente.activar()
                LogHelper.detalle(f"Cliente '{cliente.nombre}' reactivado.")
            except Exception:
                pass
            LogHelper.fin_modulo("Simulación 30")

    def _sim_reserva_asesoria_bajo_minimo(self) -> None:
        """
        SIMULACIÓN 31: Reserva de asesoría avanzada por menos del mínimo de horas (2h).
        Resultado esperado: ERROR CONTROLADO.
        """
        self._encabezar("Reserva FALLIDA - asesoría avanzada con menos del mínimo de horas")
        try:
            LogHelper.inicio_operacion("Intentar reservar asesoría avanzada por solo 0.5h (mínimo 2h)")
            cliente = self.gestor_clientes.buscar_por_id("12345678")
            asesoria = self.gestor_servicios.buscar_por_codigo("ASESORIA-TI-ADV")
            self.gestor_reservas.crear_reserva(cliente, asesoria, horas=0.5)
        except ServicioInvalidoException as error:
            LogHelper.advertencia(f"Horas bajo mínimo rechazadas: {error}")
            self._con_error_controlado += 1
        except SoftwareFJException as error:
            LogHelper.advertencia(f"Error controlado: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 31")

    def _sim_cancelar_reserva_valida(self) -> None:
        """
        SIMULACIÓN 32: Cancelar una reserva en estado PENDIENTE.
        Resultado esperado: ÉXITO.
        """
        self._encabezar("Cancelar reserva PENDIENTE (motivo: cambio de agenda)")
        try:
            LogHelper.inicio_operacion("Cancelar reserva de equipo de Ana Torres")
            pendientes = self.gestor_reservas.listar_por_estado(EstadoReserva.PENDIENTE)
            if pendientes:
                reserva = pendientes[0]
                LogHelper.detalle(f"Cancelando: {reserva.describir()}")
                self.gestor_reservas.cancelar(
                    reserva.id_reserva,
                    motivo="Cambio de agenda del cliente"
                )
                LogHelper.detalle(f"Estado tras cancelar: {reserva.estado.value}")
                LogHelper.detalle(f"Motivo: {reserva.motivo_cancelacion}")
                self._exitosas += 1
            else:
                LogHelper.advertencia("No hay reservas pendientes para cancelar.")
        except SoftwareFJException as error:
            LogHelper.error(f"Error al cancelar: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 32")

    def _sim_cancelar_reserva_ya_cancelada(self) -> None:
        """
        SIMULACIÓN 33: Intentar cancelar una reserva que ya está cancelada.
        Resultado esperado: ERROR CONTROLADO (ReservaInvalidaException).
        """
        self._encabezar("Cancelar reserva YA CANCELADA (operación no permitida)")
        try:
            LogHelper.inicio_operacion("Intentar cancelar dos veces la misma reserva")
            canceladas = self.gestor_reservas.listar_por_estado(EstadoReserva.CANCELADA)
            if canceladas:
                reserva = canceladas[0]
                LogHelper.detalle(f"Intentando cancelar reserva #{reserva.id_reserva} (ya cancelada)")
                self.gestor_reservas.cancelar(reserva.id_reserva, "Segunda cancelación")
            else:
                LogHelper.advertencia("No hay reservas canceladas para esta prueba.")
        except ReservaInvalidaException as error:
            LogHelper.advertencia(f"Doble cancelación rechazada: {error}")
            self._con_error_controlado += 1
        except SoftwareFJException as error:
            LogHelper.advertencia(f"Error controlado: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 33")

    def _sim_completar_sin_confirmar(self) -> None:
        """
        SIMULACIÓN 34: Intentar completar una reserva que está PENDIENTE (sin confirmar).
        Resultado esperado: ERROR CONTROLADO.
        """
        self._encabezar("Completar reserva PENDIENTE sin confirmar (no permitido)")
        try:
            LogHelper.inicio_operacion("Intentar completar una reserva en estado PENDIENTE")
            pendientes = self.gestor_reservas.listar_por_estado(EstadoReserva.PENDIENTE)
            if pendientes:
                reserva = pendientes[0]
                LogHelper.detalle(f"Estado actual: {reserva.estado.value}")
                self.gestor_reservas.completar(reserva.id_reserva)
            else:
                LogHelper.advertencia("No hay reservas pendientes para esta prueba.")
        except ReservaInvalidaException as error:
            LogHelper.advertencia(f"Completar sin confirmar rechazado: {error}")
            self._con_error_controlado += 1
        except SoftwareFJException as error:
            LogHelper.advertencia(f"Error controlado: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 34")

    def _sim_buscar_reserva_inexistente(self) -> None:
        """
        SIMULACIÓN 35: Buscar una reserva con ID que no existe.
        Resultado esperado: ERROR CONTROLADO (ReservaNoEncontradaException).
        """
        self._encabezar("Buscar reserva INEXISTENTE - ID 'ZZZZZZZZ'")
        try:
            LogHelper.inicio_operacion("Buscar reserva con ID inválido: ZZZZZZZZ")
            self.gestor_reservas.buscar_por_id("ZZZZZZZZ")
        except ReservaNoEncontradaException as error:
            LogHelper.advertencia(f"Reserva no encontrada manejada: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 35")

    # =========================================================
    # BLOQUE 5: CÁLCULOS DE COSTOS (7 simulaciones)
    # =========================================================

    def _sim_calcular_costo_con_iva(self) -> None:
        """
        SIMULACIÓN 36: Calcular costo de sala con IVA del 19%.
        Resultado esperado: ÉXITO.
        """
        self._encabezar("Cálculo de costo de sala CON IVA 19%")
        try:
            LogHelper.inicio_operacion("Calcular costo SALA-A1 por 3 horas con IVA")
            sala = self.gestor_servicios.buscar_por_codigo("SALA-A1")
            horas = 3.0
            costo_base = sala.calcular_costo(horas)
            costo_iva = sala.calcular_costo_con_impuestos(horas)
            LogHelper.detalle(f"Sala: {sala.nombre} | Horas: {horas}")
            LogHelper.detalle(f"Costo base: {Helper.formatear_pesos(costo_base)}")
            LogHelper.detalle(f"Con IVA 19%: {Helper.formatear_pesos(costo_iva)}")
            LogHelper.detalle(f"(Nota: Sala tiene proyector → recargo 10% incluido en base)")
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error en cálculo: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 36")

    def _sim_calcular_costo_con_descuento(self) -> None:
        """
        SIMULACIÓN 37: Calcular costo de equipo con descuento del 15%.
        Resultado esperado: ÉXITO.
        """
        self._encabezar("Cálculo de costo de equipo CON descuento 15%")
        try:
            LogHelper.inicio_operacion("Calcular costo EQ-LAP01 por 4 horas con 15% descuento")
            equipo = self.gestor_servicios.buscar_por_codigo("EQ-LAP01")
            horas = 4.0
            descuento = 0.15
            costo_base = equipo.calcular_costo(horas)
            costo_descuento = equipo.calcular_costo_con_descuento(horas, descuento)
            ahorro = costo_base - costo_descuento
            LogHelper.detalle(f"Equipo: {equipo.nombre} | Horas: {horas}")
            LogHelper.detalle(f"Costo base: {Helper.formatear_pesos(costo_base)}")
            LogHelper.detalle(f"Con 15% descuento: {Helper.formatear_pesos(costo_descuento)}")
            LogHelper.detalle(f"Ahorro: {Helper.formatear_pesos(ahorro)}")
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error en cálculo: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 37")

    def _sim_calcular_costo_paquete(self) -> None:
        """
        SIMULACIÓN 38: Calcular paquete corporativo (descuento + IVA) para asesoría.
        Resultado esperado: ÉXITO. Usa método sobrecargado calcular_costo_paquete().
        """
        self._encabezar("Cálculo PAQUETE corporativo asesoría (descuento 20% + IVA 19%)")
        try:
            LogHelper.inicio_operacion("Calcular paquete asesoría avanzada 5 horas")
            asesoria = self.gestor_servicios.buscar_por_codigo("ASESORIA-TI-ADV")
            horas = 5.0
            descuento = 0.20
            costo_sin_nada = asesoria.calcular_costo(horas)
            costo_paquete = asesoria.calcular_costo_paquete(
                horas,
                porcentaje_descuento=descuento
            )
            LogHelper.detalle(f"Asesoría: {asesoria.nombre} | Horas: {horas}")
            LogHelper.detalle(f"Costo sin ajustes: {Helper.formatear_pesos(costo_sin_nada)}")
            LogHelper.detalle(f"Paquete (20% desc + 19% IVA): {Helper.formatear_pesos(costo_paquete)}")
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error en cálculo paquete: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 38")

    def _sim_descuento_invalido(self) -> None:
        """
        SIMULACIÓN 39: Calcular descuento con porcentaje mayor al 100% (inválido).
        Resultado esperado: ERROR CONTROLADO.
        """
        self._encabezar("Cálculo con descuento INVÁLIDO (150% > 100%)")
        try:
            LogHelper.inicio_operacion("Intentar calcular con descuento del 150%")
            equipo = self.gestor_servicios.buscar_por_codigo("EQ-CAM01")
            # Descuento de 1.5 = 150% (inválido, máximo 1.0)
            costo = equipo.calcular_costo_con_descuento(2.0, porcentaje_descuento=1.5)
            LogHelper.info(f"Resultado: {costo}")
        except ValueError as error:
            LogHelper.advertencia(f"Descuento inválido rechazado: {error}")
            self._con_error_controlado += 1
        except SoftwareFJException as error:
            LogHelper.advertencia(f"Error controlado: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 39")

    def _sim_calcular_costo_sala_con_proyector(self) -> None:
        """
        SIMULACIÓN 40: Comparar costos sala con y sin proyector.
        Resultado esperado: ÉXITO. Demuestra polimorfismo.
        """
        self._encabezar("Comparar costos: Sala CON proyector vs SIN proyector")
        try:
            LogHelper.inicio_operacion("Comparar tarifas de SALA-A1 vs SALA-B2")
            sala_con = self.gestor_servicios.buscar_por_codigo("SALA-A1")
            sala_sin = self.gestor_servicios.buscar_por_codigo("SALA-B2")
            horas = 4.0

            costo_con = sala_con.calcular_costo(horas)
            costo_sin = sala_sin.calcular_costo(horas)
            diferencia = costo_con - costo_sin

            LogHelper.detalle(f"{sala_con.nombre} ({horas}h): {Helper.formatear_pesos(costo_con)}")
            LogHelper.detalle(f"{sala_sin.nombre} ({horas}h): {Helper.formatear_pesos(costo_sin)}")
            LogHelper.detalle(f"Diferencia por proyector: {Helper.formatear_pesos(diferencia)}")
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error en comparación: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 40")

    def _sim_calcular_costo_asesoria_avanzada(self) -> None:
        """
        SIMULACIÓN 41: Demostrar diferencia de costo por nivel de asesoría.
        Resultado esperado: ÉXITO. Demuestra polimorfismo.
        """
        self._encabezar("Comparar costos: Asesoría AVANZADA vs BÁSICA (mismo tiempo)")
        try:
            LogHelper.inicio_operacion("Comparar tarifas asesoría avanzada vs básica")
            avanzada = self.gestor_servicios.buscar_por_codigo("ASESORIA-TI-ADV")
            basica = self.gestor_servicios.buscar_por_codigo("ASESORIA-PY-BAS")
            horas = 3.0

            costo_avanzada = avanzada.calcular_costo(horas)
            costo_basica = basica.calcular_costo(horas)

            LogHelper.detalle(f"Asesoría avanzada ({horas}h): {Helper.formatear_pesos(costo_avanzada)}")
            LogHelper.detalle(f"Asesoría básica ({horas}h): {Helper.formatear_pesos(costo_basica)}")
            LogHelper.detalle(f"La asesoría avanzada cuesta {avanzada.FACTORES_NIVEL['avanzado']}x más")
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error en comparación: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 41")

    def _sim_calcular_costo_con_deposito(self) -> None:
        """
        SIMULACIÓN 42: Calcular desembolso total de equipo incluyendo depósito.
        Resultado esperado: ÉXITO.
        """
        self._encabezar("Cálculo de costo total de equipo CON depósito inicial")
        try:
            LogHelper.inicio_operacion("Calcular desembolso total EQ-LAP01")
            equipo = self.gestor_servicios.buscar_por_codigo("EQ-LAP01")
            horas = 6.0
            costo_alquiler = equipo.calcular_costo(horas)
            total_con_deposito = equipo.calcular_costo_total_con_deposito(horas)
            LogHelper.detalle(f"Equipo: {equipo.nombre}")
            LogHelper.detalle(f"Alquiler {horas}h: {Helper.formatear_pesos(costo_alquiler)}")
            LogHelper.detalle(f"Depósito: {Helper.formatear_pesos(equipo.valor_deposito)}")
            LogHelper.detalle(f"Total desembolso inicial: {Helper.formatear_pesos(total_con_deposito)}")
            LogHelper.detalle("(El depósito se devuelve al entregar el equipo)")
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error en cálculo con depósito: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 42")

    # =========================================================
    # BLOQUE 6: BÚSQUEDAS Y CONSULTAS (6 simulaciones)
    # =========================================================

    def _sim_buscar_cliente_existente(self) -> None:
        """SIMULACIÓN 43: Buscar cliente que existe."""
        self._encabezar("Buscar cliente EXISTENTE por ID")
        try:
            LogHelper.inicio_operacion("Buscar cliente con ID: 12345678")
            cliente = self.gestor_clientes.buscar_por_id("12345678")
            LogHelper.resultado(f"Encontrado: {cliente.describir()}")
            self._exitosas += 1
        except ClienteNoEncontradoException as error:
            LogHelper.error(f"Error: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 43")

    def _sim_buscar_cliente_inexistente(self) -> None:
        """SIMULACIÓN 44: Buscar cliente que no existe."""
        self._encabezar("Buscar cliente INEXISTENTE - ID '00000000'")
        try:
            LogHelper.inicio_operacion("Buscar cliente con ID: 00000000")
            self.gestor_clientes.buscar_por_id("00000000")
        except ClienteNoEncontradoException as error:
            LogHelper.advertencia(f"Cliente no encontrado manejado: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 44")

    def _sim_buscar_servicio_existente(self) -> None:
        """SIMULACIÓN 45: Buscar servicio que existe."""
        self._encabezar("Buscar servicio EXISTENTE por código")
        try:
            LogHelper.inicio_operacion("Buscar servicio con código: EQ-CAM01")
            servicio = self.gestor_servicios.buscar_por_codigo("EQ-CAM01")
            LogHelper.resultado(f"Encontrado: {servicio.describir()}")
            self._exitosas += 1
        except ServicioNoEncontradoException as error:
            LogHelper.error(f"Error: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 45")

    def _sim_buscar_servicio_inexistente(self) -> None:
        """SIMULACIÓN 46: Buscar servicio que no existe."""
        self._encabezar("Buscar servicio INEXISTENTE - código 'SRV-9999'")
        try:
            LogHelper.inicio_operacion("Buscar servicio con código: SRV-9999")
            self.gestor_servicios.buscar_por_codigo("SRV-9999")
        except ServicioNoEncontradoException as error:
            LogHelper.advertencia(f"Servicio no encontrado manejado: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 46")

    def _sim_listar_clientes_activos(self) -> None:
        """SIMULACIÓN 47: Listar todos los clientes activos."""
        self._encabezar("Listar todos los clientes activos del sistema")
        try:
            LogHelper.inicio_operacion("Obtener lista de clientes activos")
            activos = self.gestor_clientes.listar_activos()
            LogHelper.resultado(f"Total clientes activos: {len(activos)}")
            for cliente in activos:
                LogHelper.detalle(f"  → {cliente.describir()}")
            self._exitosas += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 47")

    def _sim_listar_servicios_disponibles(self) -> None:
        """SIMULACIÓN 48: Listar todos los servicios disponibles."""
        self._encabezar("Listar todos los servicios disponibles del catálogo")
        try:
            LogHelper.inicio_operacion("Obtener lista de servicios disponibles")
            disponibles = self.gestor_servicios.listar_disponibles()
            LogHelper.resultado(f"Total servicios disponibles: {len(disponibles)}")
            for servicio in disponibles:
                LogHelper.detalle(f"  → {servicio.describir()}")
            self._exitosas += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 48")

    def _sim_listar_reservas_por_cliente(self) -> None:
        """SIMULACIÓN 49: Listar todas las reservas de un cliente específico."""
        self._encabezar("Listar reservas del cliente Carlos Pérez (ID: 12345678)")
        try:
            LogHelper.inicio_operacion("Obtener reservas de cliente 12345678")
            reservas = self.gestor_reservas.listar_por_cliente("12345678")
            LogHelper.resultado(f"Total reservas del cliente: {len(reservas)}")
            for reserva in reservas:
                LogHelper.detalle(f"  → {reserva.describir()}")
            self._exitosas += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 49")

    # =========================================================
    # BLOQUE 7: OPERACIONES COMBINADAS (6 simulaciones)
    # =========================================================

    def _sim_flujo_completo_exitoso(self) -> None:
        """
        SIMULACIÓN 50: Flujo completo exitoso: crear cliente → servicio → reservar →
        confirmar → completar.
        Resultado esperado: ÉXITO total.
        """
        self._encabezar("FLUJO COMPLETO exitoso: cliente nuevo → reserva → completar")
        try:
            LogHelper.inicio_operacion("START: Flujo completo exitoso")

            # Crear cliente nuevo
            LogHelper.inicio_operacion("Crear cliente nuevo: Valentina Castro")
            cliente = Cliente(
                nombre="Valentina Castro",
                identificacion="77777777",
                email="valentina.castro@empresa.co",
                telefono="3109876543"
            )
            self.gestor_clientes.registrar(cliente)
            LogHelper.fin_operacion("Crear cliente nuevo", f"ID: {cliente.identificacion}")

            # Obtener sala disponible
            LogHelper.inicio_operacion("Obtener sala disponible")
            sala = self.gestor_servicios.buscar_por_codigo("SALA-B2")
            LogHelper.fin_operacion("Obtener sala disponible", sala.nombre)

            # Crear reserva
            LogHelper.inicio_operacion("Crear reserva Valentina → SALA-B2")
            reserva = self.gestor_reservas.crear_reserva(cliente, sala, horas=1.5)
            LogHelper.fin_operacion("Crear reserva", f"ID: {reserva.id_reserva}")

            # Confirmar
            LogHelper.inicio_operacion(f"Confirmar reserva #{reserva.id_reserva}")
            self.gestor_reservas.confirmar(reserva)
            LogHelper.fin_operacion("Confirmar reserva", "CONFIRMADA")

            # Completar
            LogHelper.inicio_operacion(f"Completar reserva #{reserva.id_reserva}")
            self.gestor_reservas.completar(reserva.id_reserva)
            LogHelper.fin_operacion("Completar reserva", "COMPLETADA")

            # Resumen de costos
            costo_base = reserva.calcular_costo_base()
            costo_iva = reserva.calcular_costo_con_iva()
            costo_desc = reserva.calcular_costo_con_descuento(0.10)

            LogHelper.resultado(f"Costo base: {Helper.formatear_pesos(costo_base)}")
            LogHelper.resultado(f"Con IVA 19%: {Helper.formatear_pesos(costo_iva)}")
            LogHelper.resultado(f"Con 10% desc: {Helper.formatear_pesos(costo_desc)}")
            LogHelper.fin_operacion("FINISH: Flujo completo exitoso")
            self._exitosas += 1

        except SoftwareFJException as error:
            LogHelper.error(f"Error en flujo completo: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 50")

    def _sim_flujo_con_errores_multiples(self) -> None:
        """
        SIMULACIÓN 51: Flujo con múltiples errores seguidos. El sistema no se detiene.
        Demuestra encadenamiento de try/except/else/finally.
        """
        self._encabezar("FLUJO con múltiples errores seguidos (sistema no cae)")
        LogHelper.inicio_operacion("START: Flujo con errores múltiples")

        errores_acumulados = []

        # Error 1: cliente inválido
        try:
            LogHelper.inicio_operacion("Intento 1: Crear cliente con email inválido")
            Cliente(nombre="Test Error", identificacion="66666666", email="INVALIDO")
        except ClienteInvalidoException as e:
            LogHelper.advertencia(f"Error 1 capturado: {e}")
            errores_acumulados.append("Email inválido")
        else:
            LogHelper.info("Intento 1: Sin error.")
        finally:
            LogHelper.fin_operacion("Intento 1")

        # Error 2: servicio con tarifa inválida
        try:
            LogHelper.inicio_operacion("Intento 2: Crear sala con tarifa 0")
            ReservaSala(
                codigo="ERR-SLT",
                nombre="Sala Tarifa Cero",
                tarifa_hora=0,          # inválido
                capacidad_maxima=5
            )
        except ServicioInvalidoException as e:
            LogHelper.advertencia(f"Error 2 capturado: {e}")
            errores_acumulados.append("Tarifa cero")
        else:
            LogHelper.info("Intento 2: Sin error.")
        finally:
            LogHelper.fin_operacion("Intento 2")

        # Error 3: buscar cliente inexistente
        try:
            LogHelper.inicio_operacion("Intento 3: Buscar cliente ID 99999999")
            self.gestor_clientes.buscar_por_id("99999999")
        except ClienteNoEncontradoException as e:
            LogHelper.advertencia(f"Error 3 capturado: {e}")
            errores_acumulados.append("Cliente no encontrado")
        else:
            LogHelper.info("Intento 3: Sin error.")
        finally:
            LogHelper.fin_operacion("Intento 3")

        LogHelper.resultado(
            f"FINISH: Flujo con errores: {len(errores_acumulados)} errores manejados. "
            f"Sistema OPERATIVO."
        )
        self._con_error_controlado += len(errores_acumulados)
        LogHelper.fin_modulo("Simulación 51")

    def _sim_reactivar_servicio(self) -> None:
        """SIMULACIÓN 52: Desactivar y reactivar un servicio."""
        self._encabezar("Desactivar y reactivar servicio EQ-CAM01")
        try:
            LogHelper.inicio_operacion("Desactivar EQ-CAM01")
            self.gestor_servicios.marcar_no_disponible("EQ-CAM01")
            camara = self.gestor_servicios.buscar_por_codigo("EQ-CAM01")
            LogHelper.detalle(f"Estado: {camara.describir()}")

            LogHelper.inicio_operacion("Reactivar EQ-CAM01")
            self.gestor_servicios.marcar_disponible("EQ-CAM01")
            LogHelper.detalle(f"Estado: {camara.describir()}")
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 52")

    def _sim_desactivar_cliente(self) -> None:
        """SIMULACIÓN 53: Desactivar un cliente."""
        self._encabezar("Desactivar cliente (baja lógica)")
        try:
            LogHelper.inicio_operacion("Desactivar cliente Ana Torres (98765432)")
            self.gestor_clientes.desactivar("98765432")
            cliente = self.gestor_clientes.buscar_por_id("98765432")
            LogHelper.detalle(f"Estado: {cliente.describir()}")
            # Reactivar para no afectar estado final
            cliente.activar()
            LogHelper.detalle(f"Reactivado: {cliente.describir()}")
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 53")

    def _sim_encadenamiento_excepciones(self) -> None:
        """
        SIMULACIÓN 54: Demuestra encadenamiento de excepciones (raise X from Y).
        Resultado esperado: ERROR CONTROLADO con causa raíz visible.
        """
        self._encabezar("ENCADENAMIENTO de excepciones (raise X from Y)")
        try:
            LogHelper.inicio_operacion("Demostrar encadenamiento de excepciones")

            try:
                # Error original (ValueError del Helper)
                Helper.validar_horas(-5, "Prueba encadenamiento")
            except ValueError as error_original:
                # Encadenar: lanzar excepción de dominio desde la causa raíz
                raise ServicioInvalidoException(
                    f"Las horas proporcionadas no son válidas para el servicio.",
                    campo="horas"
                ) from error_original

        except ServicioInvalidoException as error_encadenado:
            LogHelper.advertencia(f"Excepción encadenada capturada: {error_encadenado}")
            if error_encadenado.__cause__:
                LogHelper.advertencia(f"Causa raíz: {error_encadenado.__cause__}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 54")

    def _sim_multiples_reservas_mismo_cliente(self) -> None:
        """
        SIMULACIÓN 55: Un cliente hace múltiples reservas de diferentes servicios.
        Resultado esperado: ÉXITO.
        """
        self._encabezar("Cliente Carlos Pérez crea múltiples reservas")
        try:
            LogHelper.inicio_operacion("Crear 3 reservas para el mismo cliente")
            cliente = self.gestor_clientes.buscar_por_id("12345678")

            servicios = ["SALA-B2", "EQ-CAM01", "ASESORIA-PY-BAS"]
            horas_lista = [1.0, 2.0, 1.5]
            reservas_creadas = []

            for codigo, horas in zip(servicios, horas_lista):
                try:
                    servicio = self.gestor_servicios.buscar_por_codigo(codigo)
                    reserva = self.gestor_reservas.crear_reserva(cliente, servicio, horas)
                    reservas_creadas.append(reserva)
                    LogHelper.detalle(
                        f"Reserva creada: #{reserva.id_reserva} | "
                        f"{servicio.nombre} | {horas}h | "
                        f"{Helper.formatear_pesos(reserva.calcular_costo_base())}"
                    )
                except SoftwareFJException as e:
                    LogHelper.advertencia(f"Error en reserva {codigo}: {e}")

            total = sum(r.calcular_costo_base() for r in reservas_creadas)
            LogHelper.resultado(
                f"Total reservas creadas: {len(reservas_creadas)} | "
                f"Costo total: {Helper.formatear_pesos(total)}"
            )
            self._exitosas += 1
        except SoftwareFJException as error:
            LogHelper.error(f"Error en múltiples reservas: {error}")
            self._con_error_controlado += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 55")

    def _sim_resumen_final(self) -> None:
        """SIMULACIÓN 56: Imprimir resumen estadístico del sistema."""
        self._encabezar("RESUMEN ESTADÍSTICO del sistema Software FJ")
        try:
            LogHelper.inicio_operacion("Generar resumen del sistema")

            total_clientes = self.gestor_clientes.total_clientes()
            activos = len(self.gestor_clientes.listar_activos())
            total_servicios = self.gestor_servicios.total_servicios()
            disponibles = len(self.gestor_servicios.listar_disponibles())
            total_reservas = self.gestor_reservas.total_reservas()

            pendientes = len(self.gestor_reservas.listar_por_estado(EstadoReserva.PENDIENTE))
            confirmadas = len(self.gestor_reservas.listar_por_estado(EstadoReserva.CONFIRMADA))
            completadas = len(self.gestor_reservas.listar_por_estado(EstadoReserva.COMPLETADA))
            canceladas = len(self.gestor_reservas.listar_por_estado(EstadoReserva.CANCELADA))

            LogHelper.resultado(f"=== ESTADO DEL SISTEMA ===")
            LogHelper.resultado(f"Clientes totales: {total_clientes} | Activos: {activos}")
            LogHelper.resultado(f"Servicios totales: {total_servicios} | Disponibles: {disponibles}")
            LogHelper.resultado(f"Reservas totales: {total_reservas}")
            LogHelper.resultado(
                f"  Pendientes: {pendientes} | Confirmadas: {confirmadas} | "
                f"Completadas: {completadas} | Canceladas: {canceladas}"
            )
            self._exitosas += 1
        except Exception as error:
            LogHelper.error(f"Error inesperado: {error}")
        finally:
            LogHelper.fin_modulo("Simulación 56")

    # =========================================================
    # RESUMEN FINAL DE SIMULACIONES
    # =========================================================

    def _imprimir_resumen(self) -> None:
        """Imprime el resumen de resultados de todas las simulaciones."""
        LogHelper.log("=" * 60)
        LogHelper.log("RESUMEN DE SIMULACIONES")
        LogHelper.log("=" * 60)
        LogHelper.resultado(f"Total simulaciones ejecutadas : {self._numero_simulacion}")
        LogHelper.resultado(f"Operaciones exitosas          : {self._exitosas}")
        LogHelper.resultado(f"Errores controlados manejados : {self._con_error_controlado}")
        LogHelper.resultado(f"Sistema: ESTABLE y OPERATIVO en todo momento.")
        LogHelper.log("=" * 60)
