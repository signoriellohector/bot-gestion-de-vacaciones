# Bot de Gestión de Vacaciones vía WhatsApp

Este es un bot conversacional simple para la gestión de solicitudes de vacaciones, con autenticación por número de WhatsApp, persistencia de base de datos y gestión de sesiones conversacionales multiusuario (**flujos asincrónicos**).  
**Tecnologías:** Python 3, Flask, SQLAlchemy, Twilio WhatsApp API  
**Modelo de datos:** fiel al diccionario de datos provisto.

---

## 🚦 Prerrequisitos

1. **Python 3.8+** instalado (recomendado: venv virtual)
2. **Cuenta gratuita en [Twilio](https://www.twilio.com/try-twilio)**
3. **Twilio Sandbox para WhatsApp** configurado ([guía oficial](https://www.twilio.com/docs/whatsapp/sandbox))
4. **Paquetes de Python**:
    - Flask
    - SQLAlchemy
    - twilio

Puedes instalarlos así:  
```sh
pip install flask sqlalchemy twilio
```

---

## ⚡ Instalación y configuración básica

1. **Clona o descarga el repositorio** en tu máquina local.
2. **Configura la base de datos**:
    - El bot usa SQLite por defecto para pruebas. Los modelos y tablas se crearán automáticamente al correr el bot por primera vez.

3. **Crea usuarios de prueba** en la base de datos:
    - Puedes crear un script sencillo usando SQLAlchemy o cargar registros manualmente con herramientas como `sqlitebrowser`.

    ```python
    # Script ejemplo para agregar usuarios iniciales (run once)
    from models import Base, Usuarios
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///vacaciones.db')
    Base.metadata.create_all(engine)
    SessionDB = sessionmaker(bind=engine)
    session = SessionDB()

    u1 = Usuarios(
        telefono='+549xxxxxxxxxx',
        nombre_completo='Ejemplo Empleado',
        rol='EMPLEADO',
        id_manager=None,
        dias_totales=21,
        dias_usados=5
    )
    u2 = Usuarios(
        telefono='+549yyyyyyyyyy',
        nombre_completo='Ejemplo Gerente',
        rol='GERENTE',
        id_manager=None,
        dias_totales=25,
        dias_usados=1
    )
    session.add_all([u1, u2])
    session.commit()
    session.close()
    ```

    - Cambia los teléfonos a los reales de WhatsApp con los que vas a probar.

4. **Configura Twilio Sandbox:**
    - Entra a [Twilio Console → Messaging → Try it Out → Send a WhatsApp message](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp).
    - Sigue los pasos para vincular tu WhatsApp al sandbox (añade el número a tus contactos y envía el código join que Twilio te indique).
    - Ve a la pestaña **Sandbox settings** y encuentra la URL del webhook entrante.

5. **Ejecuta el bot:**  
    ```sh
    python whatsapp_bot_con_sesion.py
    ```
    - Esto iniciará el servidor Flask en `http://localhost:5000/webhook`

6. **Expone temporalmente tu localhost a internet:**  
    (Twilio debe poder enviar mensajes webhooks a tu máquina local)
    - Usar [ngrok](https://ngrok.com/download):
    ```sh
    ngrok http 5000
    ```
    - Copia la "Forwarding" HTTPS URL, por ejemplo, `https://abcd1234.ngrok.io/webhook`
    - Pega esa URL en la **configuración del sandbox de Twilio** como "WHEN A MESSAGE COMES IN".

---

## 🎬 ¿Cómo usarlo?

1. Desde tu WhatsApp personal, envía cualquier mensaje al número del Sandbox de Twilio (asegúrate de haber vinculado tu teléfono).
2. Escribe `menu` o cualquier saludo y sigue el flujo del bot:
    - **Opción 1:** Consultar saldo de vacaciones.
    - **Opción 2:** Ingresar una solicitud de vacaciones (el bot guía paso a paso, pide fechas, valida saldo y registra la solicitud).

---

## 📂 Estructura de Archivos

- `models.py` – Modelos de datos SQLAlchemy.
- `whatsapp_bot.py` – Lógica principal del bot Flask+Twilio+SQLAlchemy.
- `README.md` – Este instructivo.
- _(Opcional)_ `crear_usuarios.py` – Script para insertar usuarios de prueba.

---

## 🧠 Notas importantes

- **Persistencia total:** El bot recuerda en qué punto está cada usuario gracias a la tabla `sesiones_chatbot`.
- **Ejemplo mínimo:** El menú principal y el flujo de solicitud de vacaciones están operativos. Puedes expandir lógicamente el código para sumar aprobaciones de gerente, historial de solicitudes, cancelaciones, etc.
- **WhatsApp requiere números reales:** Usa exactamente el formato `+549xxxxxx` usado al registrar cada usuario.
- **Si cambias a PostgreSQL/MySQL**, solo actualiza la línea de `create_engine(...)` en el código.

---

## 💡 Troubleshooting

- Si no recibes respuestas en WhatsApp:
    - Verifica que tu teléfono esté en la base de datos.
    - Chequea el webhook de Twilio.
    - Confirma que Flask esté corriendo y ngrok esté activo.
- Si cortas el servidor por mucho tiempo, la sesión de WhatsApp puede vencer y deberás reiniciar el flujo escribiendo `menu`.

---

## 📚 Créditos & Licencia

Desarrollado como ejemplo educativo para la **Tecnicatura Universitaria en Programación**, adaptado a la operatoria real de bots conversacionales para RRHH.

---