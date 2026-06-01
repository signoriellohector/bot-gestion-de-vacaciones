from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from models import Base, Usuarios, SolicitudesVacaciones
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date

# Configuracion DB SQLite según modelo
engine = create_engine('sqlite:///vacaciones.db')
Base.metadata.create_all(engine)
SessionDB = sessionmaker(bind=engine)

app = Flask(__name__)

# Utilidad para obtener usuario autenticado por teléfono de WhatsApp
def get_usuario(telefono):
    session = SessionDB()
    user = session.query(Usuarios).filter_by(telefono=telefono).first()
    session.close()
    return user

@app.route("/webhook", methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')
    # El formato de from_number que envía WhatsApp / Twilio es: 'whatsapp:+549...'
    telefono = from_number.replace('whatsapp:', '')
    resp = MessagingResponse()
    session = SessionDB()
    user = get_usuario(telefono)

    if not user:
        resp.message("Acceso denegado. Su número no está registrado. Contacte a RRHH.")
        return str(resp)
        
    # Flujos muy simples
    if incoming_msg.lower() in ['menu', 'hola', 'buenas', 'opciones', '/start']:
        respuesta = (
            f"Hola {user.nombre_completo} 👋\n"
            f"¿Qué desea hacer?\n"
            "1. Consultar saldo\n"
            "2. Solicitar vacaciones\n"
            "Responda con el número de opción."
        )
        resp.message(respuesta)
    elif incoming_msg == '1':
        disponibles = user.dias_totales - user.dias_usados
        resp.message(f"Saldo:\n- Totales: {user.dias_totales}\n- Usados: {user.dias_usados}\n- Disponibles: {disponibles}")
    elif incoming_msg == '2':
        resp.message("Por favor, indique la fecha de INICIO de sus vacaciones (YYYY-MM-DD):")
        session.close()
        # Usar una sesión real (tabla SESIONES_CHATBOT) para guardar el estado entre mensajes en producción
    elif len(incoming_msg) == 10 and incoming_msg[4] == '-':  # YYYY-MM-DD probable formato de fecha
        # Intento capturar solicitud básica:
        # Buscar si tiene una sesión de vacaciones abierta, si no, pide fecha fin.

        resp.message("¿Hasta qué fecha desea sus vacaciones? Envíe usando YYYY-MM-DD.")
    elif len(incoming_msg) == 10 and incoming_msg[4] == '-' and context_user_wants_to_end(user):
        # Ahora debería guardar la solicitud.
        fecha_inicio = context_get_fecha_inicio(user)
        fecha_fin = incoming_msg
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            dias = (fecha_fin_dt - fecha_inicio_dt).days + 1
            saldo_disp = user.dias_totales - user.dias_usados
            if dias > saldo_disp or dias <= 0:
                msg = "Error: el rango solicitado no es válido o excede su saldo."
            else:
                nueva = SolicitudesVacaciones(
                    id_empleado=user.id_usuario,
                    fecha_inicio=fecha_inicio_dt,
                    fecha_fin=fecha_fin_dt,
                    dias_solicitados=dias,
                    estado="PENDIENTE",
                    fecha_creacion=datetime.now()
                )
                session.add(nueva)
                session.commit()
                msg = "¡Solicitud enviada! Queda pendiente de aprobación. Gracias."
            resp.message(msg)
        except Exception:
            resp.message("Formato de fecha inválido. Use YYYY-MM-DD.")
    else:
        resp.message("Opción no reconocida. Escriba 'menu' para reiniciar opciones.")
    session.close()
    return str(resp)



if __name__ == "__main__":
    app.run(port=5000, debug=True)
