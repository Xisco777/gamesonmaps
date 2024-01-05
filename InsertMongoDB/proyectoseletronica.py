from pymongo import MongoClient


class DatabaseManager:
    def __init__(self, db_name):
        self.db_client=MongoClient(db_name).test

    def insert_enpleadoselectronica(self, empleadoselectronica):
        self.db_client.proyectos_electronica.insert_many(empleadoselectronica)


pathBBDD="mongodb+srv://fpratsquilez:GTdbIFamKljeyUvs@worldmanagergame.k3rozlq.mongodb.net/?retryWrites=true&w=majority"

# tengo la siguiente variable en python: empleadoselectronica=[{"id":3,"nombre_empleado":"Toni","empleado_ciudad":"Utiel","productividad_empleado":0.5,"precio_empleado":2160,"tipo":"SW"}]
# tipo puede ser: HW, FW, SW, Produccion, Testing, Gestion, Mecanica. empleado_ciudad quiero que siempre sea Utiel, prodias crear una lista de 10 personas

db = DatabaseManager(pathBBDD)
empleadoselectronica = [
    {"id": 1, "nombreproyecto": "Prueba", "descripcion": "", "relevancia": 0.01, "presupuesto": 120000, "numeroempleadosHW": 2,"numeroempleadosFW": 2,"numeroempleadosSW": 2,"numeroempleadosProduccion": 2,"numeroempleadosTesting": 2, "numeroempreadosMecanica": 2,"numeroepleadosGestion": 2,"duracionmeses": 10,"dificultad": 0.6,"tipo": "Cliente","producto": "","numeroproductos": 0},
   ]

db.insert_enpleadoselectronica(empleadoselectronica)
