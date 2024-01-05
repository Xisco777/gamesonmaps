
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
        self.db_client.plantaciones.insert_one(casas)
    def deleteallcasas(self):
        self.db_client.plantaciones.delete_many({})
    
    def prueba(self,indice):
        self.db_client.datosusuarios.find_one_and_update({"nombre": "Fran"}, { '$set': { "almacen" : indice} })
   

pathBBDD = "mongodb+srv://fpratsquilez:GTdbIFamKljeyUvs@worldmanagergame.k3rozlq.mongodb.net/?retryWrites=true&w=majority"


listageojson=["Novelda"]


# Leer el archivo .xls
df = pd.read_excel('C:/Users/xisco/Documents/GameManagerWorld/DatosJuego/listaProductos.xls')

# Crear una lista para almacenar los registros en el formato JSON que deseas
registros_json = []
db = DatabaseManager(pathBBDD)
casas = []
idpartida=1
# Iterar sobre cada fila del DataFrame
for index2, row in df.iterrows():

    producto=row['Producto']
    jsonn={"idpartida":idpartida,"tipo": row['Producto'], "numero": row['CantidadInicial'], "precio":row['PrecioKilo'], "prodHectarea":row['prodHectarea'],"totalano":row['totalano']}
    casas.append(jsonn)
    db.insert_casas(jsonn)

#db.prueba(casas)
  
#db.deleteallcasas()
