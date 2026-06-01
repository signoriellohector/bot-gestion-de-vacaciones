from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from models import Base, Usuarios, SolicitudesVacaciones, SesionesChatbot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
import json

engine = create_engine('sqlite:///vacaciones.db')
Base.metadata.create_all(engine)
SessionDB = sessionmaker(bind=engine)
app = Flask(__name__)

def get_usuario(telefono):
    session = SessionDB()
    user = session.query(Usuarios).filter_by(telefono=telefono).first()
    session.close()
    return user

def get_sesion(user_id):
    session = SessionDB()
    sesion = session.query(SesionesChatbot).filter_by(id_usuario=user_id).first()
    session.close()
    return sesion

def save_or_update_sesion(sid, user_id, estado_chat, datos_temporales):
    # datos_temporales es un dict
    session = SessionDB()
    sesion = session.query(SesionesChatbot).filter_by(id_sesion=sid).first()
    now = datetime.now()
    if sesion:
        sesion.estado_chat = estado_chat
        sesion.datos_temporales = datos_temporales
        sesion.ultima_interaccion = now
    else:
        sesion = SesionesChatbot(
            id_sesion=sid,
            id_usuario=user_id,
            estado_chat=estado_chat,
            datos_temporales=datos_temporales,
            ultima_interaccion=now
        )
        session.add(sesion)
    session.commit()
    session.close()

def borrar_sesion(sid):
    session = SessionDB()
    sesion = session.query(SesionesChatbot).filter_by(id_sesion=sid).first()
    if sesion:
        session.delete(sesion)
        session.commit()
    session.close()


@app.route("/webhook", methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')
    telefono = from_number.replace('whatsapp:', '')
    sid = from_number  # usamos el "from" whatsapp como id sesion
    resp = MessagingResponse()
    session = SessionDB()
    user = session.query(Usuarios).filter_by(telefono=telefono).first()

    if not user:
        resp.message("Acceso denegado. Su número no está registrado. Contacte a RRHH.")
        return str(resp)

    sesion = session.query(SesionesChatbot).filter_by(id_sesion=sid).first()
    estado_actual = sesion.estado_chat if sesion else None
    datos_tmp = sesion.datos_temporales if sesion else {}

    # MENÚ PRINCIPAL
    if estado_actual is None or incoming_msg.lower() in ['menu', 'hola', 'buenas', '/start']:
        respuesta = (
            f"Hola {user.nombre_completo} 👋\n"
            f"¿Qué desea hacer?\n"
            "1. Consultar saldo\n"
            "2. Solicitar vacaciones\n"
            "Escriba 1 o 2."
        )
        save_or_update_sesion(sid, user.id_usuario, "MENU_PRINCIPAL", {})
        resp.message(respuesta)
        session.close()
        return str(resp)

    # CONSULTAR SALDO
    if estado_actual == "MENU_PRINCIPAL" and incoming_msg == "1":
        disponibles = user.dias_totales - user.dias_usados
        resp.message(f"Saldo:\n- Totales: {user.dias_totales}\n- Usados: {user.dias_usados}\n- Disponibles: {disponibles}")
        borrar_sesion(sid)
        session.close()
        return str(resp)

    # SOLICITAR VACACIONES - INICIO FLUJO
    if estado_actual == "MENU_PRINCIPAL" and incoming_msg == "2":
        resp.message("Ingrese la fecha de INICIO de sus vacaciones (YYYY-MM-DD):")
        save_or_update_sesion(sid, user.id_usuario, "ESPERANDO_FECHA_INICIO", {})
        session.close()
        return str(resp)

    # Espera FECHA INICIO vacaciones
    if estado_actual == "ESPERANDO_FECHA_INICIO":
        try:
            fecha_inicio = datetime.strptime(incoming_msg, "%Y-%m-%d").date()
            datos_tmp = {"fecha_inicio": incoming_msg}
            resp.message("Ahora ingrese la fecha de FIN de sus vacaciones (YYYY-MM-DD):")
            save_or_update_sesion(sid, user.id_usuario, "ESPERANDO_FECHA_FIN", datos_tmp)
        except Exception:
            resp.message("Formato inválido. Ingrese la fecha de inicio en formato YYYY-MM-DD.")
        session.close()
        return str(resp)

    # Espera FECHA FIN vacaciones
    if estado_actual == "ESPERANDO_FECHA_FIN":
        fecha_inicio_str = datos_tmp.get("fecha_inicio")
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
            fecha_fin = datetime.strptime(incoming_msg, "%Y-%m-%d").date()
            dias = (fecha_fin - fecha_inicio).days + 1
            if dias <= 0:
                resp.message("Error: la fecha de fin debe ser posterior a la de inicio.")
                session.close()
                return str(resp)
            saldo_disponible = user.dias_totales - user.dias_usados
            if dias > saldo_disponible:
                resp.message(f"Saldo insuficiente. Te quedan {saldo_disponible} días.")
                borrar_sesion(sid)
                session.close()
                return str(resp)
            # Guardamos solicitud
            nueva = SolicitudesVacaciones(
                id_empleado=user.id_usuario,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                dias_solicitados=dias,
                estado="PENDIENTE",
                fecha_creacion=datetime.now()
            )
            session.add(nueva)
            session.commit()
            resp.message("¡Solicitud enviada! Queda pendiente de aprobación. Escriba 'menu' para más opciones.")
            borrar_sesion(sid)
        except Exception:
            resp.message("Formato inválido. Ingrese la fecha de fin en formato YYYY-MM-DD.")
        session.close()
        return str(resp)

    resp.message("Opción no reconocida. Escriba 'menu' para ver opciones.")
    session.close()
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)