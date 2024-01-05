
from area import area
import json 
import random
from pymongo import MongoClient
import json
import pandas as pd

class DatabaseManager:
    def __init__(self, db_name):
        self.db_client = MongoClient(db_name).test

    def insert_casas(self, casas):
        self.db_client.casas.insert_many(casas)
    def deleteallcasas(self):
        self.db_client.casas.delete_many({})
    def insert_tiendas(self, tiendas):
        self.db_client.tiendas.insert_many(tiendas)
    def deletealltiendas(self):
        self.db_client.tiendas.delete_many({})   
    def insert_empleados(self, empleados):
        self.db_client.empleados.insert_many(empleados)
    def deleteallempleados(self):
        self.db_client.empleados.delete_many({})
    def insert_enpleadoselectronica(self, parcelas):
        self.db_client.parcelas.insert_many(parcelas)
    def deleteallparcelas(self):
        myquery = {}
        self.db_client.parcelas.delete_many(myquery)
    def insert_ciudades(self, ciudades):
        self.db_client.ciudades.insert_many(ciudades) 
    def eliminar_ciudades(self):
        self.db_client.ciudades.delete_many({}) 
    def insert_plantaciones(self, plantacion):
        self.db_client.plantaciones.insert_one(plantacion)
    def deleteallplantaciones(self):
        self.db_client.plantaciones.delete_many({})
    def deleteallproduccion_plantacion(self):
        self.db_client.produccion_plantacion.delete_many({})
    def insert_produccion_plantacion(self, empleados):
        self.db_client.produccion_plantacion.insert_many(empleados)
        
pathBBDD = "mongodb+srv://fpratsquilez:GTdbIFamKljeyUvs@worldmanagergame.k3rozlq.mongodb.net/?retryWrites=true&w=majority"


nombres = ['Sofía', 'Daniel', 'Lucía', 'Martín', 'María', 'Pablo', 'Andrea', 'Mateo', 'Julia', 'Alejandro', 'Valentina', 'David', 'Sara', 'Hugo', 'Laura', 'Adrián', 'Paula', 'Álvaro', 'Elena', 'Diego']
nombres_aleatorios = random.sample(nombres, 20)
apellidos = ['García', 'Fernández', 'González', 'López', 'Martínez', 'Sánchez', 'Pérez', 'Martín', 'Gómez', 'Ruiz', 'Hernández', 'Jiménez', 'Díaz', 'Moreno', 'Álvarez', 'Muñoz', 'Romero', 'Alonso', 'Gutiérrez', 'Navarro']
apellidos_aleatorios = random.sample(apellidos, 20)
apellidos2 = ['García', 'Fernández', 'González', 'López', 'Martínez', 'Sánchez', 'Pérez', 'Martín', 'Gómez', 'Ruiz', 'Hernández', 'Jiménez', 'Díaz', 'Moreno', 'Álvarez', 'Muñoz', 'Romero', 'Alonso', 'Gutiérrez', 'Navarro']
apellidos_aleatorios2 = random.sample(apellidos2, 20)
# Leer el archivo .xls
df = pd.read_excel('C:/Users/xisco/Documents/GameManagerWorld/DatosJuego/listaMunicipios.xls')

# Crear una lista para almacenar los registros en el formato JSON que deseas
registros_json = []
db = DatabaseManager(pathBBDD)
db.deleteallcasas()
db.deletealltiendas()
db.deleteallempleados()
db.deleteallparcelas()
db.eliminar_ciudades()
db.deleteallplantaciones()
db.deleteallproduccion_plantacion()

# Crear una lista para almacenar los registros en el formato JSON que deseas
registros_json = []
idpartida=1
# Iterar sobre cada fila del DataFrame
for index3, row in df.iterrows():
    registro = {
        "idpartida":idpartida,
        "id": index3 + 1,
        "nombre": row['Población'],
        "poblacion": row['Habitantes'],
        "coordenadas_x": row['Latitud'],
        "coordenadas_y": row['Longitud'],
        "idioma_principal": "Español",  # Puedes cambiar esto según tus necesidades
        "indice_productos": row['Productos'],
        "radio": 10000,  # Puedes cambiar esto según tus necesidades
        "descripcion": row['Descripcion']
    }
    registros_json.append(registro)

db.insert_ciudades(registros_json)

# Iterar sobre cada fila del DataFrame
for index2, row in df.iterrows():

    ciudad=row['Población']
    ruta_archivo = f'C:/Users/xisco/Documents/GameManagerWorld/DatosJuego/{ciudad}Plantaciones.geojson'
    with open(ruta_archivo, 'r') as archivo:
        geojson = json.load(archivo)

    listanombrescasas=["Casa del Sol","Villa Serenidad","Rincón Acogedor","Morada Tranquila",
    "Jardín Secreto","Refugio Verde","Pueblo Encantado","Rinconcito Azul","Palacio de Sueños","Cabaña del Bosque",
    "Oasis de Paz","Escondite del Mar","Dulce Morada","Hogar de las Estrellas","Villa del Horizonte"]

    listanombrestiendas=["Delicias Gourmet","Abasto Fresco","Mercado Sabroso","Sabor Natural","Rincón Delicatessen","La Despensa de Sabores","Selección de Sabores",
    "Gusto en Casa","La Cocina de Tradición","Rincón Gastronómico","Alimenta Bienestar","Bocado de Sazón","Comida con Amor",
    "Delicias de la Tierra","Sabores del Mundo"]

    listanombresparcela = ["El Vergel Verde", "Tierra Fértil", "La Granja Encantada", "Campo Dorado",  "La Huerta Serena", "El Oasis Agrícola", "Finca Bella Vista", 
                       "Rancho Aromático", "Cosecha de Sueños", "Jardín de la Abundancia",  "La Colina Productiva", "Granja Armoniosa", "La Parcela del Sol",  "Vereda del Trigo", "Tierras de Esperanza", "Campo Estelar", 
                       "Rincón Productivo", "Huerto de los Sueños", "Lugar de la Cosecha",  "Prado Tranquilo", "Rincón de la Abundancia", "Cosecha Dorada", 
                       "Granja de Ensueño", "Tierra de Promesas", "Campo Sereno",  "El Rincón Fructífero", "Finca del Amanecer", "Villa de la Cosecha", 
                       "Rancho de la Paz", "Jardín del Sol Naciente", "Verde Horizonte",  "El Huerto Encantado", "Lugar de la Prosperidad", "Rincón Agrario",
                       "Finca del Sueño Azul", "Campo de las Estrellas", "Granja Tranquila", "Tierras Fértiles del Este", "Cosecha de la Aurora", "Huerto de la Serenidad", 
                       "Prado de la Armonía", "Parcela del Sueño Perenne", "Rancho de la Abundancia",  "Campos Dorados del Oeste", "Jardín de la Eterna Primavera", 
                       "Granja de la Brisa Fresca", "Villa de la Plenitud",  "Rincón de la Cosecha Bendita", "Finca del Sol Radiante", 
                       "Tierras de la Tranquilidad", "Campo de la Luna Llena",  "Huerto de los Vientos Cálidos", "Lugar de la Cosecha Feliz", 
                       "Prado de la Dulce Serenata", "El Oasis del Verdor",  "Granja del Horizonte Dorado", "Parcela de la Aurora Boreal", 
                       "Rancho de los Sueños Realizados", "Jardín de la Felicidad Infinita",  "Vereda de la Plenitud Interior", "Finca de los Días Radiantes",
                       "Tierras de la Riqueza Abundante", "Campo de la Tranquilidad Eterna", "Huerto del Destino Brillante", "Lugar de la Cosecha Mágica",
                       "Prado de la Alegría Perpetua", "El Oasis de la Armonía", "Granja de los Sueños Florecientes", "Parcela de la Prosperidad Infinita",
                       "Rancho del Pleno Bienestar", "Jardín del Éxito Continuo", "Vereda de la Abundancia Sin Fin", "Finca de la Plenitud Absoluta",
                       "Tierras del Bienestar Duradero", "Campo de la Alegría Eterna", "Huerto del Éxito Ininterrumpido", "Lugar de la Cosecha Prodigiosa",
                       "Prado de la Felicidad Ilimitada", "El Oasis de la Prosperidad Perenne",  "Granja de los Sueños Duraderos", "Parcela de la Plenitud Infinita",
                       "Rancho del Gozo Incesante", "Jardín de la Abundancia Ilimitada", "Vereda de la Riqueza Interminable", "Finca del Bienestar Completo",
                       "Tierras de la Felicidad Sin Fin", "Campo de la Prosperidad Perpetua", "Huerto del Éxito Duradero", "Lugar de la Cosecha Inagotable",
                       "Prado de la Abundancia Duradera", "El Oasis del Gozo Eterno", "Granja de los Sueños Incesantes", "Parcela de la Riqueza Interminable",
                       "Rancho del Bienestar Absoluto", "Jardín del Pleno Gozo", "Vereda de la Plenitud Duradera"]
    parcelas = []
       # Iterar sobre todos los features
    for feature in geojson['features']:
        nombreParcela=random.choice(listanombresparcela)
        listanombresparcela.remove(nombreParcela)

        print(int(area(feature['geometry'])/10000))
       
        feature['properties']['name']="Libre"
        feature['properties']['tipo']="Parcela"        
        jsonn={
            "idpartida":idpartida,
            "objeto":[{"type":"FeatureCollection","features":[feature]}],
            "nombre_ciudad":ciudad,
            "nombre_parcela":nombreParcela,
            "precio":int(area(feature['geometry'])/10000)*random.randint(20000, 35000),
            "tamano":int(area(feature['geometry'])/10000),
            "propietario":"Libre",
            "numeroplantaciones":random.randint(4, 10)
        }
        parcelas.append(jsonn)
    print(parcelas)
    db.insert_enpleadoselectronica(parcelas)


    casas = []
    ciudad=row['Población']
    numero_aleatorio = random.uniform(-0.001, 0.001)

    print(numero_aleatorio)
    for index in range(row['NumeroCasas']):
        nombreCasa=random.choice(listanombrescasas)
        listanombrescasas.remove(nombreCasa)
        precio=random.randint(40000, 160000)
        jsoncasa={
            "idpartida":idpartida,
            "id": index,
            "nombre_casa":nombreCasa,
            "nombre_ciudad":ciudad,
            "precio":precio,
            "prestigio":int(precio/10000),
            "propietario":"Libre",
            "coordenadas_x":row['Latitud']+random.uniform(-0.003, 0.003),
            "coordenadas_y":row['Longitud']+random.uniform(-0.003, 0.003),
            "seguridad":0
        }
        casas.append(jsoncasa)
    print(casas)
    
    db.insert_casas(casas)

    tiendas= []
        # Iterar sobre todos los features
    for index in range(row['NumeroTiendas']):
        nombreTienda=random.choice(listanombrestiendas)
        listanombrestiendas.remove(nombreTienda)
        precio=random.randint(40000, 250000)        
        jsontienda={
                "idpartida":idpartida,
                "id": index,
                "nombre_tienda":nombreTienda,
                "nombre_ciudad":ciudad,
                "tamano":int(precio/6000),
                "precio":precio,
                "propietario":"Libre",
                "coordenadas_x":row['Latitud']+random.uniform(-0.003, 0.003),
                "coordenadas_y":row['Longitud']+random.uniform(-0.003, 0.003),
                "seguridad":0,
                "prestigio":int(precio/10000),
                "numeroMaximoEmpleados":int(precio/50000)+1
            }
        tiendas.append(jsontienda)
    print(tiendas)
    
    db.insert_tiendas(tiendas)

    empleados = []
    ciudad=row['Población']
    for index in range(row['NumeroEmpleados']):
        comunicacion = random.randint(0, 5)
        estudios = random.randint(0, 5)
        fuerza = random.randint(0, 5)
        liderazgo = random.randint(0, 5)
        salario=(comunicacion*150)+(fuerza*150)+(liderazgo*300)+(estudios*350)
        nombre=random.choice(nombres_aleatorios) + " " + random.choice(apellidos_aleatorios) + " " + random.choice(apellidos_aleatorios2) 
        jsonemp={
            "idpartida":idpartida,
            "id": index,
            "nombre_empleado": nombre,
            "empleado_ciudad": ciudad,
            "precio_empleado": salario,
            "Jefe": "SinJefe",
            "Lugar": "Libre",
            "comunicacion": comunicacion,
            "estudios": estudios,
            "fuerza": fuerza,
            "liderazgo": liderazgo
        }
        empleados.append(jsonemp)
        
    db.insert_empleados(empleados)
 
 # Leer el archivo .xls haceeeeer
df = pd.read_excel('C:/Users/xisco/Documents/GameManagerWorld/DatosJuego/listaProductos.xls')

# Iterar sobre cada fila del DataFrame
for index3, row in df.iterrows():
    casas = []
    producto=row['Producto']
    jsonn={"idpartida":idpartida,"tipo": row['Producto'], "numero": row['CantidadInicial'], "precio":row['PrecioKilo'],"prodHectarea":row['prodHectarea'],"totalano":row['totalano']}
    db.insert_plantaciones(jsonn) 
    jsonpro_plant= {
        "id": index3,
        "tipo_plantacion": row['Producto'],
        "enero": row['Enero'],
        "febrero": row['Febrero'],
        "marzo": row['Marzo'],
        "abril": row['Abril'],
        "mayo": row['Mayo'],
        "junio": row['Junio'],
        "julio": row['Julio'],
        "agosto": row['Agosto'],
        "septiembre": row['Septiembre'],
        "octubre": row['Octubre'],
        "noviembre": row['Noviembre'],
        "diciembre": row['Diciembre'],
        "urlicono": ""
        }
    db.insert_produccion_plantacion(jsonpro_plant)   
