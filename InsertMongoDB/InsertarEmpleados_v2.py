
from area import area
import json 
import random
from pymongo import MongoClient
import json
import pandas as pd

class DatabaseManager:
    def __init__(self, db_name):
        self.db_client = MongoClient(db_name).test

    def insert_empleados(self, empleados):
        self.db_client.empleados.insert_many(empleados)
    def deleteallempleados(self):
        self.db_client.empleados.delete_many({})
   

pathBBDD = "mongodb+srv://fpratsquilez:GTdbIFamKljeyUvs@worldmanagergame.k3rozlq.mongodb.net/?retryWrites=true&w=majority"

nombres = ['Sofía', 'Daniel', 'Lucía', 'Martín', 'María', 'Pablo', 'Andrea', 'Mateo', 'Julia', 'Alejandro', 'Valentina', 'David', 'Sara', 'Hugo', 'Laura', 'Adrián', 'Paula', 'Álvaro', 'Elena', 'Diego']

nombres_aleatorios = random.sample(nombres, 20)

print(nombres_aleatorios)

apellidos = ['García', 'Fernández', 'González', 'López', 'Martínez', 'Sánchez', 'Pérez', 'Martín', 'Gómez', 'Ruiz', 'Hernández', 'Jiménez', 'Díaz', 'Moreno', 'Álvarez', 'Muñoz', 'Romero', 'Alonso', 'Gutiérrez', 'Navarro']

apellidos_aleatorios = random.sample(apellidos, 20)

print(apellidos_aleatorios)

# Leer el archivo .xls
df = pd.read_excel('C:/Users/xisco/Documents/GameManagerWorld/DatosJuego/listaMunicipios.xls')

# Crear una lista para almacenar los registros en el formato JSON que deseas


db = DatabaseManager(pathBBDD)

# Iterar sobre cada fila del DataFrame
for index2, row in df.iterrows():
    print("dsd")
    empleados = []
    ciudad=row['Población']
    for index in range(row['NumeroEmpleados']):
        comunicacion = random.randint(0, 5)
        estudios = random.randint(0, 5)
        fuerza = random.randint(0, 5)
        liderazgo = random.randint(0, 5)
        salario=(comunicacion*100)+(fuerza*100)+(liderazgo*250)+(estudios*300)
        nombre=random.choice(nombres_aleatorios) + " " + random.choice(apellidos_aleatorios)
        json={
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
        empleados.append(json)
        
    db.insert_empleados(empleados)
    #print(empleados)
# db = DatabaseManager(pathBBDD)   
#db.deleteallempleados()
