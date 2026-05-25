
# MANUAL DE USUARIO: GESTIÓN DE VACACIONES VÍA CHATBOT

Este instructivo detalla el funcionamiento, comandos y flujos interactivos de la plataforma automatizada de autoservicio para la gestión de licencias. El sistema cuenta con memoria de estados , adaptando dinámicamente sus respuestas según el rol jerárquico del usuario autenticado en la base de datos de la organización.  

## ACCESO Y AUTENTICACIÓN TRANSVERSAL

El chatbot opera de manera asincrónica y automatizada. No requiere de la instalación de aplicativos adicionales, ya que se integra directamente con la API del canal de mensajería corporativo elegido.

---

  - Primer Contacto: Para iniciar la interacción, el colaborador debe enviar un mensaje de saludo inicial (ej: `Hola`, `Buenas tardes` o `/start`).
  
  - Validación de Identidad: El sistema capturará automáticamente el número de teléfono del remitente y realizará una consulta de persistencia en la base de datos en tiempo real. 

  - Acceso Exitoso: Si el número coincide con los registros del personal, se iniciará la sesión y se desplegará el Menú Principal.

  - Acceso Denegado: Si el número no se encuentra registrado en el sistema, el bot ejecutará el flujo de excepción devolviendo el mensaje: `"Acceso denegado. Por favor, póngase en contacto con el departamento de Recursos Humanos."` El proceso finalizará inmediatamente por motivos de seguridad.
  
  ## COMANDOS Y MENÚ PRINCIPAL
  Una vez superada la fase de autenticación, el bot presentará una interfaz guiada por botones interactivos o comandos numéricos simples (1, 2, 3, 4). Esto evita errores de tipeo y agiliza la navegación por los diferentes andariveles del proceso.  
  
  ### OPCIÓN 1: SOLICITAR VACACIONES (Rol: Empleado)
   Permite iniciar un proceso de punta a punta para la reserva de días de descanso.  Seleccione la opción 1 o pulse el botón `Solicitar vacaciones`. El bot solicitará la Fecha de Inicio en formato estandarizado (Ej: 15/07/2026). Posteriormente, solicitará la Fecha de Fin (Ej: 22/07/2026).

   Validación Automática (Camino Feliz / Infeliz): El sistema procesará los datos contra el backend para comprobar el saldo disponible y descartar solapamientos críticos con otros miembros de la célula de desarrollo. 
   
   Si los datos son erróneos o inválidos: El bot indicará la anomalía (ej: "Formato de fecha incorrecto" o "Supera el saldo disponible") y reiniciará el paso de solicitud.  Si los datos son válidos: Mostrará un resumen de la solicitud con las opciones `[Confirmar]` o `[Cancelar]`. 
   
   Al confirmar, el sistema modificará el estado de la máquina de estados a "PENDIENTE", enviará una notificación automatizada al WhatsApp del Manager asignado y concluirá la operación con el mensaje "Solicitud enviada con éxito".
  
  ### OPCIÓN 2: APROBAR / RECHAZAR (Rol: Manager)
  Módulo restringido exclusivamente para líderes de equipo y gerentes con personal a cargo. Seleccione la opción 2 o pulse `Aprobar / rechazar`. El bot consultará los permisos en el backend. Si el usuario posee rol de empleado común, el sistema disparará la derivación por error: "Sin permisos para acceder a este módulo" y regresará al menú.
  
   Si el rol es válido, el bot listará cronológicamente las solicitudes en estado `"PENDIENTE" `pertenecientes a su equipo de trabajo. El manager deberá seleccionar el ID de la solicitud que desea evaluar. El sistema desplegará el detalle del empleado y proveerá dos acciones directas:
   
   `[Aprobar]`: El bot actualizará el estado de la licencia a `"APROBADA"` en la base de datos y notificará inmediatamente al empleado por chat.
   
   `[Rechazar]`: 
  El bot cambiará temporalmente su estado conversacional para exigir el ingreso obligatorio de un motivo de rechazo por texto. Una vez ingresado, guardará el estado `"RECHAZADA"` junto con la justificación y notificará de forma automatizada al colaborador afectado.

  ### OPCIÓN 3: CONSULTAR SALDO (Todos los roles)
  
  Herramienta de transparencia informativa para la autogestión del personal. Seleccione la opción 3 o pulse Consultar saldo. El bot consumirá de manera dinámica la información alojada en la persistencia del sistema. En breves segundos, enviará un mensaje estructurado con el siguiente resumen de cuenta: 
  
  - Días totales del año: (Días asignados por antigüedad).
  - Días usados: (Días consumidos en periodos anteriores).
  - Días disponibles: (Saldo neto remanente a la fecha).  
  
  Adicionalmente, adjuntará un Historial Reciente detallando los estados de las últimas 3 solicitudes tramitadas en el año en curso.
  
  ### OPCIÓN 4: VER CALENDARIO DE EQUIPO (Todos los roles)
  
  Diseñado para coordinar las licencias operativas y evitar baches de capacidad técnica en equipos grandes de más de 50 personas. Seleccione la opción 4 o pulse Ver calendario.Indique el periodo temporal que desea revisar seleccionando entre las opciones: `[Esta semana], [Mes en curso] o [Próximos 3 meses]`. 

  El bot listará las ausencias programadas y aprobadas en ese rango, detallando Nombre del colaborador, Fecha de inicio, Fecha de fin y Estado de la solicitud.Filtro Avanzado: El sistema le consultará de manera interactiva: `"¿Desea filtrar por una persona en específico?"` 
  
  Seleccionando `[No]`, dará por finalizada la consulta mostrando todo el equipo. 
  
  Seleccionando `[Sí]`, el chatbot aguardará a que escriba el nombre del colaborador para realizar una búsqueda indexada y retornar exclusivamente los resultados coincidentes.