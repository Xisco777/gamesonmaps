#from BBDD import DatabaseManager
from Usuarios import Usuario
from Fecha import Fecha
from Parcela import Parcela
from Tienda import Tienda
from Formulas import * 
import threading
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect,  Depends, status,HTTPException
from fastapi.staticfiles import StaticFiles
from BBDDMongodb import DatabaseManager
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import random
from typing import List

from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
import time



maximoRoboCasa=30000
minimoRoboCasa=4000
cantidadMultaParcela=5000
cantidadMultaTienda=5000
cantidadMultaRoboParcela=15000
cantidadMultaRoboTienda=15000

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 20
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b"

app = FastAPI() 
app.mount("/static",StaticFiles(directory="static"), name="static")
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

# Configurar las opciones CORS
origins = [
    "*",   # Agrega aquí el dominio desde el cual haces la solicitud
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ano=2023
mes=8

store = [] 

produccion = {
    "tipo": str,
    "numero": int,
}

usuario_websocket = {
    "IDMessage":str,
    "dinero": float,
    "ano": int,
    "mes": str,
}

listaUsuarios=[]
parcelas= [{"objeto": [],
        "name": "",
        "precio": 0,
        "tamano": 0}]
usuario_token = {
    "username": "Xisco",
    "full_name": "Xisco",
    "email": "fprats",
    "disabled": False,
}
mensajes= []
mensajesOfertaAceRech= [{
        "IDMessage":"",
        "mensaje": "",
        "usuarioRival": "",
        "usuario":"",
        "nombreciudad":"",
        "lugar":"",
        "aceptada":False,
        }]  # mensaje cambiar a array



class ConnectionManager:
    def __init__(self):
        self.active_connections: List[dict] = []

    async def connect(self, websocket, clientid):
        await websocket.accept()
        self.active_connections.append({"websocket": websocket, "clientid": clientid})

    def disconnect(self, websocket):
        connection = next((conn for conn in self.active_connections if conn["websocket"] == websocket), None)
        if connection:
            self.active_connections.remove(connection)

    async def broadcast(self, message):
        for connection in self.active_connections:
            await connection["websocket"].send_text(message)

    async def send_personal_message(self, message, websocket):
        connection = next((conn for conn in self.active_connections if conn["websocket"] == websocket), None)
        if connection:
            await connection["websocket"].send_text(message)


async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        usuario_token["username"]=username
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return usuario_token


async def current_user(user: usuario_token = Depends(auth_user)):
    if user.get("disable"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user


def obtenerToken(user):
    return {"access_token": jwt.encode({"sub": user["username"],"exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}
  

managerWebsockets = ConnectionManager()

# pathBBDD="mongodb+srv://fpratsquilez:GTdbIFamKljeyUvs@worldmanagergame.k3rozlq.mongodb.net/?retryWrites=true&w=majority"
pathBBDD="mongodb+srv://fpratsquilez:GTdbIFamKljeyUvs@worldmanagergame.k3rozlq.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"
db_manager = DatabaseManager(pathBBDD)

fecha=Fecha(ano,mes)

def cargarUsuarios():
    
    for Datosuser in db_manager.GetUsuarios():
        usuario_objeto=Usuario(nombre=Datosuser["nombre"],bbdd=db_manager)
        for indexciudad, ciudad in enumerate(Datosuser["listaciudades"]):
            usuario_objeto.crear_ciudad(nombreciudad=ciudad["nombre"],bbdd=db_manager)

            for indextiendas, tienda in enumerate(ciudad["listatiendas"]):
                usuario_objeto.comprar_tienda(nombreciudad=ciudad["nombre"],nombretienda=tienda["nombre"],bbdd=db_manager)
                
                for indexproductos, producto in enumerate(tienda["arrayProductos"]):
                    usuario_objeto.modificar_producto(indexproductos, ciudad["nombre"],tienda["nombre"],producto["tipo"])
                
                for indexempleadostiendas, empleado in enumerate(tienda["arrayEmpleados"]):
                    usuario_objeto.contratarempleado(nombreciudad=ciudad["nombre"],lugar=tienda["nombre"],nombreempleado=empleado["nombre"],bbdd=db_manager)
                    usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].listaempleados[indexempleadostiendas].nombre=empleado["nombre"]            
                    usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].listaempleados[indexempleadostiendas].precio=empleado["precio"]  
                    usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].listaempleados[indexempleadostiendas].comunicacion=empleado["comunicacion"]
                    usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].listaempleados[indexempleadostiendas].estudios=empleado["estudios"]
                    usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].listaempleados[indexempleadostiendas].fuerza=empleado["fuerza"]
                    usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].listaempleados[indexempleadostiendas].liderazgo=empleado["liderazgo"]

                usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].nombre=tienda["nombre"]
                usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].tamaño=tienda["tamaño"]
                usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].precio=tienda["precio"]  
                usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].numeroEmpleados=tienda["numeroEmpleados"]
                usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].numeroMaximoEmpleados=tienda["numeroMaximoEmpleados"]
                usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].indiceproduccionempleados=tienda["indiceproduccionempleados"]
                usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].indiceVariedadProductos=tienda["indiceVariedadProductos"]
                usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].ciudadtienda=tienda["ciudadtienda"]
                usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].indiceproductividadempleados=tienda["indiceproductividadempleados"]
                usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].seguridad=tienda["seguridad"]
                usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].prestigio=tienda["prestigio"]
            
            for indexParcelas, parcela in enumerate(ciudad["listaparcelas"]):
                usuario_objeto.comprar_parcela(nombreciudad=ciudad["nombre"],nombreparcela=parcela["nombre"],bbdd=db_manager)
                
                for indexplantacion, plantacion in enumerate(parcela["listaplantacion"]):
                    usuario_objeto.modificar_plantacion(indice=indexplantacion,nombreciudad=ciudad["nombre"],nombreparcela=parcela["nombre"],tipoplantacion=plantacion["tipo"],bbdd=db_manager)
                    usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].listaplantacion[indexplantacion].factormultiplicacion=plantacion["factormultiplicacion"]
                    usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].listaplantacion[indexplantacion].produccionmes=plantacion["produccionmes"]
                    usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].listaplantacion[indexplantacion].urlicono=plantacion["urlicono"]



                for indexempleadosparcela, empleado in enumerate(parcela["listaempleados"]):
                    usuario_objeto.contratarempleado(nombreciudad=ciudad["nombre"],lugar=parcela["nombre"],nombreempleado=empleado["nombre"],bbdd=db_manager)
                    usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].listaempleados[indexempleadosparcela].nombre=empleado["nombre"]          
                    usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].listaempleados[indexempleadosparcela].precio=empleado["precio"]  
                    usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].listaempleados[indexempleadosparcela].comunicacion=empleado["comunicacion"]
                    usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].listaempleados[indexempleadosparcela].estudios=empleado["estudios"]
                    usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].listaempleados[indexempleadosparcela].fuerza=empleado["fuerza"]
                    usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].listaempleados[indexempleadosparcela].liderazgo=empleado["liderazgo"]

                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].nombre=parcela["nombre"]
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].tamaño=parcela["tamaño"]
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].precio=parcela["precio"]
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].numeroEmpleados=parcela["numeroEmpleados"]
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].numeroMaximoEmpleados=parcela["numeroMaximoEmpleados"]
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].indiceproduccionempleados=parcela["indiceproduccionempleados"]
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].factorMultiplicacionProducto=parcela["factorMultiplicacionProducto"]
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].calidadterreno=parcela["calidadterreno"]
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].ciudadParcela=parcela["ciudadParcela"]
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].indiceproductividadempleados=parcela["indiceproductividadempleados"]
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].seguridad=parcela["seguridad"]
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].maximaSeguridad=parcela["maximaSeguridad"]    
            ciudadCasa= ciudad["casa"]
            if ciudadCasa != "":
                usuario_objeto.comprar_casa(nombreciudad=ciudad["nombre"],nombrecasa=ciudadCasa["nombre"],bbdd=db_manager)
                usuario_objeto.listaciudades[indexciudad].casa.precio=ciudadCasa["precio"]
                usuario_objeto.listaciudades[indexciudad].casa.prestigio=ciudadCasa["prestigio"]
            
            usuario_objeto.listaciudades[indexciudad].idioma_principal=ciudad["idioma_principal"]
            usuario_objeto.listaciudades[indexciudad].poblacion=ciudad["poblacion"]
            usuario_objeto.listaciudades[indexciudad].factorMultiplicacionProducto=ciudad["factorMultiplicacionProducto"]
            usuario_objeto.listaciudades[indexciudad].prestigioCasa=ciudad["prestigioCasa"]

        usuario_objeto.prestigio=Datosuser["prestigio"]
        usuario_objeto.dinero=Datosuser["dinero"]
        usuario_objeto.almacen=Datosuser["almacen"]
        usuario_objeto.id=str(Datosuser["_id"])
        usuario_objeto.mostrar_informacion()
        listaUsuarios.append(usuario_objeto)
    return


def cargarUsuario(Datosuser):
    usuario_objeto=Usuario(nombre=Datosuser["nombre"],bbdd=db_manager)
    for indexciudad, ciudad in enumerate(Datosuser["listaciudades"]):
        usuario_objeto.crear_ciudad(nombreciudad=ciudad["nombre"],bbdd=db_manager)

        for indextiendas, tienda in enumerate(ciudad["listatiendas"]):
            usuario_objeto.comprar_tienda(nombreciudad=ciudad["nombre"],nombretienda=tienda["nombre"],bbdd=db_manager)
            
            for indexproductos, producto in enumerate(tienda["arrayProductos"]):
                    usuario_objeto.modificar_producto(indexproductos, ciudad["nombre"],tienda["nombre"],producto["tipo"])
            
            for indexempleadostiendas, empleado in enumerate(tienda["arrayEmpleados"]):
                usuario_objeto.contratarempleado(nombreciudad=ciudad["nombre"],lugar=tienda["nombre"],nombreempleado=empleado["nombre"],bbdd=db_manager)
                usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].listaempleados[indexempleadostiendas].nombre=empleado["nombre"]            
                usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].listaempleados[indexempleadostiendas].precio=empleado["precio"]  
                usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].listaempleados[indexempleadostiendas].comunicacion=empleado["comunicacion"]
                usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].listaempleados[indexempleadostiendas].estudios=empleado["estudios"]
                usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].listaempleados[indexempleadostiendas].fuerza=empleado["fuerza"]
                usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].listaempleados[indexempleadostiendas].liderazgo=empleado["liderazgo"]

            usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].nombre=tienda["nombre"]
            usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].tamaño=tienda["tamaño"]
            usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].precio=tienda["precio"]
            usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].numeroEmpleados=tienda["numeroEmpleados"]
            usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].numeroMaximoEmpleados=tienda["numeroMaximoEmpleados"]
            usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].indiceproduccionempleados=tienda["indiceproduccionempleados"]
            usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].indiceVariedadProductos=tienda["indiceVariedadProductos"]
            usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].ciudadtienda=tienda["ciudadtienda"]
            usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].indiceproductividadempleados=tienda["indiceproductividadempleados"]
            usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].seguridad=tienda["seguridad"]
            usuario_objeto.listaciudades[indexciudad].listatiendas[indextiendas].prestigio=tienda["prestigio"]
        
        for indexParcelas, parcela in enumerate(ciudad["listaparcelas"]):
            usuario_objeto.comprar_parcela(nombreciudad=ciudad["nombre"],nombreparcela=parcela["nombre"],bbdd=db_manager)
            
            for indexplantacion, plantacion in enumerate(parcela["listaplantacion"]):
                usuario_objeto.modificar_plantacion(indice=indexplantacion,nombreciudad=ciudad["nombre"],nombreparcela=parcela["nombre"],tipoplantacion=plantacion["tipo"],bbdd=db_manager)
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].listaplantacion[indexplantacion].factormultiplicacion=plantacion["factormultiplicacion"]
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].listaplantacion[indexplantacion].produccionmes=plantacion["produccionmes"]
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].listaplantacion[indexplantacion].urlicono=plantacion["urlicono"]



            for indexempleadosparcela, empleado in enumerate(parcela["listaempleados"]):
                usuario_objeto.contratarempleado(nombreciudad=ciudad["nombre"],lugar=parcela["nombre"],nombreempleado=empleado["nombre"],bbdd=db_manager)
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].listaempleados[indexempleadosparcela].nombre=empleado["nombre"]          
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].listaempleados[indexempleadosparcela].precio=empleado["precio"]  
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].listaempleados[indexempleadosparcela].comunicacion=empleado["comunicacion"]
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].listaempleados[indexempleadosparcela].estudios=empleado["estudios"]
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].listaempleados[indexempleadosparcela].fuerza=empleado["fuerza"]
                usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].listaempleados[indexempleadosparcela].liderazgo=empleado["liderazgo"]

            usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].nombre=parcela["nombre"]
            usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].tamaño=parcela["tamaño"]
            usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].precio=parcela["precio"]
            usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].numeroEmpleados=parcela["numeroEmpleados"]
            usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].numeroMaximoEmpleados=parcela["numeroMaximoEmpleados"]
            usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].indiceproduccionempleados=parcela["indiceproduccionempleados"]
            usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].factorMultiplicacionProducto=parcela["factorMultiplicacionProducto"]
            usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].calidadterreno=parcela["calidadterreno"]
            usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].ciudadParcela=parcela["ciudadParcela"]
            usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].indiceproductividadempleados=parcela["indiceproductividadempleados"]
            usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].seguridad=parcela["seguridad"]
            usuario_objeto.listaciudades[indexciudad].listaparcelas[indexParcelas].maximaSeguridad=parcela["maximaSeguridad"]    
        ciudadCasa= ciudad["casa"]
        if ciudadCasa != "":
            usuario_objeto.comprar_casa(nombreciudad=ciudad["nombre"],nombrecasa=ciudadCasa["nombre"],bbdd=db_manager)
            usuario_objeto.listaciudades[indexciudad].casa.precio=ciudadCasa["precio"]
            usuario_objeto.listaciudades[indexciudad].casa.prestigio=ciudadCasa["prestigio"]
        
        usuario_objeto.listaciudades[indexciudad].idioma_principal=ciudad["idioma_principal"]
        usuario_objeto.listaciudades[indexciudad].poblacion=ciudad["poblacion"]
        usuario_objeto.listaciudades[indexciudad].factorMultiplicacionProducto=ciudad["factorMultiplicacionProducto"]
        usuario_objeto.listaciudades[indexciudad].prestigioCasa=ciudad["prestigioCasa"]

    usuario_objeto.prestigio=Datosuser["prestigio"]
    usuario_objeto.dinero=Datosuser["dinero"]
    usuario_objeto.almacen=Datosuser["almacen"]
    usuario_objeto.id=str(Datosuser["_id"])
    usuario_objeto.mostrar_informacion()
    listaUsuarios.append(usuario_objeto)
    return



async def periodic_broadcast():

    while True:
        await asyncio.sleep(20)  # Espera 20 segundos
        # Registra el tiempo de inicio
        inicio = time.time()
        if fecha.stop==False:
            for usuario in listaUsuarios:
                usuario_websocket["IDMessage"]="DatosMensuales"
                usuario_websocket["ano"]=fecha.ano
                if fecha.mes == 1:
                    usuario_websocket["mes"]="Ene"
                if fecha.mes == 2:
                    usuario_websocket["mes"]="Feb"
                if fecha.mes == 3:
                    usuario_websocket["mes"]="Mar"
                if fecha.mes == 4:
                    usuario_websocket["mes"]="Abr"
                if fecha.mes == 5:
                    usuario_websocket["mes"]="May"
                if fecha.mes == 6:
                    usuario_websocket["mes"]="Jun"
                if fecha.mes == 7:
                    usuario_websocket["mes"]="Jul"
                if fecha.mes == 8:
                    usuario_websocket["mes"]="Ago"
                if fecha.mes == 9:
                    usuario_websocket["mes"]="Sep"
                if fecha.mes == 10:
                    usuario_websocket["mes"]="Oct"
                if fecha.mes == 11:
                    usuario_websocket["mes"]="Nov"
                if fecha.mes == 12:
                    usuario_websocket["mes"]="Dic"
                usuario_websocket["dinero"]=usuario.dinero
                usuario_websocket["almacen"]=usuario.almacen
                usuario_websocket["prestigio"]=usuario.prestigio
                for connection in managerWebsockets.active_connections:
                    # print("id:")
                    # print(connection["clientid"].replace("{", "").replace("}", "").replace("$", ""))
                    if connection["clientid"].replace("{", "").replace("}", "").replace("$", "") == usuario.id:
                        print(connection["clientid"].replace("{", "").replace("}", "").replace("$", ""))
                        await connection["websocket"].send_text(str(usuario_websocket))   
            #print(mensajes)
            listaEliminarMensajes=[]
            for index, mensaje in enumerate(mensajes):
                for usuario in listaUsuarios:
                    if mensaje["usuarioRival"]==usuario.nombre:
                        for connection in managerWebsockets.active_connections:
                            #print("id:")
                            #print(connection["clientid"].replace("{", "").replace("}", "").replace("$", ""))
                            if connection["clientid"].replace("{", "").replace("}", "").replace("$", "") == usuario.id:
                                #print(connection["clientid"].replace("{", "").replace("}", "").replace("$", ""))
                                #print("mensaje")
                                await connection["websocket"].send_text(str(mensaje))
                                listaEliminarMensajes.append(index)
            
            for index in listaEliminarMensajes:
                mensajes.pop(index)

            if fecha.finalizar==True:
                break

            #print(mensajes)
        
        fin = time.time()
        tiempo_total = fin - inicio
        print(f"Tiempo de ejecución: {tiempo_total} segundos")
 



def ejecutar_metodo(clase_instancia):
    while True:
        if fecha.stop==False:
            store=clase_instancia.incrementar(listaUsuarios,db_manager)
        time.sleep(20)
        if fecha.finalizar==True:
            break




@app.get("/inicioPartida/")
async def inicioPartida():
    
    fecha.cambioStop(False)
    fecha.cambioFinalizar(False)
    fecha.cambioFecha(ano,mes)
    
    listaUsuarios=[]
    cargarUsuarios()

    # Inicia la tarea periódica
    loop = asyncio.get_event_loop()
    loop.create_task(periodic_broadcast())

    # Crear un hilo para ejecutar el método cada 20 segundos
    hilo = threading.Thread(target=ejecutar_metodo, args=(fecha,))
    hilo.daemon = True
    hilo.start()

    return 

@app.get("/stopPartida/")
async def stopPartida():
    fecha.cambioStop(True)
    return 

@app.get("/continuarPartida/")
async def continuarPartida():
    fecha.cambioStop(False)
    return 

@app.get("/finalizarPartida/")
async def finalizarPartida():
    fecha.cambioFinalizar(True)
    return

@app.get("/reinicioPartida/")
async def reinicioPartida():
    
    fecha.cambioFinalizar(True)

    time.sleep(25)
    fecha.cambioStop(False)
    fecha.cambioFinalizar(False)

    fecha.cambioFecha(ano,mes)
    listaUsuarios=[]
    cargarUsuarios()
    
    # Inicia la tarea periódica
    loop = asyncio.get_event_loop()
    loop.create_task(periodic_broadcast())

    # Crear un hilo para ejecutar el método cada 20 segundos
    hilo = threading.Thread(target=ejecutar_metodo, args=(fecha,))
    hilo.daemon = True
    hilo.start()

    return 

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await managerWebsockets.connect(websocket, client_id)
    try:
        await websocket.receive_text()  # Puedes usar esto para mantener la conexión abierta
    except WebSocketDisconnect:
        managerWebsockets.disconnect(websocket)

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = db_manager.buscar_usuario(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    ID_Usuario = db_manager.buscar_IDusuario(form.username)
    if not crypt.verify(form.password, user_db["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    access_token = {"sub": user_db["nombre"],
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer", "user_id": ID_Usuario}

@app.get("/registrarse/")
async def registrarse(nombreUsuario:str,contrasena:str):
    datosregistro=db_manager.registrarse(nombreUsuario,crypt.hash(contrasena))
    cargarUsuario(datosregistro['objetousuario'])
    return {"mensaje":datosregistro['mensaje']}

@app.get("/obtenerUsuarios/")
async def obtenerUsuarios(usuarioname: str):
    for usuario_objeto in listaUsuarios:
        if usuario_objeto.nombre==usuarioname:
            break
    return usuario_objeto

@app.get("/Fruterias/")
async def leerfruterias(ciudad,nombreUsuario):
    return db_manager.leer_fruterias(ciudad,nombreUsuario)

@app.get("/casas/")
async def leercasas(ciudad,nombreUsuario):
    return db_manager.leer_casas(ciudad,nombreUsuario)

@app.get("/ciudades/")
async def leerciudades(user: usuario_token = Depends(auth_user)):
    ciudades=db_manager.leer_ciudades()
    return {"token":obtenerToken(user),"ciudades":ciudades} 

@app.get("/CoordenadasCiudad/")
async def CoordenadasCiudad(nombreCiudad: str,user: usuario_token = Depends(auth_user)):
    return {"token":obtenerToken(user),"coordenadas": db_manager.leer_ciudad(nombreCiudad)} 

@app.get("/getItemsPlantaciones/")
async def getItemsPlantaciones():
    return db_manager.getItemsPlantaciones()

@app.get("/obtenerTiendaItems/")
async def obtenerTiendaItems(nombreCiudad,nombreTienda,nombreUsuario):
    selects=[]
    tienda=db_manager.leerTiendaPropia(nombreCiudad,nombreTienda,nombreUsuario)
    for producto in tienda['arrayProductos']:
        item={"nombre": producto['tipo'], "urlicono": producto['urlicono']}
        selects.append(item)
    return selects

@app.get("/ciudadesUsuario/")
async def leerciudades(nombreCiudad,nombreUsuario,user: usuario_token = Depends(auth_user)):    
    return {"token":obtenerToken(user),"resultado":db_manager.leer_ciudades_usuario(nombreUsuario,nombreCiudad)} 

@app.get("/comprarCasa/")
async def comprarCasa(nombreUsuario:str, nombreCiudad: str,nombreCasa:str,precio:int):
    
    for usuario in listaUsuarios:
        if nombreUsuario==str(usuario.nombre):
            break
    
    for ciudad in usuario.listaciudades:
        if ciudad.nombre==nombreCiudad:
            if ciudad.casa!=None:
                return {"mensaje":"Ya tienes casa en este municipio","tipo":"info"}
            
    if usuario.dinero > precio:
        usuario.crear_ciudad(nombreciudad=nombreCiudad,bbdd=db_manager)   
        usuario.comprar_casa(nombreciudad=nombreCiudad,nombrecasa=nombreCasa,bbdd=db_manager)
        db_manager.cambiar_propietario_casa(nombreCiudad, nombreCasa,  usuario.nombre)
        db_manager.updateusuario(usuario)
        return {"mensaje":"Casa comprada con exito","tipo":"success"}
    else:
        return {"mensaje":"No tienes suficiente dinero para comprar la casa","tipo":"info"}

@app.get("/comprarParcela/")
async def comprarParcela(nombreUsuario:str, nombreCiudad: str,nombreParcela:str,precio:int):
    
    for usuario in listaUsuarios:
        if nombreUsuario==str(usuario.nombre):
            break

    if usuario.dinero > precio:   
        usuario.comprar_parcela(nombreciudad=nombreCiudad,nombreparcela=nombreParcela,bbdd=db_manager)
        db_manager.cambiar_propietario_parcela(nombre_ciudad=nombreCiudad,nombre_parcela=nombreParcela,nombre_usuario=usuario.nombre)
        db_manager.updateusuario(usuario)
        return {"mensaje":"Parcela comprada con exito","tipo":"success"}
    else:
        return {"mensaje":"No tienes suficiente dinero para comprar la parcela","tipo":"info"}

@app.get("/comprarTienda/")
async def comprarTienda(nombreUsuario:str, nombreCiudad: str,nombreTienda:str,precio:int):
    for usuario in listaUsuarios:
        if nombreUsuario==str(usuario.nombre):
            break   
    if usuario.dinero > precio:
        usuario.comprar_tienda(nombreciudad=nombreCiudad,nombretienda=nombreTienda,bbdd=db_manager)
        db_manager.cambiar_propietario_tienda(nombreCiudad, nombreTienda, usuario.nombre)
        db_manager.updateusuario(usuario)
        return {"mensaje":"Tienda comprada con exito","tipo":"success"}
    else:
        return {"mensaje":"No tienes suficiente dinero para comprar la tienda","tipo":"info"}



@app.get("/modificarPlantacion/")
async def modificarPlantacion(nombreUsuario:str, nombreCiudad: str,nombreParcela:str, arrayPlantacion:str):
    arrayPlantacion = arrayPlantacion.split(",")
    for usuario in listaUsuarios:
        if nombreUsuario==str(usuario.nombre):
            break   
    for index, plantacion in enumerate(arrayPlantacion):
        usuario.modificar_plantacion(indice=index, nombreciudad=nombreCiudad,nombreparcela=nombreParcela,tipoplantacion=plantacion, bbdd=db_manager)
    db_manager.updateusuario(usuario)
    return {"mensaje":"Plantaciones modificadas con exito"}

@app.get("/agregarProducto/")
async def agregarProducto(nombreUsuario:str, nombreCiudad: str,nombreTienda:str, tipoProducto:str):
    for usuario in listaUsuarios:
        if nombreUsuario==str(usuario.nombre):
            break
    usuario.agregar_producto(nombreciudad=nombreCiudad,nombretienda=nombreTienda,tipoproducto=tipoProducto)
    return usuario

@app.get("/modificarProductos/")
async def modificarProductos(nombreUsuario:str, nombreCiudad: str,nombreTienda:str, arrayProductos:str):
    arrayProductos = arrayProductos.split(",")
    for usuario in listaUsuarios:
        if nombreUsuario==str(usuario.nombre):
            break   
    for index, producto in enumerate(arrayProductos):
        usuario.modificar_producto(indice=index, nombreciudad=nombreCiudad,nombretienda=nombreTienda,tipoproducto=producto)
    db_manager.updateusuario(usuario)
    return {"mensaje":"Productos modificados con exito"}

@app.get("/contratarEmpleado/")
async def contratarEmpleado(nombreUsuario:str, nombreCiudad: str,Lugar:str, nombreEmpleado:str):
    for usuario in listaUsuarios:
        if nombreUsuario==str(usuario.nombre):
            break   
    mensaje=usuario.contratarempleado(nombreciudad=nombreCiudad,lugar=Lugar,nombreempleado=nombreEmpleado, bbdd=db_manager)
    db_manager.cambiar_jefe_empleado(nombreCiudad, nombreEmpleado,  usuario.nombre, Lugar)
    db_manager.updateusuario(usuario)
    return mensaje

@app.get("/obtenerEmpleadosParados/")
async def obtenerEmpleadosParados(nombreCiudad: str):
    return db_manager.obtenerEmpleadosParados(nombreCiudad)

@app.get("/despedirEmpleado/")
async def despedirEmpleado(nombreUsuario:str, nombreCiudad: str,Lugar:str, nombreEmpleado:str):
    for usuario in listaUsuarios:
        if nombreUsuario==str(usuario.nombre):
            break   
    mensaje=usuario.despedirempleado(nombreciudad=nombreCiudad,lugar=Lugar,nombreempleado=nombreEmpleado)
    db_manager.cambiar_jefe_empleado(nombreCiudad, nombreEmpleado,  "SinJefe", "Libre")
    return mensaje

@app.get("/Parcelas/")
async def leerparcelas(ciudad,nombreUsuario):
    parcelas=db_manager.leer_parcelas(ciudad,nombreUsuario)
    return parcelas


@app.get("/obtenerParcelaPropietario/")
async def leerparcelas(nombreCiudad,nombreParcela,nombreUsuario,user: usuario_token = Depends(auth_user)):
    return {"token":obtenerToken(user),"parcela":db_manager.leer_parcelasPropia(nombreCiudad,nombreParcela,nombreUsuario)} 

@app.get("/obtenerParcelaItems/")
async def obtenerParcelaItems(nombreCiudad,nombreParcela,nombreUsuario):
    selects=[]
    parcela=db_manager.leer_parcelasPropia(nombreCiudad,nombreParcela,nombreUsuario)
    for producto in parcela['listaplantacion']:
        item={"nombre": producto['tipo'], "urlicono": producto['urlicono']}
        selects.append(item)
    return selects

@app.get("/obtenerParcelaRival/")
async def obtenerParcelaRival(nombreCiudad,nombreParcela,nombreUsuario,user: usuario_token = Depends(auth_user)):
    return {"token":obtenerToken(user),"parcela":db_manager.leer_parcelasRival(nombreCiudad,nombreParcela,nombreUsuario)}

@app.get("/obtenerCasaPropietario/")
async def obtenerCasaPropietario(nombreCiudad,nombreCasa,nombreUsuario,user: usuario_token = Depends(auth_user)):
    return {"token":obtenerToken(user),"casa":db_manager.leerCasaPropia(nombreCiudad,nombreCasa,nombreUsuario)}

@app.get("/obtenerCasaRival/")
async def obtenerCasaRival(nombreCiudad,nombreCasa,nombreUsuario,user: usuario_token = Depends(auth_user)):
    return {"token":obtenerToken(user),"casa":db_manager.leerCasaRival(nombreCiudad,nombreCasa,nombreUsuario)}

@app.get("/obtenerTiendaPropietario/")
async def obtenerTiendaPropietario(nombreCiudad,nombreTienda,nombreUsuario,user: usuario_token = Depends(auth_user)):
    return {"token":obtenerToken(user),"tienda":db_manager.leerTiendaPropia(nombreCiudad,nombreTienda,nombreUsuario)}

@app.get("/obtenerTiendaRival/")
async def obtenerParcelaRival(nombreCiudad,nombreTienda,nombreUsuario,user: usuario_token = Depends(auth_user)):
    return {"token":obtenerToken(user),"tienda":db_manager.leerTiendaRival(nombreCiudad,nombreTienda,nombreUsuario)}

@app.get("/robarCasa/")
async def RobarCasa(nombreUsuario,nombreCiudad,nombreCasa,nombreUsuarioRival):
    mensaje={
        "IDMessage":"RoboCasa",
        "mensaje": "",
        "usuarioRival": "",
        "usuario":"",
        "nombreciudad":"",
        "casa":"",
        }
    mensajeRobo=""
    for usuario in listaUsuarios:
        if usuario.nombre == nombreUsuarioRival:    
            for ciudad in usuario.listaciudades:
                if ciudad.nombre == nombreCiudad:
                    if  roboCasa(ciudad.casa.seguridad):
                        cantidadRobo=cantidadRoboCasa()
                        usuario.dinero=usuario.dinero-cantidadRobo
                        mensajeRobo="Robo con exito, has conseguido "+str(cantidadRobo)                  
                        mensaje["mensaje"]="El contrincante "+nombreUsuario+" te ha robado en "+nombreCasa+" del municipio de "+nombreCiudad+" una cantidad de "+str(cantidadRobo)+" Euros."
                    else:
                        multaRobo=cantidadMultaRoboCasa()
                        mensajeRobo="Te han pillado robando, vas a tener una multa de "+ str(multaRobo)
                        for usuario in listaUsuarios:
                            if usuario.nombre == nombreUsuario:
                                usuario.dinero=usuario.dinero-multaRobo
                        mensaje["mensaje"]="El contrincante "+nombreUsuario+" te ha intentado robar en "+nombreCasa+" del municipio de "+nombreCiudad+". La policia le ha pillado."
                    break

    
    mensaje["usuarioRival"]=nombreUsuarioRival
    mensaje["usuario"]=nombreUsuario
    mensaje["nombreciudad"]=nombreCiudad
    mensaje["casa"]=nombreCasa
    mensajes.append(mensaje)               
    return mensaje

@app.get("/RobarParcela/")
async def RobarParcela(nombreUsuario,nombreCiudad,nombreParcela,nombreUsuarioRival):
    mensaje={
        "IDMessage":"RoboParcela",
        "mensaje": "",
        "usuarioRival": "",
        "usuario":"",
        "nombreciudad":"",
        "lugar":"",
        }
    mensajeRobo=""
    lista_produccion = []
    roboOK=False
    multaRobo=0
    if "Libre" == nombreUsuarioRival:
        if roboParcela(2):
            for plantacion in db_manager.getItemsPlantaciones():  
                produccion = {}  # Crear un nuevo diccionario para cada plantación   
                produccion["tipo"] = plantacion["nombre"]
                produccion["numero"] = randomRoboParcelaLibre()
                lista_produccion.append(produccion)
                mensajeRobo=mensajeRobo+str(produccion["numero"])+" de "+produccion["tipo"]+". "
            mensajeRobo="Robo con exito, has conseguido "+mensajeRobo
            roboOK=True
            mensaje["mensaje"]="El contrincante "+nombreUsuario+" te ha robado en "+nombreParcela+" del municipio de "+nombreCiudad+": "+mensajeRobo
        else:
            multaRobo=cantidadMultaRoboParcela_valor
            mensajeRobo="Te han pillado robando, vas a tener una multa de "+ str(multaRobo)
            for usuario in listaUsuarios:
                if usuario.nombre == nombreUsuario:
                    usuario.dinero=-multaRobo
            mensaje["mensaje"]="El contrincante "+nombreUsuario+" te ha intentado robar en "+nombreParcela+" del municipio de "+nombreCiudad+". La policia le ha pillado."
        

    for usuario in listaUsuarios:
        if usuario.nombre == nombreUsuarioRival:    
            for ciudad in usuario.listaciudades:
                if ciudad.nombre == nombreCiudad:
                    for parcela in ciudad.listaparcelas:
                        if parcela.nombre == nombreParcela: 
                            if roboParcela(parcela.seguridad):
                                parcela.habilitacionproduccionmes=False
                                for plantacion in parcela.listaplantacion:  
                                    produccion = {}  # Crear un nuevo diccionario para cada plantación   
                                    produccion["tipo"] = plantacion.tipo
                                    produccion["numero"] = 1 * plantacion.factormultiplicacion * plantacion.produccionmes[fecha.mes] * parcela.indiceproduccionempleados * parcela.calidadterreno * parcela.indiceproductividadempleados
                                    #print(produccion["numero"], "random_anual", plantacion.factormultiplicacion, plantacion.produccionmes[fecha.mes], parcela.indiceproduccionempleados, parcela.calidadterreno, parcela.indiceproductividadempleados)
                                    lista_produccion.append(produccion)
                                    mensajeRobo=mensajeRobo+str(produccion["numero"])+" de "+produccion["tipo"]+". "
                                mensajeRobo="Robo con exito, has conseguido "+mensajeRobo
                                roboOK=True
                                mensaje["mensaje"]="El contrincante "+nombreUsuario+" te ha robado en "+nombreParcela+" del municipio de "+nombreCiudad+": "+mensajeRobo
                            else:
                                multaRobo=cantidadMultaRoboParcela_valor
                                mensajeRobo="Te han pillado robando, vas a tener una multa de "+ str(multaRobo)
                                for usuario in listaUsuarios:
                                    if usuario.nombre == nombreUsuario:
                                        usuario.dinero=-multaRobo
                                mensaje["mensaje"]="El contrincante "+nombreUsuario+" te ha intentado robar en "+nombreParcela+" del municipio de "+nombreCiudad+". La policia le ha pillado."
                            break
                        
    if roboOK==True:
        for usuario in listaUsuarios:
            if usuario.nombre == nombreUsuario:
                for producto in lista_produccion:
                    elemento = {}  
                    for idx, elemento in enumerate(usuario.almacen):
                        if elemento["tipo"] == producto["tipo"]:
                            elemento["numero"] = elemento["numero"] + producto["numero"]
                            usuario.almacen[idx]["numero"] = elemento["numero"]

    mensaje["usuarioRival"]=nombreUsuarioRival
    mensaje["usuario"]=nombreUsuario
    mensaje["nombreciudad"]=nombreCiudad
    mensaje["lugar"]=nombreParcela
    mensajes.append(mensaje)
    #print(mensajes)             
    
    if roboOK==True:
        return {"mensaje":mensajeRobo,"tipo":"success"}
    else:
        usuario.dinero=usuario.dinero-cantidadMultaRoboParcela
        return {"mensaje":"La policia te ha pillado robandp la parcela. Te han multado con 15000 euros","tipo":"info"}

@app.get("/RobarTienda/")
async def RobarTienda(nombreUsuario,nombreCiudad,nombreTienda,nombreUsuarioRival):
    roboOK=False
    mensaje={
        "IDMessage":"RoboTienda",
        "mensaje": "",
        "usuarioRival": "",
        "usuario":"",
        "nombreciudad":"",
        "tienda":"",
        }
    #print(nombreUsuario,nombreCiudad,nombreTienda,nombreUsuarioRival)
    mensajeRobo=""

    for usuario in listaUsuarios:
        if usuario.nombre == nombreUsuarioRival:    
            for ciudad in usuario.listaciudades:
                if ciudad.nombre == nombreCiudad:
                    for tienda in ciudad.listatiendas:
                        if tienda.nombre == nombreTienda: 
                            if  random.uniform(0, 4.5) > tienda.seguridad:
                                cantidadRobo=random.uniform(minimoRoboCasa, maximoRoboCasa)
                                usuario.dinero=-cantidadRobo
                                mensajeRobo="Robo con exito, has conseguido "+str(cantidadRobo)
                                roboOK=True
                                mensaje["mensaje"]="El contrincante "+nombreUsuario+" te ha robado en "+nombreTienda+" del municipio de "+nombreCiudad+" una cantidad de "+str(cantidadRobo)+" Euros."
                            else:
                                multaRobo=cantidadMultaRoboTienda()
                                mensajeRobo="Te han pillado robando, vas a tener una multa de "+ str(multaRobo)
                                for usuario in listaUsuarios:
                                    if usuario.nombre == nombreUsuario:
                                        usuario.dinero=-multaRobo
                                mensaje["mensaje"]="El contrincante "+nombreUsuario+" te ha intentado robar en "+nombreTienda+" del municipio de "+nombreCiudad+". La policia le ha pillado."
                            break

    
    mensaje["usuarioRival"]=nombreUsuarioRival
    mensaje["usuario"]=nombreUsuario
    mensaje["nombreciudad"]=nombreCiudad
    mensaje["tienda"]=nombreTienda
    mensajes.append(mensaje)
    #print(mensajes)                
    
    if roboOK==True:
        return {"mensaje":mensajeRobo,"resultado":True}
    else:
        usuario.dinero=usuario.dinero-cantidadMultaRoboTienda
        return {"mensaje":mensajeRobo,"resultado":False}

@app.get("/OfertaParcela/")
async def OfertaParcela(nombreUsuario,nombreCiudad,nombreParcela,nombreUsuarioRival,oferta):
    mensaje={
        "IDMessage":"",
        "mensaje": "",
        "usuarioRival": "",
        "usuario":"",
        "nombreciudad":"",
        "lugar":"",
        "oferta":0,
        }
     
    mensaje["mensaje"]="El contrincante "+nombreUsuario+" te ha realizado una oferta por la "+nombreParcela+" de municipio de "+nombreCiudad+" por "+str(oferta)+" Euros"
    mensaje["usuarioRival"]=nombreUsuarioRival
    mensaje["usuario"]=nombreUsuario
    mensaje["IDMessage"]="Oferta"
    mensaje["nombreciudad"]=nombreCiudad
    mensaje["lugar"]=nombreParcela
    mensaje["oferta"]=oferta
    mensajes.append(mensaje)
    return {"mensaje":"Oferta enviada correctamente"} 

@app.get("/OfertaTienda/")
async def OfertaTienda(nombreUsuario,nombreCiudad,nombreTienda,nombreUsuarioRival,oferta):
    mensaje={
        "IDMessage":"",
        "mensaje": "",
        "usuarioRival": "",
        "usuario":"",
        "nombreciudad":"",
        "lugar":"",
        "oferta":0,
        }
     
    mensaje["mensaje"]="El contrincante "+nombreUsuario+" te ha realizado una oferta por la "+nombreTienda+" de municipio de "+nombreCiudad+" por "+str(oferta)+" Euros"
    mensaje["usuarioRival"]=nombreUsuarioRival
    mensaje["usuario"]=nombreUsuario
    mensaje["IDMessage"]="Oferta"
    mensaje["nombreciudad"]=nombreCiudad
    mensaje["lugar"]=nombreTienda
    mensaje["oferta"]=oferta
    mensajes.append(mensaje)
    return {"mensaje":"Oferta enviada correctamente"} 

@app.get("/aceptarOferta/")
async def aceptarOferta(nombreUsuario,usuarioRival,nombreCiudad,lugar,oferta):
    tipo=""
    for usuario in listaUsuarios:
        if nombreUsuario==str(usuario.nombre):
            break
    
    if usuario.dinero>oferta:
        #print(nombreUsuario,usuarioRival,nombreCiudad,lugar,oferta)
        for usuario in listaUsuarios:
            if usuario.nombre==usuarioRival:
                for ciudad in usuario.listaciudades:
                    if ciudad.nombre==nombreCiudad:
                        for parcela in ciudad.listaparcelas:
                            if parcela.nombre == lugar:
                                db_manager.cambiar_propietario_parcela(nombreCiudad, lugar, nombreUsuario)
                                for empleado in parcela.listaempleados:
                                    db_manager.cambiar_jefe_empleado( nombreCiudad, empleado.nombre,  nombreUsuario, lugar)
                                tipo="parcela"
                                break
                        for tienda in ciudad.listatiendas:
                            if tienda.nombre == lugar:
                                db_manager.cambiar_propietario_tienda(nombreCiudad, lugar, nombreUsuario)
                                for empleado in parcela.listaempleados:
                                    db_manager.cambiar_jefe_empleado( nombreCiudad, empleado.nombre,  nombreUsuario, lugar)
                                tipo="tienda"
                                break
        

        for Rival in listaUsuarios:
            if usuarioRival==str(Rival.nombre):
                Rival.dinero=+int(oferta)
                break  
        
        for usuario in listaUsuarios:
            if nombreUsuario==str(usuario.nombre):
                usuario.dinero=-int(oferta)
                break


        if tipo == "parcela":        
            parcela=Rival.eliminar_y_obtener_parcela_por_nombre(nombreciudad=nombreCiudad,nombreparcela=lugar) 
            usuario.añadir_parcela(nombreCiudad,parcela)

        if tipo == "tienda":        
            tienda=Rival.eliminar_y_obtener_tienda_por_nombre(nombreciudad=nombreCiudad,nombretienda=lugar) 
            usuario.añadir_tienda(nombreCiudad,tienda)


        for Rival in listaUsuarios:
            if usuarioRival==str(Rival.nombre):
                break  
        
        for usuario in listaUsuarios:
            if nombreUsuario==str(usuario.nombre):
                break


        db_manager.updateusuario(usuario)
        db_manager.updateusuario(Rival) 
        usuario.mostrar_informacion()
        Rival.mostrar_informacion()
        # db_manager.cambiarPropiedad(nombreUsuario,usuarioRival,nombreCiudad,lugar,tipo)

        mensajeAceptadaOferta={
            "IDMessage":"OfertaRespuesta",
            "mensaje":"El contrincante "+nombreUsuario+" ha aceptado la oferta por la "+lugar+" de municipio de "+nombreCiudad,
            "usuarioRival": usuarioRival,
            "usuario":nombreUsuario,
            "nombreciudad":nombreCiudad,
            "lugar":lugar,
            "aceptada":"aceptada"
            }
        mensajes.append(mensajeAceptadaOferta)
        return {"mensaje":"Oferta aceptada","aceptada":True}
    else:
        return {"mensaje":"No tienes suficiente dinero para aceptar la oferta","aceptada":False}

@app.get("/rechazarOferta/")
async def rechazarOferta(nombreUsuario,usuarioRival,nombreCiudad,lugar,oferta):
    mensajeRechazoOferta={
        "IDMessage":"OfertaRespuesta",
        "mensaje":"El contrincante "+usuarioRival+" ha rechazado la oferta por la "+lugar+" de municipio de "+nombreCiudad,
        "usuarioRival": nombreUsuario,
        "usuario":usuarioRival,
        "nombreciudad":nombreCiudad,
        "lugar":lugar,
        "aceptada":"rechazada"
        }
    mensajes.append(mensajeRechazoOferta)
    return {"mensaje":"Oferta rechazada"}

@app.get("/espiarCasa/")
async def EspiarCasa(nombreCiudad,nombreCasa,nombreUsuarioRival):
    for usuario in listaUsuarios:
        if usuario.nombre == nombreUsuarioRival:    
            for ciudad in usuario.listaciudades:
                if 1*random.uniform(0.5, 1)  > 0.5:  #revisar
                    return ciudad.casa
    return None

@app.get("/EspiarParcela/")
async def EspiarParcela(nombreCiudad,nombreParcela,nombreUsuarioRival):
    for usuario in listaUsuarios:
        if usuario.nombre == nombreUsuarioRival:    
            for ciudad in usuario.listaciudades:
                if ciudad.nombre == nombreCiudad:
                    for parcela in ciudad.listaparcelas:
                        if parcela.nombre == nombreParcela:
                            if random.uniform(0, 1)  > 0.5:  
                                return {"parcela":parcela,"mensaje":"Espionaje con exito","resultado":True}
    usuario.dinero=usuario.dinero-cantidadMultaParcela
    return {"parcela":parcela,"mensaje":"La policia te ha pillado espiando la parcela. Te han multado con 5000 euros","resultado":False}

@app.get("/EspiarTienda/")
async def EspiarTienda(nombreCiudad,nombreTienda,nombreUsuarioRival):
    for usuario in listaUsuarios:
        if usuario.nombre == nombreUsuarioRival:    
            for ciudad in usuario.listaciudades:
                if ciudad.nombre == nombreCiudad:
                    for tienda in ciudad.listatiendas:
                        if tienda.nombre == nombreTienda:
                            if random.uniform(0, 1)  > 0.5:  
                                return {"tienda":tienda,"mensaje":"Espionaje con exito","resultado":True}
    usuario.dinero=usuario.dinero-cantidadMultaTienda
    return {"tienda":tienda,"mensaje":"La policia te ha pillado espiando la tienda. Te han multado con 5000 euros","resultado":False}

@app.get("/incrementarSeguridad/")
async def incrementarSeguridad(nombreUsuario:str, nombreCiudad: str,Lugar:str, indice:int,precio:int):
    for usuario in listaUsuarios:
        if nombreUsuario==str(usuario.nombre):
            break   
    if usuario.dinero > precio:    
        usuario.cambiarSeguridad(nombreciudad=nombreCiudad,lugar=Lugar,indice=indice,precioMejoraSeguridad=precio)
        db_manager.cambiarSeguridadParcela(nombreciudad=nombreCiudad,nombreParcela=Lugar,indice=indice)
        db_manager.updateusuario(usuario)
        return {"mensaje":"Se ha mejorado la seguridad"}
    else:
        return {"mensaje":"No tienes suficiente dinero para mejorar la seguridad"}

@app.get("/incrementarSeguridadTienda/")
async def incrementarSeguridad(nombreUsuario:str, nombreCiudad: str,Lugar:str, indice:int,precio:int):
    for usuario in listaUsuarios:
        if nombreUsuario==str(usuario.nombre):
            break   
    if usuario.dinero > precio:    
        usuario.cambiarSeguridadTienda(nombreciudad=nombreCiudad,lugar=Lugar,indice=indice,precioMejoraSeguridad=precio)
        db_manager.cambiarSeguridadTienda(nombreciudad=nombreCiudad,nombreTienda=Lugar,indice=indice)
        db_manager.updateusuario(usuario)
        return {"mensaje":"Se ha mejorado la seguridad"}
    else:
        return {"mensaje":"No tienes suficiente dinero para mejorar la seguridad"}

@app.get("/incrementarSeguridadCasa/")
async def incrementarSeguridadCasa(nombreUsuario:str, nombreCiudad: str,Casa:str, indice:int,precio:int):
    for usuario in listaUsuarios:
        if nombreUsuario==str(usuario.nombre):
            break 
    if usuario.dinero > precio:  
        usuario.cambiarSeguridadCasa(nombreciudad=nombreCiudad,nombreCasa=Casa,indice=indice,precioMejoraSeguridad=precio)
        db_manager.cambiarSeguridadCasa(nombreciudad=nombreCiudad,nombreCasa=Casa,indice=indice)
        db_manager.updateusuario(usuario)
        return {"mensaje":"Se ha mejorado la seguridad"}
    else:
        return {"mensaje":"No tienes suficiente dinero para mejorar la seguridad"}
        
    
@app.get("/incrementarCalidadTerreno/")
async def incrementarSeguridadTerreno(nombreUsuario:str, nombreCiudad: str,Lugar:str, indice:int,precio:int):
    for usuario in listaUsuarios:
        if nombreUsuario==str(usuario.nombre):
            break 
    if usuario.dinero > precio:   
        usuario.incrementarCalidadTerreno(nombreciudad=nombreCiudad,lugar=Lugar,indice=indice,precioMejora=precio)
        # db_manager.cambiarCalidadTerreno(nombreciudad=nombreCiudad,nombreParcela=Lugar,indice=indice)
        db_manager.updateusuario(usuario)
        return {"mensaje":"Se ha mejorado la calidad del terreno"}
    else:
        return {"mensaje":"No tienes suficiente dinero para mejorar la calidad del terreno"}

@app.get("/actualizarclasificacion/")
async def actualizarclasificacion():
    clasificacion = []  # Inicializa una lista vacía

    for usuario in listaUsuarios:
        posicion = {
            "nombre": usuario.nombre,
            "dinero": usuario.dinero,
            "iniciales": usuario.nombre[:2],
        }
        clasificacion.append(posicion)

        # Ordena la lista por el valor de 'dinero' en orden descendente
    clasificacion = sorted(clasificacion, key=lambda x: x['dinero'], reverse=True)
    return clasificacion

""" 
@app.get("/comprarEmpresaElectronica/")
async def comprarEmpresaElectronica(nombreUsuario:str, nombreCiudad: str,nombreEmpresa:str):
    db_manager = DatabaseManager(pathBBDD)
    for usuario in listaUsuarios:
        if nombreUsuario==str(usuario.nombre):
            break
    usuario.crear_ciudad(nombreciudad=nombreCiudad,bbdd=db_manager)   
    usuario.comprar_empresaelectronica(nombreciudad=nombreCiudad,nombreempresa=nombreEmpresa,bbdd=db_manager)
    db_manager.cerrar_conexion()
    return usuario

@app.get("/contratarEmpleadoElectronica/")
async def contratarEmpleadoElectronica(nombreUsuario:str, nombreCiudad: str,Lugar:str, nombreEmpleado:str):
    db_manager = DatabaseManager(pathBBDD)
    for usuario in listaUsuarios:
        if nombreUsuario==str(usuario.nombre):
            break   
    usuario.contratarempleado(nombreciudad=nombreCiudad,lugar=Lugar,nombreempleado=nombreEmpleado, bbdd=db_manager)
    db_manager.cerrar_conexion()
    return usuario

@app.get("/agregarProyectoElectronica/")
async def agregarProyectoElectronica(nombreUsuario:str, nombreCiudad: str,nombreEmpresaElectronica:str, nombreProyecto:str):
    for usuario in listaUsuarios:
        if nombreUsuario==str(usuario.nombre):
            break
    usuario.agregar_proyecto_electronica(nombreciudad=nombreCiudad,nombreEmpresaElectronica=nombreEmpresaElectronica,nombreProyecto=nombreProyecto)
    return usuario """





""" async def main():
    task = asyncio.create_task(broadcast_periodically(manager))
    # Puedes seguir realizando otras tareas aquí si es necesario
    await task

# Ejecutar el loop de eventos de asyncio
if __name__ == "__main__":
    asyncio.run(main()) """

# Mantener el programa en ejecución
""" try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    
    pass """