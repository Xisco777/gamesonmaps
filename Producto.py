from Formulas import GetURL

class Producto():
    def __init__(self, tipoproducto):
        self.tipo = tipoproducto
        self.urlicono =GetURL()+tipoproducto+".PNG"
        self.select={ "nombre": self.tipo, "urlicono": self.urlicono }
        #añadir parametro factor localizacion

    def mostrar_informacion(self):
        producto_dict = {
            "tipo": self.tipo,
            "urlicono":self.urlicono,
            "select":{ "nombre": self.tipo, "urlicono": self.urlicono }
        }
        return producto_dict