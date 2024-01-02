
from Plantacion import Plantacion
from Empleados import Empleados
import random
from Formulas import indiceProductividadEmpleadosParcelas, GetHectareasPorEmpleado,Getfactormultiplicacion,GetURL
import math

class Parcela():
    def __init__(self, nombreparcela, nombreciudad, factorMultiplicacionProducto,bbdd):
        self.nombre = nombreparcela
        precio,tamaño,numeroplantaciones = bbdd.obtener_informacion_parcela(nombreparcela,nombreciudad)
        self.tamaño = tamaño
        self.precio = precio
        self.listaplantacion = []
        self.listaempleados = []
        self.factorMultiplicacionProducto = factorMultiplicacionProducto.split(",")
        self.numeroEmpleados = 0
        self.numeroMaximoEmpleados = math.ceil(tamaño/GetHectareasPorEmpleado())
        self.indiceproduccionempleados = 0
        self.calidadterreno = math.ceil(random.uniform(0, 3))
        self.ciudadParcela = nombreciudad
        self.indiceproductividadempleados = 0
        self.seguridad = 0
        self.maximaSeguridad = 3
        self.numeroplantaciones = numeroplantaciones
        for _ in range(numeroplantaciones):
            self.agregar_plantacion("Libre", bbdd)
        self.habilitacionproduccionmes=True

    def mostrar_informacion(self):
        arrayPlantacion=[]
        arrayEmpleados=[]
        for plantacion in self.listaplantacion:
            arrayPlantacion.append(plantacion.mostrar_informacion())
        for empleado in self.listaempleados:
            arrayEmpleados.append(empleado.mostrar_informacion())
        calidadterrenofrase="Mala Calidad"
        if(self.calidadterreno==0):
            calidadterrenofrase="Mala Calidad"
        if(self.calidadterreno==1):
            calidadterrenofrase="Calidad Media" 
        if(self.calidadterreno==2):
            calidadterrenofrase="Buena Calidad"   
        if(self.calidadterreno==3):
            calidadterrenofrase="Calidad Excelente"  
        parcela_dict = {
            "nombre": self.nombre,
            "tamaño": self.tamaño,
            "precio": self.precio,
            "listaplantacion": arrayPlantacion,
            "listaempleados": arrayEmpleados,
            "factorMultiplicacionProducto": self.factorMultiplicacionProducto,
            "numeroEmpleados": self.numeroEmpleados,
            "numeroMaximoEmpleados": self.numeroMaximoEmpleados,
            "indiceproduccionempleados": self.indiceproduccionempleados,
            "calidadterreno": self.calidadterreno,
            "ciudadParcela": self.ciudadParcela,
            "indiceproductividadempleados": self.indiceproductividadempleados,
            "seguridad": self.seguridad,
            "maximaSeguridad": self.maximaSeguridad,
            "numeroplantaciones": self.numeroplantaciones,
            "calidadterrenofrase":calidadterrenofrase,
        }
        return parcela_dict
    

    def agregar_plantacion(self,tipoplantacion,bbdd):
        factormultiplicacion=1
        for factor in self.factorMultiplicacionProducto:
            if (tipoplantacion == factor):
                factormultiplicacion=Getfactormultiplicacion()
        plantacion=Plantacion(tipoplantacion,factormultiplicacion,bbdd)
        self.listaplantacion.append(plantacion)

    def modificar_plantacion(self, index, tipoplantacion,bbdd):
        factormultiplicacion=1
        for factor in self.factorMultiplicacionProducto:
            if (tipoplantacion == factor):
                factormultiplicacion=Getfactormultiplicacion()
        plantacion=self.listaplantacion[index]
        plantacion.tipo=tipoplantacion
        plantacion.urlicono=GetURL()+tipoplantacion+".PNG"
        plantacion.factormultiplicacion=factormultiplicacion
        plantacion.produccionmes = bbdd.obtener_informacion_produccion_platacion_meses(tipoplantacion)
        self.listaplantacion[index] = plantacion

    def contratar_empleado(self,nombre_empleado, bbdd):
        notify={ "mensaje":"Empleado contratado con exito","tipo":"success"}
        if self.numeroEmpleados < self.numeroMaximoEmpleados:
            self.numeroEmpleados += 1
        else:
            notify={"mensaje":"No se puede contratar a mas empleados","tipo":"info"}
            return notify
            return
        self.indiceproduccionempleados = self.numeroEmpleados/self.numeroMaximoEmpleados
        empleado=Empleados(nombre_empleado,self.ciudadParcela, bbdd)
        self.listaempleados.append(empleado)
        productividad=0
        for empleado in self.listaempleados:
            productividad=productividad + empleado.fuerza
        self.indiceproductividadempleados = indiceProductividadEmpleadosParcelas(productividad,self.numeroEmpleados)
        return notify

    def despedir_empleado(self,nombre_empleado):
        notify={ "mensaje":"Empleado despedido con exito","tipo":"success"}
        if self.numeroEmpleados != 0:
            self.numeroEmpleados=self.numeroEmpleados - 1
        else:
            notify={"mensaje":"No se puede despedir a mas empleados","tipo":"info"}
            return notify
        if self.numeroEmpleados != 0:
            self.indiceproduccionempleados = self.numeroEmpleados/self.numeroMaximoEmpleados
        else:
            self.indiceproduccionempleados = 0
        for empleado in self.listaempleados:
            if empleado.nombre == nombre_empleado:
                self.listaempleados.remove(empleado)
        productividad=0
        for empleado in self.listaempleados:
            productividad=productividad + empleado.fuerza
        if self.numeroEmpleados != 0:
            self.indiceproductividadempleados = indiceProductividadEmpleadosParcelas(productividad,self.numeroEmpleados)
        else:
            self.indiceproductividadempleados = 0
        return notify

    def cambiarSeguridad(self,indice):
        self.seguridad=indice

    def incrementarCalidadTerreno(self,indice):
        if indice==1:
            self.calidadterreno=1
        if indice==2:
            self.calidadterreno=2
        if indice==3:
            self.calidadterreno=3
