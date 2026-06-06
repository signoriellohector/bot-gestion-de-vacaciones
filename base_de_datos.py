"""
base_de_datos.py
────────────────
Capa de acceso a datos del simulador.

Responsabilidades:
  • Leer y escribir archivos JSON (primitivas cargar / guardar).
  • Inicializar el directorio `db/` con datos semilla en el primer arranque.
  • Exponer operaciones con nombre de dominio claro para cada entidad:
      - Usuarios    → buscar, actualizar días usados
      - Solicitudes → listar, crear, aprobar, rechazar, consultar calendario
      - Sesiones    → obtener, guardar (máquina de estados)
      - Fechas      → calcular días hábiles

Los módulos de nivel superior (estados.py, interfaz.py) solo llaman a estas
funciones; ninguno accede a los archivos JSON directamente.
"""

import json
import os
from datetime import datetime, date, timedelta

from config import (
    DIRECTORIO_DB,
    ARCHIVO_USUARIOS,
    ARCHIVO_SOLICITUDES,
    ARCHIVO_SESIONES,
    USUARIOS_INICIALES,
    SOLICITUDES_INICIALES,
)


# ─────────────────────────────────────────────────────────────────────────────
# Primitivas JSON
# ─────────────────────────────────────────────────────────────────────────────

def cargar_json(ruta_archivo: str) -> list:
    """Lee un archivo JSON y retorna su contenido como lista."""
    if not os.path.exists(ruta_archivo):
        return []
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_json(ruta_archivo: str, registros: list) -> None:
    """Serializa una lista de registros y la escribe en el archivo JSON."""
    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(registros, archivo, ensure_ascii=False, indent=2, default=str)


# ─────────────────────────────────────────────────────────────────────────────
# Inicialización de la base de datos
# ─────────────────────────────────────────────────────────────────────────────

def inicializar_base_de_datos() -> None:
    """
    Crea la carpeta `db/` y los tres archivos JSON con datos semilla
    si todavía no existen. Operación idempotente: no borra datos previos.
    """
    os.makedirs(DIRECTORIO_DB, exist_ok=True)
    if not os.path.exists(ARCHIVO_USUARIOS):
        guardar_json(ARCHIVO_USUARIOS, USUARIOS_INICIALES)
    if not os.path.exists(ARCHIVO_SOLICITUDES):
        guardar_json(ARCHIVO_SOLICITUDES, SOLICITUDES_INICIALES)
    if not os.path.exists(ARCHIVO_SESIONES):
        guardar_json(ARCHIVO_SESIONES, [])


# ─────────────────────────────────────────────────────────────────────────────
# Usuarios
# ─────────────────────────────────────────────────────────────────────────────

def buscar_usuario_por_telefono(telefono: str) -> dict | None:
    """Retorna el usuario cuyo teléfono coincide, o None si no existe."""
    todos_los_usuarios = cargar_json(ARCHIVO_USUARIOS)
    return next(
        (usuario for usuario in todos_los_usuarios
         if usuario["telefono"] == telefono),
        None,
    )


def buscar_usuario_por_id(id_usuario: int) -> dict | None:
    """Retorna el usuario con el ID indicado, o None si no existe."""
    todos_los_usuarios = cargar_json(ARCHIVO_USUARIOS)
    return next(
        (usuario for usuario in todos_los_usuarios
         if usuario["id_usuario"] == id_usuario),
        None,
    )


def listar_todos_los_usuarios() -> list:
    """Retorna la lista completa de usuarios registrados."""
    return cargar_json(ARCHIVO_USUARIOS)


def incrementar_dias_usados(id_usuario: int, dias_a_sumar: int) -> None:
    """Suma los días aprobados al contador de días usados del empleado."""
    todos_los_usuarios = cargar_json(ARCHIVO_USUARIOS)
    for usuario in todos_los_usuarios:
        if usuario["id_usuario"] == id_usuario:
            usuario["dias_usados"] += dias_a_sumar
            break
    guardar_json(ARCHIVO_USUARIOS, todos_los_usuarios)


# ─────────────────────────────────────────────────────────────────────────────
# Solicitudes
# ─────────────────────────────────────────────────────────────────────────────

def buscar_solicitud_por_id(id_solicitud: int) -> dict | None:
    """Retorna la solicitud con el ID indicado, o None si no existe."""
    todas_las_solicitudes = cargar_json(ARCHIVO_SOLICITUDES)
    return next(
        (solicitud for solicitud in todas_las_solicitudes
         if solicitud["id_solicitud"] == id_solicitud),
        None,
    )


def listar_solicitudes_pendientes_del_equipo(id_manager: int) -> list:
    """
    Retorna las solicitudes en estado PENDIENTE pertenecientes
    a los empleados que reportan directamente al manager indicado.
    """
    todos_los_usuarios    = cargar_json(ARCHIVO_USUARIOS)
    todas_las_solicitudes = cargar_json(ARCHIVO_SOLICITUDES)

    ids_del_equipo = {
        usuario["id_usuario"]
        for usuario in todos_los_usuarios
        if usuario.get("id_manager") == id_manager
    }
    return [
        solicitud
        for solicitud in todas_las_solicitudes
        if solicitud["id_empleado"] in ids_del_equipo
        and solicitud["estado"] == "PENDIENTE"
    ]


def listar_solicitudes_del_empleado(id_empleado: int) -> list:
    """Retorna todas las solicitudes de un empleado, sin importar su estado."""
    return [
        solicitud
        for solicitud in cargar_json(ARCHIVO_SOLICITUDES)
        if solicitud["id_empleado"] == id_empleado
    ]


def crear_solicitud_vacaciones(
    id_empleado: int,
    fecha_inicio_iso: str,
    fecha_fin_iso: str,
    dias_habiles: int,
) -> dict:
    """
    Crea una nueva solicitud en estado PENDIENTE, le asigna un ID
    correlativo y la persiste en el archivo JSON.
    Retorna el dict de la solicitud recién creada.
    """
    todas_las_solicitudes = cargar_json(ARCHIVO_SOLICITUDES)
    nuevo_id = max(
        (solicitud["id_solicitud"] for solicitud in todas_las_solicitudes),
        default=5000,
    ) + 1
    nueva_solicitud = {
        "id_solicitud":     nuevo_id,
        "id_empleado":      id_empleado,
        "fecha_inicio":     fecha_inicio_iso,
        "fecha_fin":        fecha_fin_iso,
        "dias_solicitados": dias_habiles,
        "estado":           "PENDIENTE",
        "motivo_rechazo":   None,
        "fecha_creacion":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    todas_las_solicitudes.append(nueva_solicitud)
    guardar_json(ARCHIVO_SOLICITUDES, todas_las_solicitudes)
    return nueva_solicitud


def aprobar_solicitud(id_solicitud: int) -> dict:
    """
    Cambia el estado de la solicitud a APROBADA, actualiza el contador
    de días usados del empleado y persiste ambos cambios.
    Retorna la solicitud actualizada.
    """
    todas_las_solicitudes = cargar_json(ARCHIVO_SOLICITUDES)
    solicitud_aprobada    = None

    for solicitud in todas_las_solicitudes:
        if solicitud["id_solicitud"] == id_solicitud:
            solicitud["estado"] = "APROBADA"
            solicitud_aprobada  = solicitud
            break

    guardar_json(ARCHIVO_SOLICITUDES, todas_las_solicitudes)
    incrementar_dias_usados(
        solicitud_aprobada["id_empleado"],
        solicitud_aprobada["dias_solicitados"],
    )
    return solicitud_aprobada


def rechazar_solicitud(id_solicitud: int, motivo_de_rechazo: str) -> dict:
    """
    Cambia el estado de la solicitud a RECHAZADA, guarda el motivo
    y persiste el cambio.
    Retorna la solicitud actualizada.
    """
    todas_las_solicitudes = cargar_json(ARCHIVO_SOLICITUDES)
    solicitud_rechazada   = None

    for solicitud in todas_las_solicitudes:
        if solicitud["id_solicitud"] == id_solicitud:
            solicitud["estado"]         = "RECHAZADA"
            solicitud["motivo_rechazo"] = motivo_de_rechazo
            solicitud_rechazada         = solicitud
            break

    guardar_json(ARCHIVO_SOLICITUDES, todas_las_solicitudes)
    return solicitud_rechazada


def consultar_calendario_del_equipo(
    id_manager: int,
    opcion_periodo: str,
) -> tuple[list, str]:
    """
    Retorna las ausencias (PENDIENTE o APROBADA) del equipo del manager
    para el período elegido, ordenadas por fecha de inicio.

    opcion_periodo:
        "1" → Esta semana
        "2" → Mes en curso
        "3" → Próximos 3 meses

    Retorna: (lista_de_ausencias, etiqueta_legible_del_período)
    """
    todos_los_usuarios    = cargar_json(ARCHIVO_USUARIOS)
    todas_las_solicitudes = cargar_json(ARCHIVO_SOLICITUDES)

    # El gerente ve su propio equipo; también se incluye a sí mismo
    ids_del_equipo = {
        usuario["id_usuario"]
        for usuario in todos_los_usuarios
        if usuario.get("id_manager") == id_manager
        or usuario["id_usuario"] == id_manager
    }

    hoy = date.today()
    if opcion_periodo == "1":
        inicio_periodo   = hoy - timedelta(days=hoy.weekday())
        fin_periodo      = inicio_periodo + timedelta(days=6)
        etiqueta_periodo = "Esta semana"
    elif opcion_periodo == "2":
        inicio_periodo   = hoy.replace(day=1)
        fin_periodo      = (
            hoy.replace(year=hoy.year + 1, month=1, day=1)
            if hoy.month == 12
            else hoy.replace(month=hoy.month + 1, day=1)
        ) - timedelta(days=1)
        etiqueta_periodo = "Mes en curso"
    else:
        inicio_periodo   = hoy
        fin_periodo      = hoy + timedelta(days=90)
        etiqueta_periodo = "Próximos 3 meses"

    ausencias_en_periodo = []
    for solicitud in todas_las_solicitudes:
        if (solicitud["id_empleado"] not in ids_del_equipo
                or solicitud["estado"] not in ("PENDIENTE", "APROBADA")):
            continue
        inicio_solicitud = datetime.strptime(solicitud["fecha_inicio"], "%Y-%m-%d").date()
        fin_solicitud    = datetime.strptime(solicitud["fecha_fin"],    "%Y-%m-%d").date()
        hay_solapamiento = not (fin_solicitud < inicio_periodo
                                or inicio_solicitud > fin_periodo)
        if hay_solapamiento:
            empleado = buscar_usuario_por_id(solicitud["id_empleado"])
            ausencias_en_periodo.append({
                "nombre":       empleado["nombre_completo"] if empleado else "?",
                "fecha_inicio": solicitud["fecha_inicio"],
                "fecha_fin":    solicitud["fecha_fin"],
                "estado":       solicitud["estado"],
            })

    ausencias_ordenadas = sorted(
        ausencias_en_periodo,
        key=lambda ausencia: ausencia["fecha_inicio"],
    )
    return ausencias_ordenadas, etiqueta_periodo


# ─────────────────────────────────────────────────────────────────────────────
# Sesiones (persistencia de la máquina de estados)
# ─────────────────────────────────────────────────────────────────────────────

def obtener_sesion(id_sesion: str) -> dict | None:
    """Retorna la sesión activa para el ID de chat dado, o None."""
    todas_las_sesiones = cargar_json(ARCHIVO_SESIONES)
    return next(
        (sesion for sesion in todas_las_sesiones
         if sesion["id_sesion"] == id_sesion),
        None,
    )


def guardar_sesion(sesion: dict) -> None:
    """
    Inserta o reemplaza la sesión en el archivo de persistencia,
    actualizando la marca de tiempo de última interacción.
    """
    sesiones_sin_la_actual = [
        s for s in cargar_json(ARCHIVO_SESIONES)
        if s["id_sesion"] != sesion["id_sesion"]
    ]
    sesion["ultima_interaccion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sesiones_sin_la_actual.append(sesion)
    guardar_json(ARCHIVO_SESIONES, sesiones_sin_la_actual)


# ─────────────────────────────────────────────────────────────────────────────
# Utilidades de fecha
# ─────────────────────────────────────────────────────────────────────────────

def calcular_dias_habiles(
    fecha_inicio_raw: str,
    fecha_fin_raw: str,
) -> tuple[int, str, str]:
    """
    Cuenta los días hábiles (lunes a viernes) entre dos fechas
    en formato DD/MM/AAAA, ambas inclusive.

    Retorna: (cantidad_dias, fecha_inicio_ISO, fecha_fin_ISO)
    """
    fecha_inicio  = datetime.strptime(fecha_inicio_raw, "%d/%m/%Y").date()
    fecha_fin     = datetime.strptime(fecha_fin_raw,    "%d/%m/%Y").date()
    cantidad_dias = 0
    dia_actual    = fecha_inicio

    while dia_actual <= fecha_fin:
        if dia_actual.weekday() < 5:   # 0=lunes … 4=viernes
            cantidad_dias += 1
        dia_actual += timedelta(days=1)

    return (
        cantidad_dias,
        fecha_inicio.strftime("%Y-%m-%d"),
        fecha_fin.strftime("%Y-%m-%d"),
    )
