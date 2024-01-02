from pymongo import MongoClient
import json
from Formulas import obtenerDineroInicial

class DatabaseManager:
    def __init__(self, db_name):
        self.db_client=MongoClient(db_name).test

    def obtener_informacion_ciudad(self, nombre_ciudad):
        campos=self.db_client.ciudades.find_one({"nombre": nombre_ciudad})
        result = campos.get("poblacion"),campos.get("coordenadas_x"),campos.get("coordenadas_y"), campos.get("idioma_principal"), campos.get("indice_productos")
        return result
    
    def obtener_datos_usuario(self, nombre):
        campos=self.db_client.usuarios.find_one({"nombre": nombre})
        result = campos.get("edad")
        return result
    
    def obtener_informacion_parcela(self, nombre_parcela, nombre_ciudad):  
        #print(nombre_parcela, nombre_ciudad)
        #print(nombre_parcela, nombre_ciudad)
        campos=self.db_client.parcelas.find_one({"nombre_parcela": nombre_parcela,"nombre_ciudad": nombre_ciudad})
        result = campos.get("precio"),campos.get("tamano"),campos.get("numeroplantaciones")
        return result
    
    def cambiar_propietario_parcela(self, nombre_ciudad, nombre_parcela,  nombre_usuario):  
        self.db_client.parcelas.find_one_and_update({"nombre_parcela": nombre_parcela,"nombre_ciudad": nombre_ciudad}, { '$set': { "propietario" : nombre_usuario, "objeto.0.features.0.properties.name" : nombre_usuario}})
    
    def obtener_informacion_produccion_platacion(self, tipo):
        #print("tipo")
        #print(tipo)
        campos=self.db_client.produccion_plantacion.find_one({"tipo_plantacion": tipo})
        result = campos.get("tipo_plantacion"),campos.get("enero"),campos.get("febrero"),campos.get("marzo"),campos.get("abril"),campos.get("mayo"),campos.get("junio"),campos.get("julio"),campos.get("agosto"),campos.get("septiembre"),campos.get("octubre"),campos.get("noviembre"),campos.get("diciembre")
        return result,campos.get("urlicono")
    
    def obtener_informacion_produccion_platacion_meses(self, tipo):
        #print("tipo")
        #print(tipo)
        campos=self.db_client.produccion_plantacion.find_one({"tipo_plantacion": tipo})
        #print("campos")
        #print(campos)
        result = campos.get("tipo_plantacion"),campos.get("enero"),campos.get("febrero"),campos.get("marzo"),campos.get("abril"),campos.get("mayo"),campos.get("junio"),campos.get("julio"),campos.get("agosto"),campos.get("septiembre"),campos.get("octubre"),campos.get("noviembre"),campos.get("diciembre")
        return result

    def obtener_informacion_tienda(self, nombre_tienda, nombre_ciudad):
        #print(nombre_tienda, nombre_ciudad)
        campos=self.db_client.tiendas.find_one({"nombre_tienda": nombre_tienda,"nombre_ciudad": nombre_ciudad})
        result = campos.get("precio"),campos.get("tamano"),campos.get("prestigio"),campos.get("numeroMaximoEmpleados")
        return result   
        
    def cambiar_propietario_tienda(self, nombre_ciudad, nombre_tienda,  nombre_usuario):  
        self.db_client.tiendas.find_one_and_update({"nombre_tienda": nombre_tienda,"nombre_ciudad": nombre_ciudad}, { '$set': { "propietario" : nombre_usuario} })
  
    def obtener_informacion_empleado(self, nombre_empleado, nombre_ciudad):
        campos=self.db_client.empleados.find_one({"nombre_empleado": nombre_empleado,"empleado_ciudad": nombre_ciudad})
        result = campos.get("precio_empleado"),campos.get("comunicacion"),campos.get("estudios"),campos.get("fuerza"),campos.get("liderazgo")
        return result 

    def cambiar_jefe_empleado(self, nombre_ciudad, nombre_empleado,  nombre_usuario, lugar):  
        self.db_client.empleados.find_one_and_update({"nombre_empleado": nombre_empleado,"empleado_ciudad": nombre_ciudad}, { '$set': { "Jefe" : nombre_usuario, "Lugar" : lugar} })
  
    def obtener_informacion_casa(self, nombre_casa, nombre_ciudad):
        campos=self.db_client.casas.find_one({"nombre_casa": nombre_casa,"nombre_ciudad": nombre_ciudad})
        result = campos.get("precio"), campos.get("prestigio")
        return result

    def cambiar_propietario_casa(self, nombre_ciudad, nombre_casa,  nombre_usuario):  
        self.db_client.casas.find_one_and_update({"nombre_casa": nombre_casa,"nombre_ciudad": nombre_ciudad}, { '$set': { "propietario" : nombre_usuario}})
  
    def obtener_informacion_empresa(self, nombre_empresa, nombre_ciudad):
        campos=self.db_client.empresas.find_one({"nombre_empresa": nombre_empresa,"nombre_ciudad": nombre_ciudad})
        result = campos.get("precio"),campos.get("tamano")
        return result 

    def cambiar_propietario_empresa(self, nombre_ciudad, nombre_empresa,  nombre_usuario):  
        self.db_client.empresas.find_one_and_update({"nombre_empresa": nombre_empresa,"nombre_ciudad": nombre_ciudad}, { '$set': { "propietario" : nombre_usuario}})
  
    def obtener_informacion_empleado_electronica(self, nombre_empleado, nombre_ciudad):
        campos=self.db_client.empleados_electronica.find_one({"nombre_empleado": nombre_empleado, "empleado_ciudad": nombre_ciudad})
        result = campos.get("precio_empleado"), campos.get("tipo")
        return result 
    
    def obtener_informacion_proyecto_electronica(self,nombreproyecto):
        campos=self.db_client.proyectos_electronica.find_one({"nombreproyecto": nombreproyecto})
        result = campos.get("descripcion"),campos.get("relevancia"), campos.get("presupuesto"), campos.get("numeroempleadosHW"), campos.get("numeroempleadosFW"), campos.get("numeroempleadosSW"), campos.get("numeroempleadosProduccion"), campos.get("numeroempleadosTesting"), campos.get("numeroempreadosMecanica"), campos.get("numeroepleadosGestion"), campos.get("duracionmeses"), campos.get("dificultad"), campos.get("tipo"), campos.get("producto"), campos.get("numeroproductos")
        return result 
    
    def leer_ciudades(self):
        ciudades = []  # Usamos una lista para almacenar las ciudades
        for campos in self.db_client.ciudades.find():
            ciudad = {
                "name": campos.get("nombre"),
                "coords": [campos.get("coordenadas_x"), campos.get("coordenadas_y")],  # Corregimos las coordenadas
                "radius": campos.get("radio"),
                "poblacion": campos.get("poblacion"),
                "descripcion":campos.get("descripcion"),
                "imagenurl":campos.get("imagenurl"),
            }
            ciudades.append(ciudad)
        return ciudades

    def leer_ciudades_usuario(self,nombreUsuario,nombreCiudad):
        
        resultado = self.db_client.datosusuarios.find_one({'nombre': nombreUsuario})

        for ciudad_info in resultado['listaciudades']:
            if ciudad_info['nombre'] == nombreCiudad:
                return True
        return False
    
    def leer_ciudad(self,nombreciudad):
        campos=self.db_client.ciudades.find_one({"nombre": nombreciudad})
        ciudad = {
                "name": campos.get("nombre"),
                "coords": [campos.get("coordenadas_x"), campos.get("coordenadas_y")],  # Corregimos las coordenadas
                "radius": campos.get("radio"),
            }
        #print(ciudad)
        return ciudad


    def leer_parcelas(self,nombre_ciudad,nombreusuario):
        parcelas = []  # Usamos una lista para almacenar las ciudades
        for campos in self.db_client.parcelas.find({"nombre_ciudad": nombre_ciudad}):
            if campos.get("propietario") == "Libre":
                propietario="Libre"
            elif campos.get("propietario") == nombreusuario:
                propietario="Propio"
            else:
                propietario="Oponente"

            parcela = {
                "name": campos.get("nombre_parcela"),
                "objeto": campos.get("objeto"), 
                "precio": campos.get("precio"),
                "tamano": campos.get("tamano"),
                "propietario":propietario,
                "ciudad":campos.get("nombre_ciudad"),
                "usuario":campos.get("propietario"),
            }
            parcelas.append(parcela)
        return parcelas
    
    def leer_parcelasPropia(self,nombreCiudad,nombreParcela,nombreUsuario):
        resultado = self.db_client.datosusuarios.find_one({'nombre': nombreUsuario})

        for ciudad_info in resultado['listaciudades']:
            if ciudad_info['nombre'] == nombreCiudad:
                for parcela in ciudad_info['listaparcelas']:
                    if parcela['nombre'] == nombreParcela:
                        #print(parcela)
                        return parcela
        return None

    def leer_parcelasRival(self,nombreCiudad,nombreParcela,nombreUsuario):
        campos=self.db_client.parcelas.find_one({'propietario': nombreUsuario,'nombre_ciudad': nombreCiudad,'nombre_parcela': nombreParcela })
        parcela = {
                "name": campos.get("nombre_parcela"),
                "objeto": campos.get("objeto"), 
                "precio": campos.get("precio"),
                "tamano": campos.get("tamano"),
                "propietario":campos.get("propietario"),
                "ciudad":campos.get("nombre_ciudad"),
                "usuario":campos.get("propietario"),
            }
        return parcela

    def leerTiendaPropia(self,nombreCiudad,nombreTienda,nombreUsuario):
        resultado = self.db_client.datosusuarios.find_one({'nombre': nombreUsuario})
        for ciudad_info in resultado['listaciudades']:
            if ciudad_info['nombre'] == nombreCiudad:
                for tienda in ciudad_info['listatiendas']:
                    if tienda['nombre'] == nombreTienda:
                        #print(tienda)
                        return tienda
        return None

    def leerTiendaRival(self,nombreCiudad,nombreTienda,nombreUsuario):
        campos=self.db_client.tiendas.find_one({'propietario': nombreUsuario,'nombre_ciudad': nombreCiudad,'nombre_tienda': nombreTienda })
        #print(campos)
        tienda = {
                "name": campos.get("nombre_tienda"),
                "precio": campos.get("precio"),
                "tamano": campos.get("tamano"),
                "propietario":campos.get("propietario"),
                "ciudad":campos.get("nombre_ciudad"),
                "usuario":campos.get("propietario"),
            }
        return tienda    
    
    def leerCasaPropia(self,nombreCiudad,nombreCasa,nombreUsuario):
        resultado = self.db_client.datosusuarios.find_one({'nombre': nombreUsuario})
        for ciudad_info in resultado['listaciudades']:
            if ciudad_info['nombre'] == nombreCiudad:
                #print(ciudad_info['casa'])
                campos=ciudad_info['casa']
                casa = {
                "name": campos.get("nombre"),
                "precio": campos.get("precio"),
                "prestigio": campos.get("prestigio"),
                "seguridad": campos.get("seguridad"),
                }
                #print(casa)
                return ciudad_info['casa']

        return None

    def leerCasaRival(self,nombreCiudad,nombreCasa,nombreUsuario):
        campos=self.db_client.casas.find_one({'propietario': nombreUsuario,'nombre_ciudad': nombreCiudad,'nombre_casa': nombreCasa })
        casa = {
                "name": campos.get("nombre_casa"),
                "precio": campos.get("precio"),
                "prestigio": campos.get("prestigio"),
                "propietario":campos.get("propietario"),
                "ciudad":campos.get("nombre_ciudad"),
                "usuario":campos.get("propietario"),
                "seguridad": campos.get("seguridad"),
            }
        return casa    

    def leer_fruterias(self,nombre_ciudad,nombreusuario):
        fruterias = []  # Usamos una lista para almacenar las ciudades
        for campos in self.db_client.tiendas.find({"nombre_ciudad": nombre_ciudad}):
            if campos.get("propietario") == "Libre":
                propietario="Libre"
            elif campos.get("propietario") == nombreusuario:
                propietario="Propio"
            else:
                propietario="Oponente"

            fruteria = {
                "name": campos.get("nombre_tienda"),
                "precio": campos.get("precio"),
                "tamano": campos.get("tamano"),
                "propietario":propietario,
                "coords": [campos.get("coordenadas_x"), campos.get("coordenadas_y")],
                "usuario":campos.get("propietario"),
            }
            #print(campos.get("coordenadas_x"), campos.get("coordenadas_y"))
            fruterias.append(fruteria)
        return fruterias
    
    def leer_casas(self,nombre_ciudad,nombreusuario):
        casas = []  
        for campos in self.db_client.casas.find({"nombre_ciudad": nombre_ciudad}):
            if campos.get("propietario") == "Libre":
                propietario="Libre"
            elif campos.get("propietario") == nombreusuario:
                propietario="Propio"
            else:
                propietario="Oponente"

            casa = {
                "name": campos.get("nombre_casa"),
                "precio": campos.get("precio"),
                "tamano": campos.get("tamano"),
                "propietario":propietario,
                "coords": [campos.get("coordenadas_x"), campos.get("coordenadas_y")],
                "usuario":campos.get("propietario"),
            }
            casas.append(casa)
        return casas

    def buscar_usuario(self,nombreusuario):
        usuario=self.db_client.usuarios.find_one({"nombre": nombreusuario})
        #print(usuario)
        return usuario
    
    def buscar_IDusuario(self,nombreusuario):
        usuario=self.db_client.datosusuarios.find_one({"nombre": nombreusuario})
        #print(usuario['_id'])
        return str(usuario['_id'])
    
    def obtener_usuario(self,nombreusuario):
        usuario=self.db_client.datosusuarios.find_one({"nombre": nombreusuario})
        return usuario
    
    def rellenarusuario(self,objetoUsuario):
        #print(objetoUsuario)
        self.db_client.datosusuarios.insert_one(objetoUsuario)
        return 

    def updateusuario(self,objetoUsuario):
        usuario_dict = json.loads(objetoUsuario.mostrar_informacion())
        self.db_client.datosusuarios.find_one_and_update({"nombre": usuario_dict["nombre"]}, { '$set': usuario_dict })
        return 
    
    def getItemsPlantaciones(self):
        itemsplantaciones = []  
        for plantacion in self.db_client.produccion_plantacion.find():
            itemsplantaciones.append({"nombre":plantacion.get("tipo_plantacion"),"urlicono":plantacion.get("urlicono")})  
        return itemsplantaciones
        
    def obtenerEmpleadosParados(self,nombre_ciudad):
        empleadoParados = []  
        for campos in self.db_client.empleados.find({"empleado_ciudad": nombre_ciudad}):
            if campos.get("Jefe") == "SinJefe":
                empleado = {
                    "nombre": campos.get("nombre_empleado"),
                    "precio": campos.get("precio_empleado"),
                    "comunicacion":campos.get("comunicacion"),
                    "estudios":campos.get("estudios"),
                    "fuerza":campos.get("fuerza"),
                    "liderazgo":campos.get("liderazgo"),
                }
                empleadoParados.append(empleado)
        #print(empleadoParados)    
        return empleadoParados
    
    def GetUsuarios(self):
        itemsusuarios = []  
        for usuarioobjeto in self.db_client.datosusuarios.find():
            itemsusuarios.append(usuarioobjeto)  
        return itemsusuarios

    def obtenerAlmacenInicial(self):
        datos = []  
        for producto in self.db_client.plantaciones.find():
            nuevo_producto = {
                "idpartida": producto.get("idpartida"),
                "tipo": producto.get("tipo"),
                "numero": producto.get("numero"),
                "precio": producto.get("precio"),
                "prodHectarea": producto.get("prodHectarea"),
                "totalano": producto.get("totalano"),
            }
            datos.append(nuevo_producto)  
        return datos
    
    def registrarse(self, usuario, contraseña):
        if self.db_client.usuarios.find_one({"nombre": usuario}) is None:
            nuevo_usuario = {
                "nombre": usuario,
                "password": contraseña
            }
            usuario_datos = {"nombre":usuario,"edad":33,"listaciudades":[],"prestigio":0.0,"dinero":obtenerDineroInicial(),"almacen":self.obtenerAlmacenInicial(),"id":"0"}
 
            self.db_client.usuarios.insert_one(nuevo_usuario)
            self.db_client.datosusuarios.insert_one(usuario_datos)
            usuario_objeto = self.db_client.datosusuarios.find_one({"nombre": usuario})

            # Verifica si se encontró un usuario con el nombre dado
            if usuario_objeto is not None:
                # Obtener el ObjectId
                oid_value = str(usuario_objeto["_id"])
                
                # Imprimir el valor del campo _id
                #print(oid_value)

                # Actualizar el documento para agregar el campo id
                self.db_client.datosusuarios.update_one(
                    {"nombre": usuario},
                    {"$set": {"id": oid_value}}
                    )
            else:
                print(f"No se encontró un usuario con el nombre {usuario}")
            return {"mensaje":"Usuario registrado exitosamente", "objetousuario":usuario_objeto}
        else:
            return {"mensaje":"El usuario ya existe", "objetousuario":{}}
        
    def cambiarSeguridadCasa(self,nombreciudad,nombreCasa,indice):
        self.db_client.casas.find_one_and_update({"nombre_casa": nombreCasa,"nombre_ciudad": nombreciudad}, { '$set': { "seguridad" : indice}})
        return

    def cambiarSeguridadTienda(self,nombreciudad,nombreTienda,indice):
        self.db_client.tiendas.find_one_and_update({"nombre_tienda": nombreTienda,"nombre_ciudad": nombreciudad}, { '$set': { "seguridad" : indice}})
        return

    def cambiarSeguridadParcela(self,nombreciudad,nombreParcela,indice):
        self.db_client.parcelas.find_one_and_update({"nombre_casa": nombreParcela,"nombre_ciudad": nombreciudad}, { '$set': { "seguridad" : indice}})
        return
    
    def cambiarCalidadTerreno(self,nombreciudad,nombreParcela,indice):
        self.db_client.parcelas.find_one_and_update({"nombre_casa": nombreParcela,"nombre_ciudad": nombreciudad}, { '$set': { "seguridad" : indice}})
        return
    
    """ def cambiarPropiedad(self,nombreUsuario,usuarioRival,nombreCiudad,lugar,tipo):
        resultado = self.db_client.datosusuarios.find_one({'nombre': usuarioRival})

        for ciudad_info in resultado['listaciudades']:
            if ciudad_info['nombre'] == nombreCiudad:
                if tipo == "parcela":
                    for parcela in ciudad_info['listaparcelas']:
                        if parcela['nombre'] == lugar:
                            return parcela
                if tipo == "tienda":
                    for tienda in ciudad_info['listatiendas']:
                        if tienda['nombre'] == lugar:
                            return tienda
        

        return None """

    def cerrar_conexion(self):
        campos=0

