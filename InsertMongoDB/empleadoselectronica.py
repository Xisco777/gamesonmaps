from pymongo import MongoClient


class DatabaseManager:
    def __init__(self, db_name):
        self.db_client=MongoClient(db_name).test

    def insert_enpleadoselectronica(self, empleadoselectronica):
        self.db_client.empleados_electronica.insert_many(empleadoselectronica)


pathBBDD="mongodb+srv://fpratsquilez:GTdbIFamKljeyUvs@worldmanagergame.k3rozlq.mongodb.net/?retryWrites=true&w=majority"

# tengo la siguiente variable en python: empleadoselectronica=[{"id":3,"nombre_empleado":"Toni","empleado_ciudad":"Utiel","productividad_empleado":0.5,"precio_empleado":2160,"tipo":"SW"}]
# tipo puede ser: HW, FW, SW, Produccion, Testing, Gestion, Mecanica. empleado_ciudad quiero que siempre sea Utiel, prodias crear una lista de 10 personas

db = DatabaseManager(pathBBDD)
empleadoselectronica = [
    {"id": 4, "nombre_empleado": "Juan", "empleado_ciudad": "Utiel", "productividad_empleado": 0.6, "precio_empleado": 2000, "tipo": "HW"},
    {"id": 5, "nombre_empleado": "Maria", "empleado_ciudad": "Utiel", "productividad_empleado": 0.8, "precio_empleado": 3000, "tipo": "FW"},
    {"id": 6, "nombre_empleado": "Toni", "empleado_ciudad": "Utiel", "productividad_empleado": 0.5, "precio_empleado": 1860, "tipo": "SW"},
    {"id": 7, "nombre_empleado": "Laura", "empleado_ciudad": "Utiel", "productividad_empleado": 0.7, "precio_empleado": 2300, "tipo": "Produccion"},
    {"id": 8, "nombre_empleado": "Carlos", "empleado_ciudad": "Utiel", "productividad_empleado": 0.9, "precio_empleado": 3500, "tipo": "Testing"},
    {"id": 9, "nombre_empleado": "Sara", "empleado_ciudad": "Utiel", "productividad_empleado": 0.6, "precio_empleado": 2100, "tipo": "Gestion"},
    {"id": 10, "nombre_empleado": "Daniel", "empleado_ciudad": "Utiel", "productividad_empleado": 0.8, "precio_empleado": 2400, "tipo": "Mecanica"},
    {"id": 11, "nombre_empleado": "Ana", "empleado_ciudad": "Utiel", "productividad_empleado": 0.7, "precio_empleado": 2200, "tipo": "FW"},
    {"id": 12, "nombre_empleado": "Luis", "empleado_ciudad": "Utiel", "productividad_empleado": 0.5, "precio_empleado": 1700, "tipo": "SW"},
    {"id": 13, "nombre_empleado": "Elena", "empleado_ciudad": "Utiel", "productividad_empleado": 0.6, "precio_empleado": 2100, "tipo": "Produccion"}
]
db.insert_enpleadoselectronica(empleadoselectronica)
