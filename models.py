from sqlalchemy import (
    Column, Integer, String, Date, Text, ForeignKey, TIMESTAMP, JSON, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# --------------- ENTIDAD: USUARIOS ---------------
class Usuarios(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    telefono = Column(String(20), unique=True, nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    rol = Column(String(20), nullable=False)
    id_manager = Column(Integer, ForeignKey('usuarios.id_usuario'))  # FK
    dias_totales = Column(Integer, nullable=False)
    dias_usados = Column(Integer, nullable=False)

# --------------- ENTIDAD: SOLICITUDES_VACACIONES ---------------
class SolicitudesVacaciones(Base):
    __tablename__ = 'solicitudes_vacaciones'
    id_solicitud = Column(Integer, primary_key=True, autoincrement=True)
    id_empleado = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    dias_solicitados = Column(Integer, nullable=False)
    estado = Column(String(20), nullable=False)            # "PENDIENTE", "APROBADA", "RECHAZADA"
    motivo_rechazo = Column(Text, nullable=True)
    fecha_creacion = Column(TIMESTAMP, nullable=False)

# --------------- ENTIDAD: SESIONES_CHATBOT ---------------
class SesionesChatbot(Base):
    __tablename__ = 'sesiones_chatbot'
    id_sesion = Column(String(50), primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    estado_chat = Column(String(50), nullable=False)
    datos_temporales = Column(JSON, nullable=True)
    ultima_interaccion = Column(TIMESTAMP, nullable=False)