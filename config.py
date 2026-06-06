"""
config.py
─────────
Configuración central del simulador: rutas de archivos, paleta de colores
ANSI y datos semilla que se cargan la primera vez que el sistema arranca.

Todos los demás módulos importan de aquí; ninguno define constantes propias.
"""

import os

# ─── Rutas de la base de datos local ─────────────────────────────────────────

DIRECTORIO_RAIZ = os.path.dirname(os.path.abspath(__file__))
DIRECTORIO_DB   = os.path.join(DIRECTORIO_RAIZ, "db")

ARCHIVO_USUARIOS    = os.path.join(DIRECTORIO_DB, "usuarios.json")
ARCHIVO_SOLICITUDES = os.path.join(DIRECTORIO_DB, "solicitudes.json")
ARCHIVO_SESIONES    = os.path.join(DIRECTORIO_DB, "sesiones.json")

# ─── Paleta de colores ANSI ───────────────────────────────────────────────────

RESET    = "\033[0m"
NEGRITA  = "\033[1m"
VERDE    = "\033[92m"
CIAN     = "\033[96m"
AMARILLO = "\033[93m"
ROJO     = "\033[91m"
GRIS     = "\033[90m"
BLANCO   = "\033[97m"

FONDO_BOT      = "\033[48;5;236m"   # gris oscuro  → burbuja del bot
FONDO_USUARIO  = "\033[48;5;28m"    # verde oscuro  → burbuja del usuario
FONDO_CABECERA = "\033[48;5;22m"    # verde muy oscuro → barra de título

# ─── Íconos de estado de solicitud ───────────────────────────────────────────

ICONO_POR_ESTADO = {
    "APROBADA":  "✅",
    "RECHAZADA": "❌",
    "PENDIENTE": "⏳",
}

# ─── Datos semilla ────────────────────────────────────────────────────────────
# Se usan SOLO si los archivos JSON aún no existen (primer arranque).

USUARIOS_INICIALES = [
    {
        "id_usuario":      1,
        "telefono":        "+5491112345678",
        "nombre_completo": "Carlos Martínez",
        "rol":             "GERENTE",
        "id_manager":      None,
        "dias_totales":    21,
        "dias_usados":     3,
    },
    {
        "id_usuario":      2,
        "telefono":        "+5491100000002",
        "nombre_completo": "Andrés Bonelli",
        "rol":             "EMPLEADO",
        "id_manager":      1,
        "dias_totales":    21,
        "dias_usados":     5,
    },
    {
        "id_usuario":      3,
        "telefono":        "+5491100000003",
        "nombre_completo": "Laura García",
        "rol":             "EMPLEADO",
        "id_manager":      1,
        "dias_totales":    14,
        "dias_usados":     7,
    },
    {
        "id_usuario":      4,
        "telefono":        "+5491100000004",
        "nombre_completo": "Martina López",
        "rol":             "EMPLEADO",
        "id_manager":      1,
        "dias_totales":    21,
        "dias_usados":     0,
    },
]

SOLICITUDES_INICIALES = [
    {
        "id_solicitud":     5001,
        "id_empleado":      2,
        "fecha_inicio":     "2026-03-10",
        "fecha_fin":        "2026-03-14",
        "dias_solicitados": 5,
        "estado":           "APROBADA",
        "motivo_rechazo":   None,
        "fecha_creacion":   "2026-03-01 10:30:00",
    },
    {
        "id_solicitud":     5002,
        "id_empleado":      3,
        "fecha_inicio":     "2026-04-01",
        "fecha_fin":        "2026-04-07",
        "dias_solicitados": 5,
        "estado":           "RECHAZADA",
        "motivo_rechazo":   "Período de entrega crítica",
        "fecha_creacion":   "2026-03-15 09:00:00",
    },
    {
        "id_solicitud":     5003,
        "id_empleado":      4,
        "fecha_inicio":     "2026-06-15",
        "fecha_fin":        "2026-06-19",
        "dias_solicitados": 5,
        "estado":           "PENDIENTE",
        "motivo_rechazo":   None,
        "fecha_creacion":   "2026-05-25 11:45:00",
    },
    {
        "id_solicitud":     5004,
        "id_empleado":      2,
        "fecha_inicio":     "2026-07-10",
        "fecha_fin":        "2026-07-18",
        "dias_solicitados": 7,
        "estado":           "PENDIENTE",
        "motivo_rechazo":   None,
        "fecha_creacion":   "2026-05-28 14:20:00",
    },
]
