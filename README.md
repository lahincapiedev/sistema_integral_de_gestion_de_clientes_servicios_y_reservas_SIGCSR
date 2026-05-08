# 🏢 Software FJ — Sistema Integral de Gestión de Clientes, Servicios y Reservas

> **Curso:** Programación 213023_344 · UNAD
> **Fase:** 4 — Prácticas Simuladas
> **Lenguaje:** Python 3.13
> **Paradigma:** Programación Orientada a Objetos (POO) + Manejo Avanzado de Excepciones

---

## 📋 Objetivo del proyecto

Construir una aplicación de consola **estable, modular y extensible** que gestione clientes, servicios y reservas para la empresa **Software FJ**, implementando de forma rigurosa:

- Abstracción, Herencia, Polimorfismo, Encapsulación
- Manejo avanzado de excepciones (`try/except`, `try/except/else`, `try/finally`, encadenamiento)
- Registro de eventos y errores en archivo de logs
- Más de 56 simulaciones de operaciones válidas e inválidas, sin base de datos

---

## 🗂️ Estructura del proyecto

```
software_fj/
│
├── main.py                          ← Punto de entrada principal (módulos ejecutables)
│
├── excepciones/
│   └── excepciones_personalizadas.py ← Jerarquía completa de excepciones del dominio
│
├── helpers/
│   ├── log_helper.py                 ← Registro de eventos con formato profesional
│   └── helper.py                     ← Validaciones, conversiones y utilidades
│
├── modelos/
│   ├── entidad_base.py               ← Clase abstracta base (todas las entidades)
│   ├── cliente.py                    ← Clase Cliente con encapsulación robusta
│   ├── servicios.py                  ← ReservaSala, AlquilerEquipo, AsesoriaEspecializada
│   └── reserva.py                    ← Ciclo de vida de reservas + EstadoReserva
│
├── gestores/
│   ├── gestor_clientes.py            ← CRUD de clientes en memoria
│   ├── gestor_servicios.py           ← Catálogo de servicios en memoria
│   └── gestor_reservas.py            ← Administración de reservas en memoria
│
├── simulaciones/
│   └── simulador_sistema.py          ← 56 simulaciones organizadas por bloques
│
└── logs/
    └── YYYY-MM-DD.log                ← Archivo de log generado automáticamente por día
```

---

## ⚙️ Requisitos

- **Python 3.10 o superior** (probado con Python 3.13)
- No requiere librerías externas
- No utiliza base de datos

---

## 🚀 Cómo ejecutar

```bash
# Clonar el repositorio
git clone https://github.com/lahincapiedev/sistema_integral_de_gestion_de_clientes_servicios_y_reservas_SIGCSR
cd sistema_integral_de_gestion_de_clientes_servicios_y_reservas_SIGCSR

# Ejecutar todas las simulaciones
python main.py

# Ejecutar solo un módulo específico
python main.py clientes      # Solo registro de clientes
python main.py servicios     # Solo catálogo de servicios
python main.py reservas      # Solo reservas
python main.py completo      # Flujo completo en un módulo
python main.py todos         # Todas las simulaciones (igual que sin argumentos)
```

---

## 🔑 Conceptos OOP implementados

| Concepto | Dónde se aplica |
|---|---|
| **Clase abstracta** | `EntidadBase`, `Servicio` |
| **Herencia** | `Cliente`, `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` heredan de sus bases |
| **Polimorfismo** | `calcular_costo()`, `describir()`, `validar_parametros()` sobrescritos en cada servicio |
| **Encapsulación** | Atributos privados con `@property` y setters con validación en `Cliente`, `Servicio`, `Reserva` |
| **Métodos sobrecargados** | `calcular_costo_con_impuestos()`, `calcular_costo_con_descuento()`, `calcular_costo_paquete()` |

---

## 🛡️ Manejo de excepciones

### Jerarquía de excepciones personalizadas

```
Exception
└── SoftwareFJException          ← Base del sistema
    ├── ClienteException
    │   ├── ClienteInvalidoException
    │   ├── ClienteDuplicadoException
    │   └── ClienteNoEncontradoException
    ├── ServicioException
    │   ├── ServicioInvalidoException
    │   ├── ServicioNoDisponibleException
    │   └── ServicioNoEncontradoException
    ├── ReservaException
    │   ├── ReservaInvalidaException
    │   ├── ReservaNoEncontradaException
    │   └── ReservaDuplicadaException
    └── CalculoException
        └── DescuentoInvalidoException
```

### Estructuras utilizadas

- `try / except` — captura de errores específicos
- `try / except / else` — lógica cuando no hay error
- `try / except / finally` — limpieza garantizada
- `raise X from Y` — encadenamiento de excepciones con causa raíz

---

## 📊 Simulaciones incluidas (56 en total)

| Bloque | Simulaciones | Descripción |
|---|---|---|
| 1 | 1–10 | Registro de clientes (válidos e inválidos) |
| 2 | 11–21 | Registro de servicios (válidos e inválidos) |
| 3 | 22–26 | Reservas exitosas (sala, equipo, asesoría) |
| 4 | 27–35 | Reservas fallidas y cancelaciones |
| 5 | 36–42 | Cálculos de costos (IVA, descuentos, paquetes) |
| 6 | 43–49 | Búsquedas y consultas |
| 7 | 50–56 | Flujos combinados y encadenamiento |

---

## 📄 Formato del archivo de log

Cada línea del log sigue el formato:

```
DD/MM/YYYY HH:MM:SS AM/PM    [NIVEL]    mensaje
```

Ejemplo de log real generado:
```
03/05/2026 03:26:31 AM  [INFO]     ------- INICIO DEL SISTEMA: Software FJ -------
03/05/2026 03:26:31 AM  [INFO]     START: Operación --- Registrar cliente: Carlos Andres Perez
03/05/2026 03:26:31 AM  [INFO]     FINISH: Operación --- Registrar cliente: Cliente registrado exitosamente.
03/05/2026 03:26:31 AM  [WARNING]  Email inválido detectado: [ERR_CLIENTE_INVALIDO] ...
03/05/2026 03:26:31 AM  [INFO]     Results: Total simulaciones ejecutadas : 56
```

Los archivos se guardan en la carpeta `logs/` con nombre `YYYY-MM-DD.log`.

---

## 🌿 Ramas del repositorio

| Rama | Propósito | Se desprende de |
|---|---|---|
| `main` | Versión estable y final del proyecto | — |
| `develop` | Integración de todas las features antes de pasar a `main` | `main` |
| `feature/excepciones` | Implementación de `excepciones_personalizadas.py` | `develop` |
| `feature/helpers` | Implementación de `log_helper.py` y `helper.py` | `develop` |
| `feature/modelos` | Implementación de `entidad_base.py`, `cliente.py`, `servicios.py`, `reserva.py` | `develop` |
| `feature/gestores` | Implementación de `gestor_clientes.py`, `gestor_servicios.py`, `gestor_reservas.py` | `develop` |
| `feature/simulaciones` | Implementación de `simulador_sistema.py` con las 56 simulaciones | `develop` |
| `feature/main` | Implementación del `main.py` con ejecución por módulos | `develop` |

### Flujo de trabajo con Git

```
main
 └── develop
      ├── feature/excepciones   → merge a develop → merge a main
      ├── feature/helpers       → merge a develop → merge a main
      ├── feature/modelos       → merge a develop → merge a main
      ├── feature/gestores      → merge a develop → merge a main
      ├── feature/simulaciones  → merge a develop → merge a main
      └── feature/main          → merge a develop → merge a main
```

---

## 📚 Referencias bibliográficas

- Van Rossum, G., & Drake Jr, F. L. (2024). *El tutorial de Python*. Python Software Foundation. https://docs.python.org/es/3.12/tutorial/errors.html
- Cuevas Álvarez, A. (2016). *Python 3: curso práctico*. RA-MA Editorial. (pp. 373–385)
- Romano, F., Baka, B., & Phillips, D. (2019). *Getting Started with Python*. Packt Publishing.
- Zambrano, J. P. (2025). *Introducción al uso de GitHub*. Repositorio UNAD. https://repository.unad.edu.co/handle/10596/75876
