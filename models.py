from sqlalchemy import Column, Integer, String
from database import  Base

# Cremaos una clase que representara la tabla en nuestra bd
class Usuario(Base):
  # Asi se llamara nuestra tabla en Supabase
  __tablename__ = "usuarios"

  #definimos las columnas 
  id = Column(Integer, primary_key=True, index=True)
  nombre = Column(String, index=True)
  # unique=true es para que el correo sea unico 
  correo = Column(String, unique=True, index=True)
  passqord = Column(String)