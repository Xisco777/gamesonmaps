from pymongo import MongoClient
import json
import pandas as pd
class DatabaseManager:
    def __init__(self, db_name):
        self.db_client = MongoClient(db_name).test

    def insert_ciudades(self, ciudades):
        self.db_client.ciudades.insert_many(ciudades)
    
    def eliminar_ciudades(self):
        self.db_client.ciudades.delete_many({})

empleados = []
pathBBDD = "mongodb+srv://fpratsquilez:GTdbIFamKljeyUvs@worldmanagergame.k3rozlq.mongodb.net/?retryWrites=true&w=majority"


# Leer el archivo .xls
df = pd.read_excel('C:/Users/xisco/Documents/GameManagerWorld/DatosJuego/listaMunicipios.xls')

# Crear una lista para almacenar los registros en el formato JSON que deseas
registros_json = []

# Iterar sobre cada fila del DataFrame
for index, row in df.iterrows():
    registro = {
        "id": index + 1,
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

print(registros_json)
db = DatabaseManager(pathBBDD)
db.insert_ciudades(registros_json)
# db = DatabaseManager(pathBBDD)
# db.insert_enpleadoselectronica(empleados)
