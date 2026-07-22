# 1. Importamos fastapi la herramienta de FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 2. Creamos la instancia (El motor) de nuestra aplicacion
app = FastAPI()

import models
from database import engine

# Esta es la instrucción mágica que crea las tablas en Supabase
models.Base.metadata.create_all(bind=engine)

#3. Congiguramos el CORS (El puente para la comunicacion entre mi front y este back)
#Aqui le dijo a fastAPI que URLS se pueden comunicar con el 
origenes_permitidos = [
  "http://localhost:517",  #Es donde tengo el codigo de react
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origenes_permitidos,
  allow_credentials=True,
  allow_methods=["*"] #Esto permite todos los metodos, get, post, etc..
)


#4. EL MOLDE DE DATOS (modelo pydantic)
#Asi le decimos a python que datos esperar del formulario de REACT
class UsuarioRegistro (BaseModel):
  nombre: str
  correo: str
  password: str


# 5. creamos nuestra primer ruta (Un endpoint)
# El decorador @app.get("/") le dice al servidor que escuche nuestras peticiones enla ruta raiz
@app.get("/")
def leer_raiz():
    # En python usa diccionarios, que solitos se convierten en JSON para react
    return {"mensaje": "Hola mundo, desde ek backend de annya vacio."}

#Segunda ruta para recibir los datos de registro (Aqui se usa post porque estamos enviando informacion y no podiendola a la bd)
@app.post("/registro")
def registrar_usuario(usuario: UsuarioRegistro):
  #Aqui es donde a al siguiente paso voy a conectar con la bd 
  print(f"React acaba de enviar a: {usuario.nombre} con correo {usuario.correo}")

  #Le respondemos al front que todo bien
  return {"mensaje": f"usuario {usuario.nombre} procesado por el back correctamente"}