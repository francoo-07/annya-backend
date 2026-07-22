from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base 
import os
from dotenv import load_dotenv


# 1. Carga las variables de .env
load_dotenv()

# 2. aqui lee la URL que agrege en .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 3. Aqui (Engine) funciona como el motor de la conexion con supabase pues es el encargado de establecerla
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 4. La sesion es como una pestaña para que podamos realizar consultas a la bd
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. La variable base es la que guardara todas las tablas e info de nuestra bd 
Base = declarative_base()

# 6. Esta funcion nos sirve para obtener nuestra bd en nuestras rutas 

def get_bd():
  db = SessionLocal()
  try:
    yield db 
  finally:
    db.close()