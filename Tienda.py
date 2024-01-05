from Producto import Producto
from Empleados import Empleados
from Formulas import indiceProductividadEmpleadosTiendas, indiceVariedadProductosTienda,GetURL

import json
venta = {
    "tipo": str,
    "numero": int,
}


class Tienda():
    def __init__(self, nombretienda, nombreciudad, bbdd):
        self.nombre = nombretienda
        precio,tamaño,prestigio,numeroMaximoEmpleados = bbdd.obtener_informacion_tienda(nombretienda,nombreciudad)
        self.tamaño = tamaño
        self.precio = precio
        self.prestigio = prestigio
        self.listaproductos = []
        self.numeroEmpleados = 0
        self.numeroMaximoEmpleados = numeroMaximoEmpleados
        self.indiceproduccionempleados = 0
        self.listaempleados=[]
        self.ciudadtienda=nombreciudad
        self.indiceproductividadempleados = 0
        self.seguridad = 0
        for _ in range(tamaño):
            self.agregar_producto("Libre")

    def mostrar_informacion(self):
        arrayProductos=[]
        for productos in self.listaproductos:
            arrayProductos.append(productos.mostrar_informacion())
        arrayEmpleados=[]
        for empleados in self.listaempleados:
            arrayEmpleados.append(empleados.mostrar_informacion()) 
        tienda_dict = {
            "nombre": self.nombre,
            "tamaño": self.tamaño,
            "precio": self.precio,
            "arrayProductos": arrayProductos,
            "numeroEmpleados": self.numeroEmpleados,
            "numeroMaximoEmpleados": self.numeroMaximoEmpleados,
            "indiceproduccionempleados": self.indiceproduccionempleados,
            "indiceVariedadProductos": self.indiceVariedadProductos,
            "arrayEmpleados": arrayEmpleados,
            "ciudadtienda": self.ciudadtienda,
            "indiceproductividadempleados": self.indiceproductividadempleados,
            "seguridad": self.seguridad,
            "prestigio": self.prestigio
        }
        return tienda_dict

    def agregar_producto(self, tipoproductos):
        producto=Producto(tipoproductos)
        self.listaproductos.append(producto)
        tipos_diferentes = set()  # Conjunto para almacenar tipos únicos
        for producto in self.listaproductos:
            tipo = producto.tipo
            tipos_diferentes.add(tipo)
        # Contar el número de tipos únicos
        numero_tipos_diferentes = len(tipos_diferentes)
        self.indiceVariedadProductos = indiceVariedadProductosTienda(numero_tipos_diferentes)

    def contratar_empleado(self,nombre_empleado, bbdd):
        notify={ "mensaje":"Empleado contratado con exito","tipo":"success"}
        if self.numeroEmpleados < self.numeroMaximoEmpleados:
            self.numeroEmpleados += 1
        else:
            notify={"mensaje":"No se puede contratar a mas empleados","tipo":"info"}
            return notify
        self.indiceproduccionempleados = self.numeroEmpleados/self.numeroMaximoEmpleados
        empleado=Empleados(nombre_empleado,self.ciudadtienda, bbdd)
        self.listaempleados.append(empleado)
        productividad=0
        for empleado in self.listaempleados:
            productividad=productividad + empleado.comunicacion
        self.indiceproductividadempleados = indiceProductividadEmpleadosTiendas(productividad,self.numeroEmpleados)
        return notify

    def despedir_empleado(self,nombre_empleado):
        notify={ "mensaje":"Empleado despedido con exito","tipo":"success"}
        if self.numeroEmpleados != 0:
            self.numeroEmpleados -= 1
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
            productividad=productividad + empleado.comunicacion
        if self.numeroEmpleados != 0:
            self.indiceproductividadempleados = indiceProductividadEmpleadosTiendas(productividad,self.numeroEmpleados)
        else:
            self.indiceproductividadempleados = 0 
        return notify
    
    def incremento_prestigio_tienda(self):
        self.prestigio += 0.01
        #print("Prestigiotienda:" + str(self.prestigio))
        return 0.01

    
    def incrementar_seguridad(self):
        if self.seguridad < 4:
            self.seguridads += 1


    def modificar_producto(self, index, tipoproducto):
        # print(tipoproducto)
        producto=self.listaproductos[index]
        producto.tipo=tipoproducto
        producto.urlicono =GetURL()+tipoproducto+".PNG"
        producto.select={ "nombre":tipoproducto, "urlicono": GetURL()+tipoproducto+".PNG" }
        self.listaproductos[index] = producto
        tipos_diferentes = set()  # Conjunto para almacenar tipos únicos
        for producto in self.listaproductos:
            tipo = producto.tipo
            tipos_diferentes.add(tipo)
        # Contar el número de tipos únicos
        numero_tipos_diferentes = len(tipos_diferentes)
        self.indiceVariedadProductos = indiceVariedadProductosTienda(numero_tipos_diferentes)

    def cambiarSeguridad(self,indice):
        self.seguridad=indice