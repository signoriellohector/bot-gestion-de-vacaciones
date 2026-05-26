from sqlalchemy import create_engine
from models_v1 import Base

# Crear DB SQLite (puedes ajustar a PostgreSQL, MySQL, etc)
engine = create_engine('sqlite:///vacaciones_v1.db')
Base.metadata.create_all(engine)
print("DB y tablas creadas con el modelo original (v1).")