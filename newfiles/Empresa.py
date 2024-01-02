from Producto import Producto
from Empleados import Empleados
import json
venta = {
    "tipo": str,
    "numero": int,
}

indiceNumeroMaximoEmpleados=20
indiceInicialTiempo=0.5
indiceInicialVariedadProductos=0.5

class Empresa():
    def __init__(self, nombreEmpresa, nombreciudad,bbdd):
        self.nombre = nombreEmpresa
        precio,tamaño = bbdd.obtener_informacion_tienda(nombreEmpresa,nombreciudad)
        self.tamaño = tamaño
        self.precio = precio
        self.listaproductos = []
        self.numeroEmpleados = 0
        self.numeroMaximoEmpleados = tamaño/indiceNumeroMaximoEmpleados
        self.indiceproduccionempleados = 1
        self.indiceTiempo = indiceInicialTiempo
        self.indiceVariedadProductos = indiceInicialVariedadProductos
        self.listaempleados=[]
        self.ciudadtienda=nombreciudad
        self.indiceproductividadempleados = 1
        self.seguridad = 0
        self.maximaSeguridad = 5
        self.indiceMaximoTiempo = 1.5

    def mostrar_informacion(self):
        print(f"Nombre: {self.nombre}")
        print(f"Tamaño: {self.tamaño}")
        print(f"Precio: {self.precio}")
        arrayProductos=[]
        for productos in self.listaproductos:
            arrayProductos.append(productos.mostrar_informacion())
        arrayEmpleados=[]
        for empleados in self.listaempleados:
            arrayEmpleados.append(empleados.mostrar_informacion()) 
        empresa_dict = {
            "nombre": self.nombre,
            "tamaño": self.tamaño,
            "precio": self.precio,
            "arrayProductos": arrayProductos,
            "numeroEmpleados": self.numeroEmpleados,
            "numeroMaximoEmpleados": self.numeroMaximoEmpleados,
            "indiceproduccionempleados": self.indiceproduccionempleados,
            "indiceTiempo": self.indiceTiempo,
            "indiceVariedadProductos": self.indiceVariedadProductos,
            "arrayEmpleados": arrayEmpleados,
            "ciudadtienda": self.ciudadtienda,
            "indiceproductividadempleados": self.indiceproductividadempleados,
            "seguridad": self.seguridad,
            "maximaSeguridad": self.maximaSeguridad,
            "indiceMaximoTiempo": self.indiceMaximoTiempo
        }
        return empresa_dict

    def agregar_producto(self, tipoproductos):
        producto=Producto(tipoproductos)
        self.listaproductos.append(producto)
        tipos_diferentes = set()  # Conjunto para almacenar tipos únicos
        for producto in self.listaproductos:
            tipo = producto.tipo
            tipos_diferentes.add(tipo)
        # Contar el número de tipos únicos
        numero_tipos_diferentes = len(tipos_diferentes)
        self.indiceVariedadProductos = indiceInicialVariedadProductos + (numero_tipos_diferentes/40)
        print(self.indiceVariedadProductos)

    def despedir_empleado(self):
        if self.numeroEmpleados != 0:
            self.numeroEmpleados -= 1
        else:
            print("no se puede despedir a mas personas")
        self.indiceproduccionempleados = self.numeroMaximoEmpleados/self.numeroEmpleados
        for empleado in self.listaempleados:
            if empleado.nombre == nombre_empleado:
                self.listaempleados.remove(empleado)
        productividad=0
        for empleado in self.listaempleados:
            productividad += empleado.productividad
        self.indiceproductividadempleados = productividad/self.numeroEmpleados
    
    def incremento_prestigio_tienda(self):
        if self.indiceTiempo < self.indiceMaximoTiempo:
            self.indiceTiempo += 0.01

    def contratar_empleado(self,nombre_empleado, bbdd):
        if self.numeroEmpleados < self.numeroMaximoEmpleados:
            self.numeroEmpleados += 1
        else:
            print("no se puede contratar a mas personas")
        self.indiceproduccionempleados = self.numeroMaximoEmpleados/self.numeroEmpleados
        empleado=Empleados(nombre_empleado,self.ciudadtienda, bbdd)
        self.listaempleados.append(empleado)
        productividad=0
        for empleado in self.listaempleados:
            productividad += empleado.productividad
        self.indiceproductividadempleados = productividad/self.numeroEmpleados
    
    def incrementar_seguridad(self):
        if self.seguridad < self.maximaSeguridad:
            self.seguridads += 1