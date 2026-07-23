from passlib.context import CryptContext

# Le decimos a python que utilice el algoritmo
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#nuestra funcion para encriptar las contraseñas 
def obtener_hash_password(password: str):
  return pwd_context.hash(password)