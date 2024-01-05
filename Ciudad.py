from Parcela import Parcela
from Tienda import Tienda
from Casa import Casa

class Ciudad():
    def __init__(self, nombre, bbdd):
        self.nombre = nombre
        poblacion, coordenadas_x, coordenadas_y, idioma_principal,indiceproductos = bbdd.obtener_informacion_ciudad(nombre)
        self.poblacion = poblacion
        self.ubicacion = (coordenadas_x, coordenadas_y)
        self.idioma_principal = idioma_principal
        self.listatiendas = []
        self.listaparcelas = []
        self.casa: Casa = None
        self.factorMultiplicacionProducto = indiceproductos
        self.prestigioCasa=0
 
    def mostrar_informacion(self):
        arrayTiendas = []
        arrayParcelas = []
        casavariable = ""
        for parcela in self.listaparcelas:
            arrayParcelas.append(parcela.mostrar_informacion())
        for tienda in self.listatiendas:
            arrayTiendas.append(tienda.mostrar_informacion())
        if self.casa != None:
            casavariable=self.casa.mostrar_informacion()  
        ciudad_dict = {
            "nombre": self.nombre,
            "poblacion": self.poblacion,
            "ubicacion": self.ubicacion,
            "idioma_principal": self.idioma_principal,
            "listatiendas": arrayTiendas,
            "listaparcelas": arrayParcelas,
            "casa": casavariable,
            "factorMultiplicacionProducto": self.factorMultiplicacionProducto,
            "prestigioCasa": self.prestigioCasa,
        }   
        return ciudad_dict
    
    def comprar_parcela(self, nombre_parcela, bbdd):
        parcela=Parcela(nombre_parcela,self.nombre,self.factorMultiplicacionProducto,bbdd)
        self.listaparcelas.append(parcela)
        return parcela.precio
    
    def eliminar_y_obtener_parcela_por_nombre(self, nombreparcela):
        for index, parcela in enumerate(self.listaparcelas):
            if parcela.nombre == nombreparcela:
                self.listaparcelas.pop(index)
                return parcela
    
    def añadir_parcela(self, parcela):
        self.listaparcelas.append(parcela)
        return 

    def comprar_tienda(self, nombretienda, bbdd):
        tienda=Tienda(nombretienda,self.nombre,bbdd)
        self.listatiendas.append(tienda)
        return tienda.precio, tienda.prestigio
    
    def eliminar_y_obtener_tienda_por_nombre(self,nombretienda):
        for index, tienda in  enumerate(self.listatiendas):
            if tienda.nombre==nombretienda:
                self.listatiendas.pop(index)
                return tienda

    def añadir_tienda(self, tienda):
        self.listatiendas.append(tienda)
        return
    
    def comprar_casa(self, nombrecasa, bbdd):
        self.casa = Casa(nombrecasa,self.nombre,bbdd)
        self.prestigioCasa=self.casa.prestigio