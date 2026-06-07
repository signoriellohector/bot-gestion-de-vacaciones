# Pruebas de Estrés — Bot de Gestión de Vacaciones

Evidencia de manejo de errores de entrada del usuario, gaps identificados
y propuestas de mejora. Todas las respuestas del bot que aparecen a continuación
son salidas reales capturadas ejecutando `pruebas_estres.py`.

---

## Resumen ejecutivo

| Métrica | Valor |
|---|---|
| Casos de prueba | 19 |
| Pasos totales ejecutados | 79 |
| **PASS** | **79 (100 %)** |
| **FAIL** | **0** |
| Gaps documentados | 1 |
| Mejoras propuestas | 4 |

```
python3 pruebas_estres.py

  ✅ PASS  AUTH-01    (1/1 pasos)   Número de teléfono no registrado
  ✅ PASS  MENU-01    (2/2 pasos)   Opción fuera del rango válido
  ✅ PASS  MENU-02    (2/2 pasos)   Texto libre en el menú
  ✅ PASS  MENU-03    (2/2 pasos)   Empleado accede a módulo de manager
  ✅ PASS  FECHA-01   (3/3 pasos)   Formato AAAA-MM-DD
  ✅ PASS  FECHA-02   (3/3 pasos)   Formato AAAA/MM/DD
  ✅ PASS  FECHA-03   (3/3 pasos)   Texto libre como fecha
  ✅ PASS  FECHA-04   (3/3 pasos)   Día fuera de rango (32/08)
  ✅ PASS  FECHA-05   (3/3 pasos)   Mes fuera de rango (15/13)
  ✅ PASS  FECHA-06   (4/4 pasos)   Fecha fin anterior al inicio
  ✅ PASS  FECHA-07   (4/4 pasos)   Fecha fin igual al inicio
  ✅ PASS  FECHA-08   (3/3 pasos)   [GAP] Inicio en sábado sin advertencia
  ✅ PASS  FECHA-09   (4/4 pasos)   Período supera el saldo disponible
  ✅ PASS  CONF-01    (5/5 pasos)   Respuesta ambigua en confirmación
  ✅ PASS  CONF-02    (5/5 pasos)   El usuario cancela la solicitud
  ✅ PASS  SEL-01     (3/3 pasos)   ID con letras (no numérico)
  ✅ PASS  SEL-02     (3/3 pasos)   ID numérico inexistente
  ✅ PASS  SEL-03     (3/3 pasos)   ID de solicitud ya procesada
  ✅ PASS  SEL-04     (3/3 pasos)   ID con prefijo # aceptado
  ✅ PASS  MOT-01     (5/5 pasos)   Motivo de rechazo muy corto
  ✅ PASS  MOT-02     (5/5 pasos)   Motivo en el límite mínimo exacto
  ✅ PASS  CAL-01     (3/3 pasos)   Período de calendario inválido
  ✅ PASS  CAL-02     (5/5 pasos)   Filtro por nombre sin resultados
  ✅ PASS  EST-01     (2/2 pasos)   Estado desconocido inyectado

  Resultados: 79 PASS  0 FAIL  / 79 pasos totales
  ✅  Todas las pruebas pasaron.
```

---

## Principios generales de manejo de error

Antes de detallar cada caso, tres comportamientos transversales que el bot
cumple en **todos** los caminos de error:

**1. Sin pérdida de estado** — un error nunca descarta el progreso acumulado.
Si el usuario ingresó la fecha de inicio correctamente y falla la fecha de
fin, el bot pide de nuevo solo la fecha de fin; no reinicia todo el flujo.

**2. Retroalimentación con ejemplo** — cada mensaje de error incluye el
formato o valor esperado, para que el usuario corrija sin adivinar.

**3. Persistencia entre reinicios** — si el proceso Python se interrumpe a
mitad de un flujo, la sesión se retoma exactamente desde el mismo estado la
próxima vez que el usuario escribe, porque todo está guardado en `sesiones.json`.

---

## Casos por categoría

---

### 1. Autenticación

#### AUTH-01 — Número de teléfono no registrado

El sistema termina la interacción de forma inmediata y sin revelar
información sobre la estructura interna.

```
  Vos > Hola

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ❌ Acceso denegado.                                  │
  │ Comunicate con el departamento de Recursos Humanos.  │
  └──────────────────────────────────────────────────────┘
```

**Comportamiento:** bloqueo sin información de diagnóstico. El usuario no
sabe si su número no existe o si hay un error de sistema, lo que dificulta
ataques de enumeración.

---

### 2. Menú principal

#### MENU-01 — Opción numérica fuera del rango (5, 0, 99…)

```
  Vos > 5

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ⚠️ Opción no reconocida.                             │
  │                                                      │
  │ 📋 *MENÚ PRINCIPAL*                                  │
  │ ─────────────────────                                │
  │ 1️⃣  Solicitar vacaciones                             │
  │ 2️⃣  Aprobar / Rechazar                               │
  │ 3️⃣  Consultar saldo                                  │
  │ 4️⃣  Ver calendario de equipo                         │
  │ ─────────────────────                                │
  │ Ingresá el número de opción:                         │
  └──────────────────────────────────────────────────────┘
```

#### MENU-02 — Texto libre sin coincidir con ningún comando

```
  Vos > quiero salir

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ⚠️ Opción no reconocida.                             │
  │                                                      │
  │ 📋 *MENÚ PRINCIPAL*  [menú completo...]              │
  └──────────────────────────────────────────────────────┘
```

**Comportamiento:** el mensaje de aviso y el menú se muestran en el mismo
mensaje, sin necesidad de una interacción adicional.

#### MENU-03 — Empleado intenta acceder al módulo restringido (Opción 2)

```
  Vos > 2

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ⛔ *Sin permisos para este módulo.*                  │
  │                                                      │
  │ 📋 *MENÚ PRINCIPAL*  [menú completo...]              │
  └──────────────────────────────────────────────────────┘
```

**Comportamiento:** verificación de rol antes de cualquier consulta de datos.
El empleado no puede listar ni ver solicitudes ajenas.

---

### 3. Fecha de inicio

Todos los formatos erróneos reciben el mismo mensaje, que incluye el formato
correcto y un ejemplo concreto. El estado `ESPERANDO_FECHA_INICIO` no avanza.

| ID | Entrada enviada | Por qué falla |
|---|---|---|
| FECHA-01 | `2026-08-10` | Separador incorrecto (guión) |
| FECHA-02 | `2026/08/10` | Orden de campos invertido |
| FECHA-03 | `la semana próxima` | Texto libre |
| FECHA-04 | `32/08/2026` | Día inexistente |
| FECHA-05 | `15/13/2026` | Mes inexistente |

```
  Vos > 2026-08-10

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ⚠️ Formato incorrecto. Usá DD/MM/AAAA — Ej: 15/07/2026 │
  └──────────────────────────────────────────────────────┘

  Vos > 32/08/2026

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ⚠️ Formato incorrecto. Usá DD/MM/AAAA — Ej: 15/07/2026 │
  └──────────────────────────────────────────────────────┘
```

---

### 4. Fecha de fin

#### FECHA-06 — Fecha de fin anterior a la de inicio

```
  [inicio aceptado: 20/08/2026]

  Vos > 10/08/2026

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ⚠️ La fecha de fin debe ser *posterior* al inicio.   │
  │ Ingresá una nueva *fecha de fin*:                    │
  └──────────────────────────────────────────────────────┘
```

#### FECHA-07 — Fecha de fin igual a la de inicio

```
  [inicio aceptado: 20/08/2026]

  Vos > 20/08/2026

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ⚠️ La fecha de fin debe ser *posterior* al inicio.   │
  │ Ingresá una nueva *fecha de fin*:                    │
  └──────────────────────────────────────────────────────┘
```

**Nota de diseño:** el bot no distingue "igual" de "anterior" en el mensaje.
Ambos casos son semánticamente equivalentes (período de 0 o negativo días).

#### FECHA-08 — `[GAP]` Fecha de inicio en fin de semana

El bot acepta sábado o domingo como fecha de inicio sin advertir al usuario.
El error aparece solo si **también** la fecha de fin cae en fin de semana:

```
  Vos > 01/08/2026   ← sábado

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ✅ Fecha de inicio: *01/08/2026*                     │  ← sin advertencia
  │ Ahora ingresá la *fecha de fin*...                   │
  └──────────────────────────────────────────────────────┘

  Vos > 02/08/2026   ← domingo (el período entero es fin de semana)

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ⚠️ El período no contiene días hábiles.              │  ← error diferido
  │ Ingresá fechas válidas:                              │
  └──────────────────────────────────────────────────────┘
```

Si en cambio el usuario elige fin de semana como inicio pero fecha de fin el
lunes siguiente, el bot acepta y calcula correctamente desde el lunes.
El gap es de **UX**, no de integridad de datos.

> **Propuesta de mejora:** ver sección [Alternativas y mejoras](#alternativas-y-mejoras).

#### FECHA-09 — Período que supera el saldo disponible

El error detalla tanto los días solicitados como los disponibles, permitiendo
al usuario ajustar la fecha de fin sin salir del flujo.

```
  [inicio: 01/09/2026]

  Vos > 30/10/2026   ← 44 días hábiles

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ⚠️ *Supera el saldo disponible.*                     │
  │ Solicitados: 44 días | Disponibles: 16 días          │
  │                                                      │
  │ Ingresá una nueva *fecha de fin*:                    │
  └──────────────────────────────────────────────────────┘
```

---

### 5. Confirmación de solicitud

#### CONF-01 — Respuesta fuera del conjunto válido

El bot repite la pregunta con las opciones explícitas y no avanza ni retrocede.

```
  [resumen mostrado]

  Vos > tal vez

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ Respondé *Confirmar* o *Cancelar*:                   │
  └──────────────────────────────────────────────────────┘
```

#### CONF-02 — El usuario cancela

La cancelación descarta los datos temporales y vuelve al menú en un solo paso.

```
  Vos > cancelar

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ❌ Solicitud cancelada.                              │
  │                                                      │
  │ 📋 *MENÚ PRINCIPAL*  [...]                           │
  └──────────────────────────────────────────────────────┘
```

---

### 6. Selección de solicitud (manager)

#### SEL-01 — ID con letras

```
  Vos > abc

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ⚠️ Ingresá solo el número del ID (ej: 5003):         │
  └──────────────────────────────────────────────────────┘
```

#### SEL-02 — ID numérico inexistente

```
  Vos > 9999

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ⚠️ No existe solicitud con ID #9999.                 │
  │ Ingresá un ID válido:                                │
  └──────────────────────────────────────────────────────┘
```

#### SEL-03 — ID de solicitud ya procesada

El bot indica el estado actual para que el manager entienda por qué no puede
volver a procesarla.

```
  Vos > 5001

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ⚠️ La solicitud #5001 ya fue procesada               │
  │ (Estado: APROBADA).                                  │
  │ Ingresá otro ID:                                     │
  └──────────────────────────────────────────────────────┘
```

#### SEL-04 — ID con prefijo `#` (caso de uso real de WhatsApp)

Un usuario natural podría copiar el ID tal como aparece en el mensaje de
notificación (`#5003`). El bot elimina el `#` y procesa correctamente.

```
  Vos > #5003

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ 📋 *DETALLE — Solicitud #5003*                       │
  │ ─────────────────────                                │
  │ 👤 Empleado:     *Martina López*                     │
  │ 📅 Período:      2026-06-15 → 2026-06-19             │
  │ 📆 Días hábiles: *5*                                 │
  │ 🕐 Creada:       2026-05-25 11:45:00                 │
  └──────────────────────────────────────────────────────┘
```

---

### 7. Motivo de rechazo

#### MOT-01 — Motivo de un solo carácter

```
  Vos > x

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ⚠️ El motivo debe tener al menos 5 caracteres.       │
  │ Ingresalo nuevamente:                                │
  └──────────────────────────────────────────────────────┘
```

#### MOT-02 — Motivo exactamente en el límite mínimo (5 caracteres)

Verifica que el límite sea inclusivo: `len("Vacas") == 5` debe pasar.

```
  Vos > Vacas

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ❌ *Solicitud #5004 RECHAZADA.*                      │
  │ Motivo: _Vacas_                                      │
  │ Se notificó a *Andrés Bonelli*.                      │
  └──────────────────────────────────────────────────────┘
```

**Observación:** 5 caracteres es un mínimo muy bajo en producción.
Ver propuesta MOT-A en la sección siguiente.

---

### 8. Calendario

#### CAL-01 — Opción de período inválida

El bot repite las opciones válidas de forma explícita.

```
  Vos > 4

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ⚠️ Ingresá 1, 2 o 3:                                 │
  │ 1️⃣ Esta semana                                       │
  │ 2️⃣ Mes en curso                                      │
  │ 3️⃣ Próximos 3 meses                                  │
  └──────────────────────────────────────────────────────┘
```

#### CAL-02 — Filtro por nombre sin coincidencias

El bot cierra el flujo, informa el resultado y regresa al menú.

```
  Vos > Juan Pérez

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ⚠️ Sin resultados para *'Juan Pérez'*.               │
  │                                                      │
  │ 📋 *MENÚ PRINCIPAL*  [...]                           │
  └──────────────────────────────────────────────────────┘
```

---

### 9. Máquina de estados

#### EST-01 — Estado desconocido inyectado directamente en `sesiones.json`

Simula corrupción del archivo de persistencia o un deploy que introdujo
nuevos nodos sin migrar sesiones activas.

```python
# El estado "NODO_FANTASMA" no existe en el dispatcher
sesion["estado_chat"] = "NODO_FANTASMA"
guardar_sesion(sesion)
```

```
  Vos > test

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ⚠️ Estado no reconocido. Reiniciando...              │
  │                                                      │
  │ 📋 *MENÚ PRINCIPAL*  [...]                           │
  └──────────────────────────────────────────────────────┘
```

**Comportamiento:** el bot no lanza excepción. Reinicia la sesión al menú
principal en lugar de quedar bloqueado o exponer un traceback.

---

## Alternativas y mejoras

### A — Advertencia cuando la fecha de inicio cae en fin de semana `[GAP FECHA-08]`

**Problema actual:** el bot acepta sábado o domingo como fecha de inicio
sin advertir. El error de "sin días hábiles" solo aparece si la fecha de fin
también cae en fin de semana; si no, el período se calcula silenciosamente
desde el lunes siguiente.

**Impacto:** UX confuso. El empleado podría creer que sus vacaciones empiezan
el sábado cuando en realidad el sistema las contará desde el lunes.

**Implementación sugerida** en `estados.py`, dentro de `_manejar_fecha_inicio`:

```python
from datetime import datetime

NOMBRES_DIA = ["lunes", "martes", "miércoles", "jueves",
               "viernes", "sábado", "domingo"]

def _manejar_fecha_inicio(sesion, datos_temporales, fecha_raw):
    try:
        fecha_dt = datetime.strptime(fecha_raw, "%d/%m/%Y")
    except ValueError:
        return "⚠️ Formato incorrecto. Usá DD/MM/AAAA — Ej: 15/07/2026"

    numero_dia = fecha_dt.weekday()   # 5=sábado, 6=domingo
    if numero_dia >= 5:
        nombre_dia = NOMBRES_DIA[numero_dia]
        return (
            f"⚠️ El {fecha_raw} es {nombre_dia}.\n"
            "Las vacaciones solo pueden iniciarse en días hábiles "
            "(lunes a viernes).\n\n"
            "Ingresá una nueva *fecha de inicio*:"
        )

    datos_temporales["fecha_inicio_raw"] = fecha_raw
    ...
```

**Resultado esperado:**

```
  Vos > 01/08/2026   ← sábado

  Bot Vacaciones
  ┌──────────────────────────────────────────────────────┐
  │ ⚠️ El 01/08/2026 es sábado.                         │
  │ Las vacaciones solo pueden iniciarse en días hábiles │
  │ (lunes a viernes).                                   │
  │                                                      │
  │ Ingresá una nueva *fecha de inicio*:                 │
  └──────────────────────────────────────────────────────┘
```

---

### B — Límite mínimo de motivo de rechazo más restrictivo `[MOT-02]`

**Problema actual:** 5 caracteres permiten motivos sin sentido ("Vacas",
"no ok", "xxxxx"). En producción, un motivo útil debería explicar el impacto
operativo para el empleado.

**Alternativa 1 — Elevar el mínimo a 20 caracteres:**

```python
LONGITUD_MINIMA_MOTIVO = 20
```

**Alternativa 2 — Motivos predefinidos + campo libre opcional:**

```
  Bot: Seleccioná el motivo principal:
  1️⃣  Solapamiento con entrega crítica
  2️⃣  Período de baja cobertura del equipo
  3️⃣  Conflicto con otro colega
  4️⃣  Otro (especificá a continuación)
```

La opción 4 habilitaría el campo de texto libre con el mínimo actual.
Reduce el esfuerzo del manager y estandariza los reportes de RRHH.

---

### C — Derivación a RRHH con contexto `[AUTH-01]`

**Problema actual:** el mensaje de acceso denegado no ofrece ninguna acción
concreta más allá de "contactar a RRHH", sin indicar canal ni qué dato
llevar a la consulta.

**Alternativa:**

```
  ❌ Número no registrado.
  Para solicitar acceso, enviá un correo a rrhh@empresa.com
  con asunto: "Alta de usuario - Bot Vacaciones"
  e indicá tu nombre completo y este número: +5491199990000
```

Esto convierte el mensaje de error en un paso de onboarding y reduce las
consultas manuales al equipo de RRHH.

---

### D — Timeout de sesión inactiva `[EST-01 preventivo]`

**Problema actual:** las sesiones persisten indefinidamente. Un usuario que
abandona un flujo a mitad de camino (por ejemplo, deja el bot esperando la
fecha de fin) retoma ese estado días después, cuando quizás ya no recuerda
qué estaba haciendo.

El campo `ultima_interaccion` ya está guardado en `sesiones.json` y fue
diseñado exactamente para esto. Solo falta usarlo.

**Implementación sugerida** al inicio de `procesar_mensaje`:

```python
TIMEOUT_SESION_HORAS = 2

def _sesion_expirada(sesion: dict) -> bool:
    ultima = datetime.strptime(
        sesion["ultima_interaccion"], "%Y-%m-%d %H:%M:%S"
    )
    return (datetime.now() - ultima).total_seconds() > TIMEOUT_SESION_HORAS * 3600

def procesar_mensaje(id_sesion, mensaje_raw, telefono):
    sesion = obtener_sesion(id_sesion)

    if sesion and _sesion_expirada(sesion):
        sesion["estado_chat"]      = "MENU_PRINCIPAL"
        sesion["datos_temporales"] = {}
        guardar_sesion(sesion)
        return (
            "⏰ Tu sesión expiró por inactividad.\n\n"
            + texto_menu_principal()
        )
    ...
```

**Resultado esperado:** si el usuario retoma la conversación 3 horas después
de haber ingresado solo la fecha de inicio, el bot lo devuelve al menú en
lugar de pedirle la fecha de fin fuera de contexto.

---

## Mapa de cobertura de errores

```
Nodo del flujo              Errores cubiertos
──────────────────────────  ──────────────────────────────────────────────────
Autenticación               Número no registrado
Menú principal              Opción inválida · texto libre · acceso por rol
Fecha de inicio             5 formatos erróneos · días y meses fuera de rango
Fecha de fin                Fin ≤ inicio · período sin hábiles · excede saldo
Confirmación                Respuesta ambigua · cancelación explícita
Selección de solicitud      Texto no numérico · ID inexistente · ya procesada
                            ID con prefijo #
Motivo de rechazo           Texto demasiado corto · límite mínimo inclusivo
Calendario                  Período inválido · filtro sin resultados
Máquina de estados          Estado desconocido (reinicio de seguridad)
```
