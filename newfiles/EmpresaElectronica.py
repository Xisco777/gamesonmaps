from Empresa import Empresa
from EmpleadosElectronica import EmpleadosElectronica
from ProyectoElectronica import ProyectoElectronica

venta = {
    "tipo": str,
    "numero": int,
}

indiceNumeroMaximoEmpleados=20
indiceInicialVariedadProductos=0.5

class Empresa(Empresa):
    def __init__(self, nombreEmpresa, nombreciudad,bbdd):
        self.nombre = nombreEmpresa
        precio,tamaño = bbdd.obtener_informacion_empresa(nombreEmpresa,nombreciudad)
        self.tamaño = tamaño
        self.precio = precio
        self.listaproyectos = []
        self.numeroEmpleados = 0
        self.numeroMaximoEmpleados = tamaño/indiceNumeroMaximoEmpleados
        self.indiceVariedadProductos = indiceInicialVariedadProductos
        self.listaempleados=[]
        self.ciudad=nombreciudad
        self.indiceproductividadempleados = 1
        self.seguridad = 0
        self.maximaSeguridad = 5
        self.indiceMaximoTiempo = 1.5
        self.numeroempleadosHW=0
        self.numeroempleadosFW=0
        self.numeroempleadosSW=0 
        self.numeroempleadosProduccion=0 
        self.numeroempleadosTesting=0 
        self.numeroempreadosMecanica=0 
        self.numeroepleadosGestion=0
        self.experienciaempresa=0.5

    def agregar_proyecto(self, nombreproyecto):
        proyecto=ProyectoElectronica(nombreproyecto)
        self.listaproyectos.append(proyecto)

    def evolucion_proyectos_electronica(self):
        empleados_empresa = {
            "numeroempleadosHW": self.numeroempleadosHW,
            "numeroempleadosFW": self.numeroempleadosFW,
            "numeroempleadosSW": self.numeroempleadosSW,
            "numeroempleadosProduccion": self.numeroempleadosProduccion,
            "numeroempleadosTesting": self.numeroempleadosTesting,
            "numeroempreadosMecanica": self.numeroempreadosMecanica,
            "numeroempleadosGestion": self.numeroempleadosGestion
        }
        lista_produccion = []
        beneficio=0
        for proyecto in self.listaproyectos:     
            empleados_empresa, indice=proyecto.indiceproduccionmes(empleados_empresa)
            if 0 < ((self.indiceproductividadempleados-proyecto.dificultad + indice)/2):
                evolucion= (100/proyecto.duracionmeses)*((self.indiceproductividadempleados-proyecto.dificultad + indice)/2) * self.experienciaempresa
                proyecto.porcentajefinalizacion -= evolucion
                if proyecto.porcentajefinalizacion < 0:
                    proyecto.finalizado=True
                    produccion = {}  # Crear un nuevo diccionario para cada plantación   
                    produccion["tipo"] = proyecto.producto
                    produccion["numero"] = proyecto.numeroproductos                    
                    lista_produccion.apped(produccion)
                    self.experienciaempresa += proyecto.relevancia
                    beneficio+=proyecto.presupuesto
                    self.listaproyectos.remove(proyecto)
        return lista_produccion, beneficio

    

    def contratar_empleado(self,nombre_empleado, bbdd):
        if self.numeroEmpleados < self.numeroMaximoEmpleados:
            self.numeroEmpleados += 1
        else:
            print("no se puede contratar a mas personas")
            return
        empleado=EmpleadosElectronica(nombre_empleado,self.ciudad, bbdd)
        if empleado.tipo=="HW":
            self.numeroempleadosHW +=1
        elif empleado.tipo=="FW":
            self.numeroempleadosFW +=1
        elif empleado.tipo=="SW":
            self.numeroempleadosSW +=1
        elif empleado.tipo=="Produccion":
            self.numeroempleadosProduccion +=1
        elif empleado.tipo=="Testing":
            self.numeroempleadosTesting +=1
        elif empleado.tipo=="Mecanica":
            self.numeroempleadosMecanica +=1
        elif empleado.tipo=="Gestion":
            self.numeroempleadosGestion +=1
        self.listaempleados.append(empleado)
        productividad=0
        for empleado in self.listaempleados:
            productividad += empleado.productividad
        self.indiceproductividadempleados = productividad/self.numeroEmpleados