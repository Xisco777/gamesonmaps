from Formulas import GetURL

class Plantacion():
    def __init__(self, tipoplantacion,factormultiplicacion,bbdd):
        self.tipo = tipoplantacion
        self.factormultiplicacion = factormultiplicacion
        self.produccionmes,self.urlicono = bbdd.obtener_informacion_produccion_platacion(tipoplantacion)
        self.urlicono =GetURL()+tipoplantacion+".PNG"
        self.select={ "nombre": self.tipo, "urlicono": self.urlicono }
       

    def mostrar_informacion(self):
        platacion_dict = {
            "tipo": self.tipo,
            "factormultiplicacion": self.factormultiplicacion,
            "produccionmes": self.produccionmes,
            "urlicono":self.urlicono,
            "select":{ "nombre": self.tipo, "urlicono": self.urlicono }
        }
        return platacion_dict
