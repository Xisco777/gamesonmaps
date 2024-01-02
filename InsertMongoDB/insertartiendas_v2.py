
from area import area
import json 
import random
from pymongo import MongoClient
import json
import pandas as pd

class DatabaseManager:
    def __init__(self, db_name):
        self.db_client = MongoClient(db_name).test

    def insert_tiendas(self, tiendas):
        self.db_client.tiendas.insert_many(tiendas)
    def deletealltiendas(self):
        self.db_client.tiendas.delete_many({})

pathBBDD = "mongodb+srv://fpratsquilez:GTdbIFamKljeyUvs@worldmanagergame.k3rozlq.mongodb.net/?retryWrites=true&w=majority"

tiendas = []

listanombrestiendas=["Delicias Gourmet",
"Abasto Fresco",
"Mercado Sabroso",
"Sabor Natural",
"Rincón Delicatessen",
"La Despensa de Sabores",
"Selección de Sabores",
"Gusto en Casa",
"La Cocina de Tradición",
"Rincón Gastronómico",
"Alimenta Bienestar",
"Bocado de Sazón",
"Comida con Amor",
"Delicias de la Tierra",
"Sabores del Mundo"]

# Leer el archivo .xls
df = pd.read_excel('C:/Users/xisco/Documents/GameManagerWorld/DatosJuego/listaMunicipios.xls')
db = DatabaseManager(pathBBDD)
# Crear una lista para almacenar los registros en el formato JSON que deseas
registros_json = []

# Iterar sobre cada fila del DataFrame
for index2, row in df.iterrows():
    ciudad=row['Población']
    ruta_archivo = f'C:/Users/xisco/Documents/GameManagerWorld/DatosJuego/{ciudad}Casas.geojson'
    tiendas= []
        # Iterar sobre todos los features
    for index in range(row['NumeroTiendas']):

        precio=random.randint(25000, 120000)        
        json={
                "id": index,
                "nombre_tienda":random.choice(listanombrestiendas),
                "nombre_ciudad":ciudad,
                "tamano":int(precio/5000),
                "precio":precio,
                "propietario":"Libre",
                "coordenadas_x":row['Latitud']+random.uniform(-0.003, 0.003),
                "coordenadas_y":row['Longitud']+random.uniform(-0.003, 0.003),
                "seguridad":0
            }
        tiendas.append(json)
    print(tiendas)
    
    db.insert_tiendas(tiendas)  

# db = DatabaseManager(pathBBDD)   
#db.deletealltiendas()