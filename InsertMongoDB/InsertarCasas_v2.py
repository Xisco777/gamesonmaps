
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
   

pathBBDD = "mongodb+srv://fpratsquilez:GTdbIFamKljeyUvs@worldmanagergame.k3rozlq.mongodb.net/?retryWrites=true&w=majority"


listageojson=["Novelda"]
listanombrescasas=["Casa del Sol","Villa Serenidad","Rincón Acogedor","Morada Tranquila",
"Jardín Secreto","Refugio Verde","Pueblo Encantado","Rinconcito Azul","Palacio de Sueños","Cabaña del Bosque",
"Oasis de Paz","Escondite del Mar","Dulce Morada","Hogar de las Estrellas","Villa del Horizonte"]

# Leer el archivo .xls
df = pd.read_excel('C:/Users/xisco/Documents/GameManagerWorld/DatosJuego/listaMunicipios.xls')

# Crear una lista para almacenar los registros en el formato JSON que deseas
registros_json = []
db = DatabaseManager(pathBBDD)
# Iterar sobre cada fila del DataFrame
for index2, row in df.iterrows():
    casas = []
    ciudad=row['Población']
    ruta_archivo = f'C:/Users/xisco/Documents/GameManagerWorld/DatosJuego/{ciudad}Casas.geojson'
    
    # Si el GeoJSON está en un archivo
    # with open(ruta_archivo, 'r') as archivo:
    #     geojson = json.load(archivo)

       # Iterar sobre todos los features
    # for index,feature in enumerate(geojson['features']):
    #     precio=random.randint(25000, 120000)
    #     json={
    #         "id": index,
    #         "nombre_casa":random.choice(listanombrescasas),
    #         "nombre_ciudad":ciudad,
    #         "precio":precio,
    #         "prestigio":int(precio/10000),
    #         "propietario":"Libre",
    #         "coordenadas_x":feature['geometry']['coordinates'][1],
    #         "coordenadas_y":feature['geometry']['coordinates'][0],
    #         "seguridad":0
    #     }
    numero_aleatorio = random.uniform(-0.001, 0.001)

    print(numero_aleatorio)
    for index in range(row['NumeroCasas']):
        precio=random.randint(25000, 120000)
        json={
            "id": index,
            "nombre_casa":random.choice(listanombrescasas),
            "nombre_ciudad":ciudad,
            "precio":precio,
            "prestigio":int(precio/10000),
            "propietario":"Libre",
            "coordenadas_x":row['Latitud']+random.uniform(-0.003, 0.003),
            "coordenadas_y":row['Longitud']+random.uniform(-0.003, 0.003),
            "seguridad":0
        }
        casas.append(json)
    print(casas)
    
    db.insert_casas(casas)

# db = DatabaseManager(pathBBDD)   
#db.deleteallcasas()
