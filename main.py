# 1. Importamos fastapi la herramienta de FastAPI
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from seguridad import obtener_hash_password

# Importamos lo que creamos para la base de datos
import models
from database import engine, get_bd

# 2. Creamos la instancia (El motor) de nuestra aplicacion
app = FastAPI()

# Esta es la instrucción mágica que crea las tablas en Supabase
models.Base.metadata.create_all(bind=engine)

#3. Congiguramos el CORS (El puente para la comunicacion entre mi front y este back)
#Aqui le dijo a fastAPI que URLS se pueden comunicar con el 
origenes_permitidos = [
  "http://localhost:5173",  #Es donde tengo el codigo de react
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origenes_permitidos,
  allow_credentials=True,
  allow_methods=["*"], #Esto permite todos los metodos, get, post, etc..
  allow_headers=["*"]
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
# modificare esta ruta para que ahora envie los datos a la bd y no solo los muestre en la consola 
@app.post("/registro")
def registrar_usuario(usuario: UsuarioRegistro, db: Session = Depends(get_bd)):


   #El primer paso sera verificar si el correo ya existe en la bd
   # Le didemos a sqlalchemy que busque a alguien con el correo en nuestra bd 
   usuario_existe = db.query(models.Usuario).filter(models.Usuario.correo == usuario.correo).first()

   if usuario_existe:
      #Si ya existe le mandamos un mensaje de error 400 a react 
      raise HTTPException(status_code=400, detail="Este correo ya esta registrado")

   nuevo_usuario = models.Usuario(
      nombre = usuario.nombre,
      correo = usuario.correo,
      #aqui la contraseña esta mal guardada pero despues la cambiare 
      password = obtener_hash_password(usuario.password)
   )

   # el ulgtimo paso es guardarlo en supabase 
   db.add(nuevo_usuario) #Aqui agregamos la variable al asesion
   db.commit() # Guardamos la info con el commit
   db.refresh(nuevo_usuario) # Actualozamos la variable con el ID que le asigno Supabase

   return{"mensaje": f"Exito cliente {nuevo_usuario.nombre} registrado en la nube."}