from pymongo import MongoClient


class DatabaseManager:
    def __init__(self, db_name):
        self.db_client=MongoClient(db_name).test

    def insert_enpleadoselectronica(self, empleadoselectronica):
        self.db_client.empresas.insert_many(empleadoselectronica)


pathBBDD="mongodb+srv://fpratsquilez:GTdbIFamKljeyUvs@worldmanagergame.k3rozlq.mongodb.net/?retryWrites=true&w=majority"

# tengo la siguiente variable en python: empleadoselectronica=[{"id":3,"nombre_empleado":"Toni","empleado_ciudad":"Utiel","productividad_empleado":0.5,"precio_empleado":2160,"tipo":"SW"}]
# tipo puede ser: HW, FW, SW, Produccion, Testing, Gestion, Mecanica. empleado_ciudad quiero que siempre sea Utiel, prodias crear una lista de 10 personas

db = DatabaseManager(pathBBDD)
empleadoselectronica = [
    {"id": 1, "nombre_empresa": "Juan", "nombre_ciudad": "Utiel", "tamano": 15, "precio": 800000},
   ]
db.insert_enpleadoselectronica(empleadoselectronica)
