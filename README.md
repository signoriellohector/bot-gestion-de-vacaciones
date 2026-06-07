# 🤖 Bot de Gestión de Vacaciones — Simulador WhatsApp

Chatbot de autoservicio para la gestión de licencias del equipo de desarrollo.
Simula en la terminal la interfaz de WhatsApp con burbujas de chat, colores ANSI
y persistencia de estado en archivos JSON locales.

---

## Contenido

- [Instalación](#instalación)
- [Cómo iniciarlo](#cómo-iniciarlo)
- [Usuarios de prueba](#usuarios-de-prueba)
- [Despliegue del bot](#despliegue-del-bot)
  - [Pantalla de inicio](#pantalla-de-inicio)
  - [Flujo 1 — Empleado solicita vacaciones](#flujo-1--empleado-solicita-vacaciones)
  - [Flujo 2 — Gerente rechaza una solicitud](#flujo-2--gerente-rechaza-una-solicitud)
  - [Flujo 3 — Acceso denegado](#flujo-3--acceso-denegado)
- [Arquitectura de módulos](#arquitectura-de-módulos)
- [Estructura de archivos](#estructura-de-archivos)
- [Esquema de la base de datos JSON](#esquema-de-la-base-de-datos-json)

---

## Instalación

El simulador solo usa la librería estándar de Python. No requiere `pip install`.

```bash
# Cloná o copiá los archivos del proyecto
git clone https://github.com/signoriellohector/bot-gestion-de-vacaciones.git
cd bot-gestion-de-vacaciones
```

**Requisito:** Python 3.10 o superior (usa `dict | None` como anotación de tipo).

---

## Cómo iniciarlo

```bash
python3 main.py
```

Al arrancar por primera vez, el sistema crea automáticamente la carpeta `db/`
con tres archivos JSON precargados con datos de ejemplo.

Para **reiniciar la base de datos** desde cero:

```bash
rm -rf db/ && python3 main.py
```

Para **salir** de la sesión en cualquier momento:

```
✏  Vos > salir
```

---

## Usuarios de prueba

| Ícono | Nombre            | Teléfono          | Rol      | Días totales | Días usados |
|-------|-------------------|-------------------|----------|:------------:|:-----------:|
| 👔    | Carlos Martínez   | +5491100000001    | GERENTE  | 21           | 3           |
| 👤    | Andrés Bonelli    | +5491100000002    | EMPLEADO | 21           | 5           |
| 👤    | Laura García      | +5491100000003    | EMPLEADO | 14           | 7           |
| 👤    | Martina López     | +5491100000004    | EMPLEADO | 21           | 0           |

> Cualquier otro número recibe **acceso denegado**.

---

## Despliegue del bot

Las capturas a continuación muestran la salida real del simulador en terminal.
Las burbujas del bot aparecen a la **izquierda** (fondo gris oscuro) y las del
usuario a la **derecha** (fondo verde oscuro).

### Pantalla de inicio

```
╔══════════════════════════════════════════════════════════════════╗
  📱  Bot Gestión de Vacaciones
  Simulador WhatsApp — Persistencia en JSON
──────────────────────────────────────────────────────────────────

👥 USUARIOS DEL SISTEMA:
────────────────────────────────────────────────────────────
  Nombre                     Teléfono               Rol
────────────────────────────────────────────────────────────
  👔 Carlos Martínez         +5491100000001         GERENTE
  👤 Andrés Bonelli          +5491100000002         EMPLEADO
  👤 Laura García            +5491100000003         EMPLEADO
  👤 Martina López           +5491100000004         EMPLEADO
────────────────────────────────────────────────────────────

Ingresá tu número de WhatsApp para iniciar sesión:
(copiá uno de la lista de arriba)

  📱 Teléfono > _
```

---

### Flujo 1 — Empleado solicita vacaciones

Sesión iniciada con **Andrés Bonelli** (`+5491100000002`).

```
──────────────────────────────────────────────────────────────────
                                                                Vos
                                              ┌─────────────────┐
                                              │  Hola 👋        │
                                              └─────────────────┘
                                                           19:04

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────────┐
  │ ✅ ¡Bienvenido/a, *Andrés Bonelli*!                      │
  │ Rol: 👤 Empleado                                         │
  │                                                          │
  │ 📋 *MENÚ PRINCIPAL*                                      │
  │ ─────────────────────                                    │
  │ 1️⃣  Solicitar vacaciones                                 │
  │ 2️⃣  Aprobar / Rechazar                                   │
  │ 3️⃣  Consultar saldo                                      │
  │ 4️⃣  Ver calendario de equipo                             │
  │ ─────────────────────                                    │
  │ Ingresá el número de opción:                             │
  └──────────────────────────────────────────────────────────┘
  19:04

──────────────────────────────────────────────────────────────────
✏  Vos > 1
──────────────────────────────────────────────────────────────────
                                                                Vos
                                              ┌─────────────────┐
                                              │  1              │
                                              └─────────────────┘
                                                           19:04

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────────┐
  │ 📅 *SOLICITAR VACACIONES*                                │
  │ ─────────────────────                                    │
  │ Ingresá la *fecha de inicio*.                            │
  │ Formato: DD/MM/AAAA                                      │
  │ Ejemplo: 15/07/2026                                      │
  └──────────────────────────────────────────────────────────┘
  19:04

──────────────────────────────────────────────────────────────────
✏  Vos > 15/07/2026
──────────────────────────────────────────────────────────────────
                                                                Vos
                                              ┌─────────────────┐
                                              │  15/07/2026     │
                                              └─────────────────┘
                                                           19:05

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────────┐
  │ ✅ Fecha de inicio: *15/07/2026*                         │
  │                                                          │
  │ Ahora ingresá la *fecha de fin*.                         │
  │ Formato: DD/MM/AAAA                                      │
  │ Ejemplo: 22/07/2026                                      │
  └──────────────────────────────────────────────────────────┘
  19:05

──────────────────────────────────────────────────────────────────
✏  Vos > 25/07/2026
──────────────────────────────────────────────────────────────────
                                                                Vos
                                              ┌─────────────────┐
                                              │  25/07/2026     │
                                              └─────────────────┘
                                                           19:05

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────────┐
  │ 📋 *RESUMEN DE SOLICITUD*                                │
  │ ─────────────────────                                    │
  │ 👤 Andrés Bonelli                                        │
  │ 📅 Inicio:       *15/07/2026*                            │
  │ 📅 Fin:          *25/07/2026*                            │
  │ 📆 Días hábiles: *8*                                     │
  │                                                          │
  │ ¿Confirmás?                                              │
  │ [Confirmar] / [Cancelar]                                 │
  └──────────────────────────────────────────────────────────┘
  19:05

──────────────────────────────────────────────────────────────────
✏  Vos > confirmar
──────────────────────────────────────────────────────────────────
                                                                Vos
                                              ┌─────────────────┐
                                              │  confirmar      │
                                              └─────────────────┘
                                                           19:06

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────────┐
  │ ✅ *¡Solicitud enviada con éxito!*                       │
  │ ID: *#5005* | Estado: *PENDIENTE*                        │
  │ 📨 Notificación enviada a *Carlos Martínez*.             │
  │                                                          │
  │ 📋 *MENÚ PRINCIPAL*                                      │
  │ ─────────────────────                                    │
  │ 1️⃣  Solicitar vacaciones                                 │
  │ 2️⃣  Aprobar / Rechazar                                   │
  │ 3️⃣  Consultar saldo                                      │
  │ 4️⃣  Ver calendario de equipo                             │
  │ ─────────────────────                                    │
  │ Ingresá el número de opción:                             │
  └──────────────────────────────────────────────────────────┘
  19:06

──────────────────────────────────────────────────────────────────
✏  Vos > 3
──────────────────────────────────────────────────────────────────
                                                                Vos
                                              ┌─────────────────┐
                                              │  3              │
                                              └─────────────────┘
                                                           19:06

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────────┐
  │ 💰 *SALDO DE VACACIONES*                                 │
  │ ─────────────────────                                    │
  │ 📊 Días totales:      *21*                               │
  │ 📤 Días usados:       *5*                                │
  │ 🟢 Días disponibles:  *16*                               │
  │                                                          │
  │ 📋 *Historial reciente:*                                 │
  │ ⏳ #5005 | 2026-07-15 → 2026-07-25 | PENDIENTE           │
  │ ⏳ #5004 | 2026-07-10 → 2026-07-18 | PENDIENTE           │
  │ ✅ #5001 | 2026-03-10 → 2026-03-14 | APROBADA            │
  └──────────────────────────────────────────────────────────┘
  19:07
```

---

### Flujo 2 — Gerente rechaza una solicitud

Sesión iniciada con **Carlos Martínez** (`+5491100000001`).

```
──────────────────────────────────────────────────────────────────
                                                                Vos
                                              ┌─────────────────┐
                                              │  Hola 👋        │
                                              └─────────────────┘
                                                           19:10

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────────┐
  │ ✅ ¡Bienvenido/a, *Carlos Martínez*!                     │
  │ Rol: 👔 Gerente                                          │
  │                                                          │
  │ 📋 *MENÚ PRINCIPAL*                                      │
  │ ─────────────────────                                    │
  │ 1️⃣  Solicitar vacaciones                                 │
  │ 2️⃣  Aprobar / Rechazar                                   │
  │ 3️⃣  Consultar saldo                                      │
  │ 4️⃣  Ver calendario de equipo                             │
  │ ─────────────────────                                    │
  │ Ingresá el número de opción:                             │
  └──────────────────────────────────────────────────────────┘
  19:10

──────────────────────────────────────────────────────────────────
✏  Vos > 2
──────────────────────────────────────────────────────────────────
                                                                Vos
                                              ┌─────────────────┐
                                              │  2              │
                                              └─────────────────┘
                                                           19:10

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────────┐
  │ 📋 *SOLICITUDES PENDIENTES*                              │
  │ ─────────────────────                                    │
  │ 🔸 ID #5003 — Martina López                              │
  │    2026-06-15 → 2026-06-19  (5 días)                     │
  │                                                          │
  │ 🔸 ID #5004 — Andrés Bonelli                             │
  │    2026-07-10 → 2026-07-18  (7 días)                     │
  │                                                          │
  │ 🔸 ID #5005 — Andrés Bonelli                             │
  │    2026-07-15 → 2026-07-25  (8 días)                     │
  │                                                          │
  │ Ingresá el *ID* de la solicitud a evaluar:               │
  └──────────────────────────────────────────────────────────┘
  19:10

──────────────────────────────────────────────────────────────────
✏  Vos > 5003
──────────────────────────────────────────────────────────────────
                                                                Vos
                                              ┌─────────────────┐
                                              │  5003           │
                                              └─────────────────┘
                                                           19:11

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────────┐
  │ 📋 *DETALLE — Solicitud #5003*                           │
  │ ─────────────────────                                    │
  │ 👤 Empleado:     *Martina López*                         │
  │ 📅 Período:      2026-06-15 → 2026-06-19                 │
  │ 📆 Días hábiles: *5*                                     │
  │ 🕐 Creada:       2026-05-25 11:45:00                     │
  │                                                          │
  │ ¿Qué acción tomás?                                       │
  │ [Aprobar] / [Rechazar]                                   │
  └──────────────────────────────────────────────────────────┘
  19:11

──────────────────────────────────────────────────────────────────
✏  Vos > Rechazar
──────────────────────────────────────────────────────────────────
                                                                Vos
                                              ┌─────────────────┐
                                              │  Rechazar       │
                                              └─────────────────┘
                                                           19:11

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────────┐
  │ ✏️ Ingresá el *motivo del rechazo* (obligatorio):        │
  └──────────────────────────────────────────────────────────┘
  19:12

──────────────────────────────────────────────────────────────────
✏  Vos > Solapamiento con sprint de cierre de Q3
──────────────────────────────────────────────────────────────────
                                                                Vos
                                   ┌───────────────────────────┐
                                   │  Solapamiento con sprint  │
                                   │  de cierre de Q3          │
                                   └───────────────────────────┘
                                                           19:12

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────────┐
  │ ❌ *Solicitud #5003 RECHAZADA.*                          │
  │ Motivo: _Solapamiento con sprint de cierre de Q3_        │
  │ Se notificó a *Martina López*.                           │
  │                                                          │
  │ 📋 *MENÚ PRINCIPAL*                                      │
  │ ─────────────────────                                    │
  │ 1️⃣  Solicitar vacaciones                                 │
  │ 2️⃣  Aprobar / Rechazar                                   │
  │ 3️⃣  Consultar saldo                                      │
  │ 4️⃣  Ver calendario de equipo                             │
  │ ─────────────────────                                    │
  │ Ingresá el número de opción:                             │
  └──────────────────────────────────────────────────────────┘
  19:12
```

---

### Flujo 3 — Acceso denegado

Número no registrado en la base de datos.

```
  📱 Teléfono > +5490000000000

──────────────────────────────────────────────────────────────────
                                                                Vos
                                              ┌─────────────────┐
                                              │  Hola 👋        │
                                              └─────────────────┘
                                                           19:15

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────────┐
  │ ❌ Acceso denegado.                                      │
  │ Comunicate con el departamento de Recursos Humanos.      │
  └──────────────────────────────────────────────────────────┘
  19:15
```

---

## Arquitectura de módulos

```
main.py
  │
  ├── interfaz.py          Burbujas, colores, animación de escritura
  │     └── base_de_datos.py ──► config.py
  │
  ├── estados.py           Máquina de estados (un handler por nodo BPMN)
  │     └── base_de_datos.py ──► config.py
  │
  └── base_de_datos.py     Acceso a JSON: CRUD de usuarios, solicitudes y sesiones
        └── config.py      Rutas, paleta ANSI, datos semilla
```

| Módulo              | Responsabilidad                                                 |
|---------------------|-----------------------------------------------------------------|
| `main.py`           | Loop de conversación, orquesta los demás módulos               |
| `config.py`         | Rutas de archivos, colores ANSI, datos semilla                  |
| `base_de_datos.py`  | Lectura/escritura JSON, todas las queries por entidad           |
| `interfaz.py`       | Burbujas de chat, barra de título, lista de usuarios            |
| `estados.py`        | Máquina de estados; un handler privado por nodo del flujo BPMN |

### Nodos de la máquina de estados

```
MENU_PRINCIPAL
  │
  ├─[1]─► ESPERANDO_FECHA_INICIO
  │              │
  │        ESPERANDO_FECHA_FIN
  │              │
  │        CONFIRMACION_SOLICITUD
  │              │
  │        ──────┘ (vuelve a MENU_PRINCIPAL)
  │
  ├─[2]─► ESPERANDO_SELECCION_SOLICITUD
  │              │
  │        DETALLE_SOLICITUD
  │         ├─[Aprobar]──────────────────────────────► MENU_PRINCIPAL
  │         └─[Rechazar]─► ESPERANDO_MOTIVO_RECHAZO ─► MENU_PRINCIPAL
  │
  ├─[3]─► (respuesta inmediata, sin cambio de estado)
  │
  └─[4]─► ESPERANDO_PERIODO_CALENDARIO
                 │
           FILTRO_CALENDARIO
            ├─[No]───────────────────────────────────► MENU_PRINCIPAL
            └─[Sí]─► ESPERANDO_NOMBRE_FILTRO ────────► MENU_PRINCIPAL
```

---

## Estructura de archivos

```
bot_vacaciones/
├── main.py              # Punto de entrada y loop de conversación
├── config.py            # Rutas, colores ANSI y datos semilla
├── base_de_datos.py     # Capa de acceso a datos (JSON / CRUD)
├── interfaz.py          # Presentación: burbujas y elementos visuales
├── estados.py           # Máquina de estados: handlers por nodo BPMN
└── db/                  # Creado automáticamente en el primer arranque
    ├── usuarios.json
    ├── solicitudes.json
    └── sesiones.json
```

---

## Esquema de la base de datos JSON

### `db/usuarios.json`

```json
[
  {
    "id_usuario":      1,
    "telefono":        "+5491100000001",
    "nombre_completo": "Carlos Martínez",
    "rol":             "GERENTE",
    "id_manager":      null,
    "dias_totales":    21,
    "dias_usados":     3
  }
]
```

| Campo             | Tipo    | Descripción                                    |
|-------------------|---------|------------------------------------------------|
| `id_usuario`      | int     | Clave primaria                                 |
| `telefono`        | string  | Número de WhatsApp (clave de autenticación)    |
| `nombre_completo` | string  | Nombre y apellido del colaborador              |
| `rol`             | string  | `"EMPLEADO"` o `"GERENTE"`                     |
| `id_manager`      | int/null| ID del jefe directo; null para el top level    |
| `dias_totales`    | int     | Días de vacaciones asignados por año           |
| `dias_usados`     | int     | Días consumidos (se actualiza al aprobar)      |

### `db/solicitudes.json`

```json
[
  {
    "id_solicitud":     5001,
    "id_empleado":      2,
    "fecha_inicio":     "2026-07-15",
    "fecha_fin":        "2026-07-25",
    "dias_solicitados": 8,
    "estado":           "PENDIENTE",
    "motivo_rechazo":   null,
    "fecha_creacion":   "2026-05-25 19:05:00"
  }
]
```

| Campo              | Tipo       | Valores posibles                         |
|--------------------|------------|------------------------------------------|
| `id_solicitud`     | int        | Auto-incremental desde 5001              |
| `id_empleado`      | int (FK)   | Referencia a `usuarios.id_usuario`       |
| `fecha_inicio`     | string ISO | `"AAAA-MM-DD"`                           |
| `fecha_fin`        | string ISO | `"AAAA-MM-DD"`                           |
| `dias_solicitados` | int        | Días hábiles calculados (lun–vie)        |
| `estado`           | string     | `"PENDIENTE"` · `"APROBADA"` · `"RECHAZADA"` |
| `motivo_rechazo`   | string/null| Solo se completa al rechazar             |
| `fecha_creacion`   | string     | Timestamp de la solicitud                |

### `db/sesiones.json`

```json
[
  {
    "id_sesion":          "WA_5491100000002",
    "id_usuario":         2,
    "estado_chat":        "ESPERANDO_FECHA_FIN",
    "datos_temporales":   { "fecha_inicio_raw": "15/07/2026" },
    "ultima_interaccion": "2026-05-25 19:05:00"
  }
]
```

| Campo                | Descripción                                                 |
|----------------------|-------------------------------------------------------------|
| `id_sesion`          | ID único derivado del teléfono (`WA_` + número sin `+`)    |
| `id_usuario`         | Usuario autenticado en esta sesión                          |
| `estado_chat`        | Nodo actual del flujo BPMN                                  |
| `datos_temporales`   | Datos parciales entre pasos (fechas, ID de solicitud, etc.) |
| `ultima_interaccion` | Timestamp del último mensaje (útil para implementar timeout)|

> Las sesiones persisten entre ejecuciones. Si el bot se reinicia en medio de
> un flujo, retoma exactamente desde el mismo estado.
