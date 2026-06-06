"""
estados.py
──────────
Máquina de estados del chatbot de vacaciones.

Estructura:
  • texto_menu_principal()       → texto reutilizable del menú.
  • _avanzar_estado()            → helper para transicionar y persistir.
  • _calcular_saldo_disponible() → helper numérico de días.
  • Un handler privado por cada nodo del flujo BPMN:
        _autenticar()
        _manejar_menu_principal()
        _manejar_fecha_inicio()
        _manejar_fecha_fin()
        _manejar_confirmacion_solicitud()
        _manejar_seleccion_solicitud()
        _manejar_detalle_solicitud()
        _manejar_motivo_rechazo()
        _manejar_periodo_calendario()
        _manejar_filtro_calendario()
        _manejar_nombre_filtro()
  • procesar_mensaje()           → dispatcher público que llama al handler
                                   correspondiente al estado actual.

Ningún handler conoce los archivos JSON; solo llama a base_de_datos.py.
"""

from datetime import datetime

from config import ICONO_POR_ESTADO
from base_de_datos import (
    buscar_usuario_por_telefono,
    buscar_usuario_por_id,
    buscar_solicitud_por_id,
    obtener_sesion,
    guardar_sesion,
    listar_solicitudes_pendientes_del_equipo,
    listar_solicitudes_del_empleado,
    crear_solicitud_vacaciones,
    aprobar_solicitud,
    rechazar_solicitud,
    consultar_calendario_del_equipo,
    calcular_dias_habiles,
)


# ─────────────────────────────────────────────────────────────────────────────
# Texto reutilizable
# ─────────────────────────────────────────────────────────────────────────────

def texto_menu_principal() -> str:
    return (
        "📋 *MENÚ PRINCIPAL*\n"
        "─────────────────────\n"
        "1️⃣  Solicitar vacaciones\n"
        "2️⃣  Aprobar / Rechazar\n"
        "3️⃣  Consultar saldo\n"
        "4️⃣  Ver calendario de equipo\n"
        "─────────────────────\n"
        "Ingresá el número de opción:"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Helpers internos
# ─────────────────────────────────────────────────────────────────────────────

def _avanzar_estado(
    sesion: dict,
    nuevo_estado: str,
    nuevos_datos: dict | None = None,
) -> None:
    """
    Actualiza el nodo actual de la sesión y la persiste en el archivo JSON.
    Si no se pasan nuevos_datos, conserva los datos temporales existentes.
    """
    sesion["estado_chat"] = nuevo_estado
    if nuevos_datos is not None:
        sesion["datos_temporales"] = nuevos_datos
    guardar_sesion(sesion)


def _calcular_saldo_disponible(usuario: dict) -> int:
    return usuario["dias_totales"] - usuario["dias_usados"]


# ─────────────────────────────────────────────────────────────────────────────
# Handlers — uno por nodo del flujo BPMN
# ─────────────────────────────────────────────────────────────────────────────

def _autenticar(id_sesion: str, telefono: str) -> str:
    """
    Primer contacto: valida el número de teléfono, crea la sesión
    y muestra el menú principal.
    """
    usuario = buscar_usuario_por_telefono(telefono)
    if usuario is None:
        return (
            "❌ Acceso denegado.\n"
            "Comunicate con el departamento de Recursos Humanos."
        )

    sesion_nueva = {
        "id_sesion":          id_sesion,
        "id_usuario":         usuario["id_usuario"],
        "estado_chat":        "MENU_PRINCIPAL",
        "datos_temporales":   {},
        "ultima_interaccion": "",
    }
    guardar_sesion(sesion_nueva)

    etiqueta_rol = "👔 Gerente" if usuario["rol"] == "GERENTE" else "👤 Empleado"
    return (
        f"✅ ¡Bienvenido/a, *{usuario['nombre_completo']}*!\n"
        f"Rol: {etiqueta_rol}\n\n"
        + texto_menu_principal()
    )


def _manejar_menu_principal(
    sesion: dict, usuario: dict, mensaje: str
) -> str:
    """Despacha la opción elegida por el usuario desde el menú principal."""

    OPCIONES_SOLICITAR  = {"1", "solicitar vacaciones", "solicitar"}
    OPCIONES_APROBAR    = {"2", "aprobar", "rechazar", "aprobar / rechazar"}
    OPCIONES_SALDO      = {"3", "consultar saldo", "saldo"}
    OPCIONES_CALENDARIO = {"4", "ver calendario", "calendario"}

    # ── Opción 1: Solicitar vacaciones ───────────────────────────────────────
    if mensaje in OPCIONES_SOLICITAR:
        _avanzar_estado(sesion, "ESPERANDO_FECHA_INICIO", {})
        return (
            "📅 *SOLICITAR VACACIONES*\n"
            "─────────────────────\n"
            "Ingresá la *fecha de inicio*.\n"
            "Formato: DD/MM/AAAA\n"
            "Ejemplo: 15/07/2026"
        )

    # ── Opción 2: Aprobar / Rechazar (solo managers) ─────────────────────────
    if mensaje in OPCIONES_APROBAR:
        if usuario["rol"] not in ("GERENTE", "MANAGER"):
            return "⛔ *Sin permisos para este módulo.*\n\n" + texto_menu_principal()

        solicitudes_pendientes = listar_solicitudes_pendientes_del_equipo(
            usuario["id_usuario"]
        )
        if not solicitudes_pendientes:
            return (
                "✅ No hay solicitudes *PENDIENTES* en tu equipo.\n\n"
                + texto_menu_principal()
            )

        lista_pendientes = "📋 *SOLICITUDES PENDIENTES*\n─────────────────────\n"
        for solicitud in solicitudes_pendientes:
            empleado     = buscar_usuario_por_id(solicitud["id_empleado"])
            nombre_empleado = empleado["nombre_completo"] if empleado else "?"
            lista_pendientes += (
                f"🔸 ID #{solicitud['id_solicitud']} — {nombre_empleado}\n"
                f"   {solicitud['fecha_inicio']} → {solicitud['fecha_fin']}"
                f"  ({solicitud['dias_solicitados']} días)\n\n"
            )
        lista_pendientes += "Ingresá el *ID* de la solicitud a evaluar:"
        _avanzar_estado(sesion, "ESPERANDO_SELECCION_SOLICITUD", {})
        return lista_pendientes

    # ── Opción 3: Consultar saldo ─────────────────────────────────────────────
    if mensaje in OPCIONES_SALDO:
        dias_disponibles = _calcular_saldo_disponible(usuario)
        anio_actual      = str(datetime.now().year)

        solicitudes_propias  = listar_solicitudes_del_empleado(usuario["id_usuario"])
        ultimas_tres_del_anio = sorted(
            [s for s in solicitudes_propias if anio_actual in s["fecha_creacion"]],
            key=lambda s: s["fecha_creacion"],
            reverse=True,
        )[:3]

        resumen_saldo = (
            f"💰 *SALDO DE VACACIONES*\n"
            f"─────────────────────\n"
            f"📊 Días totales:      *{usuario['dias_totales']}*\n"
            f"📤 Días usados:       *{usuario['dias_usados']}*\n"
            f"🟢 Días disponibles:  *{dias_disponibles}*\n\n"
        )
        if ultimas_tres_del_anio:
            resumen_saldo += "📋 *Historial reciente:*\n"
            for solicitud in ultimas_tres_del_anio:
                icono_estado = ICONO_POR_ESTADO.get(solicitud["estado"], "❓")
                resumen_saldo += (
                    f"{icono_estado} #{solicitud['id_solicitud']} | "
                    f"{solicitud['fecha_inicio']} → {solicitud['fecha_fin']} | "
                    f"{solicitud['estado']}\n"
                )
        else:
            resumen_saldo += "📋 Sin solicitudes registradas este año."

        return resumen_saldo + "\n\n" + texto_menu_principal()

    # ── Opción 4: Ver calendario de equipo ────────────────────────────────────
    if mensaje in OPCIONES_CALENDARIO:
        _avanzar_estado(sesion, "ESPERANDO_PERIODO_CALENDARIO", {})
        return (
            "📅 *CALENDARIO DE EQUIPO*\n"
            "─────────────────────\n"
            "Seleccioná el período:\n\n"
            "1️⃣  Esta semana\n"
            "2️⃣  Mes en curso\n"
            "3️⃣  Próximos 3 meses"
        )

    return "⚠️ Opción no reconocida.\n\n" + texto_menu_principal()


def _manejar_fecha_inicio(
    sesion: dict, datos_temporales: dict, fecha_raw: str
) -> str:
    """Valida y guarda la fecha de inicio de la solicitud de vacaciones."""
    try:
        datetime.strptime(fecha_raw, "%d/%m/%Y")
    except ValueError:
        return "⚠️ Formato incorrecto. Usá DD/MM/AAAA — Ej: 15/07/2026"

    datos_temporales["fecha_inicio_raw"] = fecha_raw
    _avanzar_estado(sesion, "ESPERANDO_FECHA_FIN", datos_temporales)
    return (
        f"✅ Fecha de inicio: *{fecha_raw}*\n\n"
        "Ahora ingresá la *fecha de fin*.\n"
        "Formato: DD/MM/AAAA\n"
        "Ejemplo: 22/07/2026"
    )


def _manejar_fecha_fin(
    sesion: dict, usuario: dict, datos_temporales: dict, fecha_raw: str
) -> str:
    """
    Valida la fecha de fin, calcula los días hábiles y verifica el saldo.
    Si todo es válido, muestra el resumen para confirmación.
    """
    try:
        fecha_fin_dt    = datetime.strptime(fecha_raw,                         "%d/%m/%Y")
        fecha_inicio_dt = datetime.strptime(datos_temporales["fecha_inicio_raw"], "%d/%m/%Y")
    except ValueError:
        return "⚠️ Formato incorrecto. Usá DD/MM/AAAA — Ej: 22/07/2026"

    if fecha_fin_dt <= fecha_inicio_dt:
        return (
            "⚠️ La fecha de fin debe ser *posterior* al inicio.\n"
            "Ingresá una nueva *fecha de fin*:"
        )

    cantidad_dias, fecha_inicio_iso, fecha_fin_iso = calcular_dias_habiles(
        datos_temporales["fecha_inicio_raw"], fecha_raw
    )
    if cantidad_dias <= 0:
        return "⚠️ El período no contiene días hábiles. Ingresá fechas válidas:"

    dias_disponibles = _calcular_saldo_disponible(usuario)
    if cantidad_dias > dias_disponibles:
        return (
            f"⚠️ *Supera el saldo disponible.*\n"
            f"Solicitados: {cantidad_dias} días | Disponibles: {dias_disponibles} días\n\n"
            "Ingresá una nueva *fecha de fin*:"
        )

    datos_temporales.update({
        "fecha_fin_raw":    fecha_raw,
        "fecha_inicio_iso": fecha_inicio_iso,
        "fecha_fin_iso":    fecha_fin_iso,
        "dias_habiles":     cantidad_dias,
    })
    _avanzar_estado(sesion, "CONFIRMACION_SOLICITUD", datos_temporales)
    return (
        f"📋 *RESUMEN DE SOLICITUD*\n"
        f"─────────────────────\n"
        f"👤 {usuario['nombre_completo']}\n"
        f"📅 Inicio:       *{datos_temporales['fecha_inicio_raw']}*\n"
        f"📅 Fin:          *{fecha_raw}*\n"
        f"📆 Días hábiles: *{cantidad_dias}*\n\n"
        f"¿Confirmás?\n"
        f"[Confirmar] / [Cancelar]"
    )


def _manejar_confirmacion_solicitud(
    sesion: dict, usuario: dict, datos_temporales: dict, mensaje: str
) -> str:
    """Crea la solicitud si el usuario confirma, o la descarta si cancela."""
    RESPUESTAS_AFIRMATIVAS = {"confirmar", "si", "sí", "s", "1"}
    RESPUESTAS_NEGATIVAS   = {"cancelar",  "no", "n",  "0"}

    if mensaje in RESPUESTAS_AFIRMATIVAS:
        nueva_solicitud = crear_solicitud_vacaciones(
            usuario["id_usuario"],
            datos_temporales["fecha_inicio_iso"],
            datos_temporales["fecha_fin_iso"],
            datos_temporales["dias_habiles"],
        )
        manager = buscar_usuario_por_id(usuario.get("id_manager"))
        notificacion_manager = (
            f"\n📨 Notificación enviada a *{manager['nombre_completo']}*."
            if manager else ""
        )
        _avanzar_estado(sesion, "MENU_PRINCIPAL", {})
        return (
            f"✅ *¡Solicitud enviada con éxito!*\n"
            f"ID: *#{nueva_solicitud['id_solicitud']}* | Estado: *PENDIENTE*"
            f"{notificacion_manager}\n\n"
            + texto_menu_principal()
        )

    if mensaje in RESPUESTAS_NEGATIVAS:
        _avanzar_estado(sesion, "MENU_PRINCIPAL", {})
        return "❌ Solicitud cancelada.\n\n" + texto_menu_principal()

    return "Respondé *Confirmar* o *Cancelar*:"


def _manejar_seleccion_solicitud(
    sesion: dict, datos_temporales: dict, texto_ingresado: str
) -> str:
    """Busca la solicitud por el ID ingresado y muestra su detalle."""
    try:
        id_solicitud_elegida = int(texto_ingresado.replace("#", "").strip())
    except ValueError:
        return "⚠️ Ingresá solo el número del ID (ej: 5003):"

    solicitud_elegida = buscar_solicitud_por_id(id_solicitud_elegida)
    if solicitud_elegida is None:
        return f"⚠️ No existe solicitud con ID #{id_solicitud_elegida}. Ingresá un ID válido:"
    if solicitud_elegida["estado"] != "PENDIENTE":
        return (
            f"⚠️ La solicitud #{id_solicitud_elegida} ya fue procesada "
            f"(Estado: {solicitud_elegida['estado']}).\n"
            "Ingresá otro ID:"
        )

    empleado = buscar_usuario_por_id(solicitud_elegida["id_empleado"])
    datos_temporales["id_solicitud_seleccionada"] = id_solicitud_elegida
    _avanzar_estado(sesion, "DETALLE_SOLICITUD", datos_temporales)
    return (
        f"📋 *DETALLE — Solicitud #{id_solicitud_elegida}*\n"
        f"─────────────────────\n"
        f"👤 Empleado:     *{empleado['nombre_completo']}*\n"
        f"📅 Período:      {solicitud_elegida['fecha_inicio']} → {solicitud_elegida['fecha_fin']}\n"
        f"📆 Días hábiles: *{solicitud_elegida['dias_solicitados']}*\n"
        f"🕐 Creada:       {solicitud_elegida['fecha_creacion']}\n\n"
        f"¿Qué acción tomás?\n"
        f"[Aprobar] / [Rechazar]"
    )


def _manejar_detalle_solicitud(
    sesion: dict, datos_temporales: dict, mensaje: str
) -> str:
    """Procesa la decisión del manager: aprobar o rechazar."""
    id_solicitud_seleccionada = datos_temporales["id_solicitud_seleccionada"]

    if mensaje in ("aprobar", "a", "1"):
        solicitud_aprobada = aprobar_solicitud(id_solicitud_seleccionada)
        empleado           = buscar_usuario_por_id(solicitud_aprobada["id_empleado"])
        _avanzar_estado(sesion, "MENU_PRINCIPAL", {})
        return (
            f"✅ *Solicitud #{id_solicitud_seleccionada} APROBADA.*\n"
            f"Se notificó a *{empleado['nombre_completo']}*.\n\n"
            + texto_menu_principal()
        )

    if mensaje in ("rechazar", "r", "2"):
        _avanzar_estado(sesion, "ESPERANDO_MOTIVO_RECHAZO", datos_temporales)
        return "✏️ Ingresá el *motivo del rechazo* (obligatorio):"

    return "Respondé *Aprobar* o *Rechazar*:"


def _manejar_motivo_rechazo(
    sesion: dict, datos_temporales: dict, motivo_ingresado: str
) -> str:
    """Valida el motivo y persiste el rechazo de la solicitud."""
    LONGITUD_MINIMA_MOTIVO = 5
    if len(motivo_ingresado) < LONGITUD_MINIMA_MOTIVO:
        return (
            f"⚠️ El motivo debe tener al menos {LONGITUD_MINIMA_MOTIVO} "
            "caracteres. Ingresalo nuevamente:"
        )

    id_solicitud_seleccionada = datos_temporales["id_solicitud_seleccionada"]
    solicitud_rechazada       = rechazar_solicitud(
        id_solicitud_seleccionada, motivo_ingresado
    )
    empleado = buscar_usuario_por_id(solicitud_rechazada["id_empleado"])
    _avanzar_estado(sesion, "MENU_PRINCIPAL", {})
    return (
        f"❌ *Solicitud #{id_solicitud_seleccionada} RECHAZADA.*\n"
        f"Motivo: _{motivo_ingresado}_\n"
        f"Se notificó a *{empleado['nombre_completo']}*.\n\n"
        + texto_menu_principal()
    )


def _manejar_periodo_calendario(
    sesion: dict, usuario: dict, datos_temporales: dict, mensaje: str
) -> str:
    """Obtiene las ausencias del equipo para el período elegido."""
    OPCIONES_VALIDAS = {"1", "2", "3"}
    if mensaje not in OPCIONES_VALIDAS:
        return (
            "⚠️ Ingresá 1, 2 o 3:\n"
            "1️⃣ Esta semana\n"
            "2️⃣ Mes en curso\n"
            "3️⃣ Próximos 3 meses"
        )

    id_manager = (
        usuario["id_usuario"]
        if usuario["rol"] == "GERENTE"
        else usuario.get("id_manager")
    )
    ausencias_del_periodo, etiqueta_periodo = consultar_calendario_del_equipo(
        id_manager, mensaje
    )

    cuerpo_calendario = (
        f"📅 *CALENDARIO — {etiqueta_periodo.upper()}*\n"
        "─────────────────────\n"
    )
    if not ausencias_del_periodo:
        cuerpo_calendario += "✅ No hay ausencias en este período."
    else:
        for ausencia in ausencias_del_periodo:
            icono_estado = ICONO_POR_ESTADO.get(ausencia["estado"], "❓")
            cuerpo_calendario += (
                f"{icono_estado} *{ausencia['nombre']}*\n"
                f"   {ausencia['fecha_inicio']} → {ausencia['fecha_fin']}"
                f" | {ausencia['estado']}\n\n"
            )

    datos_temporales["ausencias_del_calendario"] = ausencias_del_periodo
    _avanzar_estado(sesion, "FILTRO_CALENDARIO", datos_temporales)
    return cuerpo_calendario + "\n❓ *¿Filtrás por persona?*\n[Sí] / [No]"


def _manejar_filtro_calendario(
    sesion: dict, datos_temporales: dict, mensaje: str
) -> str:
    """Pregunta si el usuario quiere filtrar el calendario por nombre."""
    if mensaje in ("no", "n"):
        _avanzar_estado(sesion, "MENU_PRINCIPAL", {})
        return "✅ Consulta finalizada.\n\n" + texto_menu_principal()

    if mensaje in ("si", "sí", "s"):
        _avanzar_estado(sesion, "ESPERANDO_NOMBRE_FILTRO", datos_temporales)
        return "✏️ Ingresá el nombre del colaborador:"

    return "Respondé *Sí* o *No*:"


def _manejar_nombre_filtro(
    sesion: dict, datos_temporales: dict, nombre_buscado: str
) -> str:
    """Filtra las ausencias del calendario por el nombre ingresado."""
    termino_busqueda  = nombre_buscado.lower()
    todas_las_ausencias   = datos_temporales.get("ausencias_del_calendario", [])
    ausencias_encontradas = [
        ausencia for ausencia in todas_las_ausencias
        if termino_busqueda in ausencia["nombre"].lower()
    ]
    _avanzar_estado(sesion, "MENU_PRINCIPAL", {})

    if not ausencias_encontradas:
        return (
            f"⚠️ Sin resultados para *'{nombre_buscado}'*.\n\n"
            + texto_menu_principal()
        )

    resultado_filtrado = f"🔍 *Resultados para '{nombre_buscado}':*\n─────────────────────\n"
    for ausencia in ausencias_encontradas:
        icono_estado = ICONO_POR_ESTADO.get(ausencia["estado"], "❓")
        resultado_filtrado += (
            f"{icono_estado} *{ausencia['nombre']}*\n"
            f"   {ausencia['fecha_inicio']} → {ausencia['fecha_fin']}"
            f" | {ausencia['estado']}\n\n"
        )
    return resultado_filtrado + texto_menu_principal()


# ─────────────────────────────────────────────────────────────────────────────
# Dispatcher principal (único punto de entrada público)
# ─────────────────────────────────────────────────────────────────────────────

def procesar_mensaje(id_sesion: str, mensaje_raw: str, telefono: str) -> str:
    """
    Recibe el mensaje del usuario y retorna la respuesta del bot.

    Flujo:
      1. Si no existe sesión → autenticación.
      2. Si existe → despacha al handler del estado actual.
      3. Si el estado es desconocido → reinicio de seguridad al menú.

    Los mensajes para el menú y comandos de texto se comparan en minúsculas.
    Las fechas y motivos de rechazo se pasan sin modificar (mayúsculas/minúsculas
    son irrelevantes para fechas; los motivos deben preservar la capitalización).
    """
    sesion = obtener_sesion(id_sesion)

    # Primera interacción: sin sesión → autenticación
    if sesion is None:
        return _autenticar(id_sesion, telefono)

    usuario          = buscar_usuario_por_id(sesion["id_usuario"])
    estado_actual    = sesion["estado_chat"]
    datos_temporales = sesion.get("datos_temporales", {})

    # Versión en minúsculas para comparaciones insensibles a mayúsculas
    mensaje_normalizado = mensaje_raw.strip().lower()
    # Versión con capitalización original para fechas y texto libre
    mensaje_original    = mensaje_raw.strip()

    DISPATCHER = {
        "MENU_PRINCIPAL": lambda: _manejar_menu_principal(
            sesion, usuario, mensaje_normalizado
        ),
        "ESPERANDO_FECHA_INICIO": lambda: _manejar_fecha_inicio(
            sesion, datos_temporales, mensaje_original
        ),
        "ESPERANDO_FECHA_FIN": lambda: _manejar_fecha_fin(
            sesion, usuario, datos_temporales, mensaje_original
        ),
        "CONFIRMACION_SOLICITUD": lambda: _manejar_confirmacion_solicitud(
            sesion, usuario, datos_temporales, mensaje_normalizado
        ),
        "ESPERANDO_SELECCION_SOLICITUD": lambda: _manejar_seleccion_solicitud(
            sesion, datos_temporales, mensaje_original
        ),
        "DETALLE_SOLICITUD": lambda: _manejar_detalle_solicitud(
            sesion, datos_temporales, mensaje_normalizado
        ),
        "ESPERANDO_MOTIVO_RECHAZO": lambda: _manejar_motivo_rechazo(
            sesion, datos_temporales, mensaje_original
        ),
        "ESPERANDO_PERIODO_CALENDARIO": lambda: _manejar_periodo_calendario(
            sesion, usuario, datos_temporales, mensaje_normalizado
        ),
        "FILTRO_CALENDARIO": lambda: _manejar_filtro_calendario(
            sesion, datos_temporales, mensaje_normalizado
        ),
        "ESPERANDO_NOMBRE_FILTRO": lambda: _manejar_nombre_filtro(
            sesion, datos_temporales, mensaje_original
        ),
    }

    handler = DISPATCHER.get(estado_actual)
    if handler:
        return handler()

    # Estado desconocido: reinicio de seguridad
    _avanzar_estado(sesion, "MENU_PRINCIPAL", {})
    return "⚠️ Estado no reconocido. Reiniciando...\n\n" + texto_menu_principal()
