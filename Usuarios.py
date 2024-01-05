from Ciudad import Ciudad
import json
from Formulas import calculoProduccionParcelasMes, calculoVentaTiendasMes
import time
lista_produccion = []
lista_venta = []
produccion = {
    "tipo": str,
    "numero": int,
}
venta = {
    "tipo": str,
    "numero": int,
}


maximoprestigio = 1.0
divisionprestigocasa=10
dineroinicial=200000.0
precioMejoraCalidadTerreno=12000
precioMejoraSeguridad=15000
incrementoPrestigioCasa=1

class Usuario():
    nombre:str
    def __init__(self, nombre, bbdd):
        self.nombre = nombre
        edad = bbdd.obtener_datos_usuario(nombre)
        self.prestigio :float = 0
        self.edad = edad
        self.listaciudades = [] 
        self.dinero = dineroinicial
        self.almacen = [] 
        self.id=""

    def mostrar_informacion(self):
        arraylistaciudades = []
        for ciudad in self.listaciudades:
            arraylistaciudades.append(ciudad.mostrar_informacion())
        listaciudades_json = json.dumps(arraylistaciudades)
        usuario_dict = {
            "nombre": self.nombre,
            "edad": self.edad,
            "listaciudades": json.loads(listaciudades_json),
            "prestigio": self.prestigio,
            "dinero": self.dinero,
            "almacen": self.almacen,
            "id":self.id
        }
        # Convertir el diccionario a JSON
        usuario_json = json.dumps(usuario_dict)
        return usuario_json
        
    def crear_ciudad(self, nombreciudad,bbdd):
        ciudad=Ciudad(nombreciudad,bbdd)
        self.listaciudades.append(ciudad)

    def comprar_parcela(self, nombreciudad,nombreparcela,bbdd):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                self.dinero = self.dinero - ciudad.comprar_parcela(nombreparcela,bbdd) 
    
    def eliminar_y_obtener_parcela_por_nombre(self, nombreciudad,nombreparcela):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                return ciudad.eliminar_y_obtener_parcela_por_nombre(nombreparcela)
        return None              

    def añadir_parcela(self, nombreciudad,parcela):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                ciudad.añadir_parcela(parcela)
        return 
    
    def agregar_plantacion(self, nombreciudad,nombreparcela,tipoplantacion,bbdd):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                for parcela in ciudad.listaparcelas:
                    if parcela.nombre == nombreparcela:
                        parcela.agregar_plantacion(tipoplantacion,bbdd)
    
    def modificar_plantacion(self, indice, nombreciudad,nombreparcela,tipoplantacion,bbdd):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                for parcela in ciudad.listaparcelas:
                    if parcela.nombre == nombreparcela:
                        parcela.modificar_plantacion(indice,tipoplantacion, bbdd)

    def modificar_producto(self, indice, nombreciudad,nombretienda,tipoproducto):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                for tienda in ciudad.listatiendas:
                    if tienda.nombre == nombretienda:
                        tienda.modificar_producto(indice,tipoproducto)

    def produccion(self,fecha):
        lista_produccion = []
        inicio = time.time()
        for ciudad in self.listaciudades:
            for parcela in ciudad.listaparcelas:
                if  parcela.habilitacionproduccionmes==True:
                    for plantacion in parcela.listaplantacion:  
                        produccion = {}  # Crear un nuevo diccionario para cada plantación   
                        produccion["tipo"] = plantacion.tipo
                        try:
                            # Código que puede generar un error
                            prodmes =  plantacion.produccionmes[fecha.mes]['$numberInt']
                        except (TypeError, KeyError) as e:
                            prodmes =  plantacion.produccionmes[fecha.mes]
                        produccion["numero"] = calculoProduccionParcelasMes(plantacion.factormultiplicacion,prodmes,parcela.indiceproduccionempleados,parcela.calidadterreno,parcela.indiceproductividadempleados,parcela.numeroplantaciones,parcela.tamaño)
                        lista_produccion.append(produccion)
                    parcela.habilitacionproduccionmes==True
                # Registra el tiempo de finalización
        fin = time.time()
        # Calcula la diferencia de tiempo
        tiempo_total = fin - inicio
        print(f"Tiempo de ejecución produccion: {tiempo_total} segundos")
        return lista_produccion

    def comprar_tienda(self, nombreciudad,nombretienda,bbdd):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                tiendaPrecio, tiendaPrestigio=ciudad.comprar_tienda(nombretienda,bbdd)
                self.dinero = self.dinero - tiendaPrecio
                self.prestigio = self.prestigio + float(tiendaPrestigio)

    def eliminar_y_obtener_tienda_por_nombre(self, nombreciudad,nombretienda):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                return ciudad.eliminar_y_obtener_tienda_por_nombre(nombretienda)
        return None 
    
    def añadir_tienda(self, nombreciudad,tienda):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                ciudad.añadir_tienda(tienda)
        return 
    
    def agregar_producto(self, nombreciudad,nombretienda,tipoproducto):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                for tienda in ciudad.listatiendas:
                    if tienda.nombre == nombretienda:
                        tienda.agregar_producto(tipoproducto)   

    def venta(self):
        lista_venta=[]
        for ciudad in self.listaciudades:
            for tienda in ciudad.listatiendas:
                for producto in tienda.listaproductos:
                        venta = {}  # Crear un nuevo diccionario para cada plantación   
                        venta["tipo"] = producto.tipo
                        venta["numero"] = calculoVentaTiendasMes(tienda.indiceproduccionempleados, tienda.indiceVariedadProductos, tienda.prestigio, tienda.indiceproductividadempleados)
                        lista_venta.append(venta)
        return lista_venta
    
    def empleados_gastos_mes(self):
        cantidadgastomensual=0.0
        for ciudad in self.listaciudades:

            for parcela in ciudad.listaparcelas:
                for empleado in parcela.listaempleados:
                    cantidadgastomensual += empleado.precio

            for tienda in ciudad.listatiendas:
                for empleado in tienda.listaempleados:
                    cantidadgastomensual += empleado.precio

        return cantidadgastomensual
    
    def incremento_prestigio_tiendas(self):
        calculoprestigio=0
        for ciudad in self.listaciudades:
            for tienda in ciudad.listatiendas:
                calculoprestigio=calculoprestigio+tienda.incremento_prestigio_tienda()
        self.prestigio =self.prestigio+calculoprestigio
    
    def incrementar_prestigio(self):
        if self.prestigio < maximoprestigio:
            self.prestigio =self.prestigio+ 0.02
    
    def decrementar_prestigio(self):
        if 0 < self.prestigio:
            self.prestigio =self.prestigio- 0.02

    def contratarempleado(self, nombreciudad,lugar,nombreempleado,bbdd):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                for tienda in ciudad.listatiendas:
                    if tienda.nombre == lugar:
                        return tienda.contratar_empleado(nombreempleado,bbdd)
                for parcela in ciudad.listaparcelas:
                    if parcela.nombre == lugar:
                        return parcela.contratar_empleado(nombreempleado,bbdd)

    def despedirempleado(self, nombreciudad,lugar,nombreempleado):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                for tienda in ciudad.listatiendas:
                    if tienda.nombre == lugar:
                        return tienda.despedir_empleado(nombreempleado)
                for parcela in ciudad.listaparcelas:
                    if parcela.nombre == lugar:
                        return parcela.despedir_empleado(nombreempleado)
    
    def comprar_casa(self, nombreciudad,nombrecasa,bbdd):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                ciudad.comprar_casa(nombrecasa,bbdd)
                print(self.prestigio, ciudad.casa.prestigio)
                self.prestigio = self.prestigio + float(ciudad.casa.prestigio)
                self.dinero =self.dinero-float(ciudad.casa.precio)
                    
    
    def comprar_empresaelectronica(self, nombreciudad,nombreempresa,bbdd):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                self.dinero =self.dinero-float(ciudad.comprar_empresa_electronica(nombreempresa,bbdd))
        
    def agregar_proyecto_electronica(self, nombreciudad,nombreempresaelectronica,nombreproyecto):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                for empreselectronica in ciudad.listaEmpresaElectronica:
                    if empreselectronica.nombre == nombreempresaelectronica:
                        empreselectronica.agregar_proyecto(nombreproyecto)   

    def cambiarSeguridad(self, nombreciudad,lugar,indice,precioMejoraSeguridad):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                for tienda in ciudad.listatiendas:
                    if tienda.nombre == lugar:
                        tienda.cambiarSeguridad(indice)
                for parcela in ciudad.listaparcelas:
                    if parcela.nombre == lugar:
                        parcela.cambiarSeguridad(indice)
                # for empresaelectronica in ciudad.listaEmpresaElectronica:
                #     if empresaelectronica.nombre == lugar:
                #         empresaelectronica.cambiarSeguridad(indice)
        self.dinero=self.dinero-float(precioMejoraSeguridad)
    
    def cambiarSeguridadTienda(self, nombreciudad,lugar,indice,precioMejoraSeguridad):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                for tienda in ciudad.listatiendas:
                    if tienda.nombre == lugar:
                        tienda.cambiarSeguridad(indice)
        self.dinero=self.dinero-float(precioMejoraSeguridad)

    def cambiarSeguridadCasa(self, nombreciudad,nombreCasa,indice,precioMejoraSeguridad):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                if ciudad.casa.nombrecasa == nombreCasa:
                    ciudad.casa.cambiarSeguridadCasa(indice)
        self.dinero=self.dinero-float(precioMejoraSeguridad)

    def incrementarCalidadTerreno(self, nombreciudad,lugar,indice,precioMejora):
        for ciudad in self.listaciudades:
            if ciudad.nombre == nombreciudad:
                for parcela in ciudad.listaparcelas:
                    if parcela.nombre == lugar:
                        parcela.incrementarCalidadTerreno(indice)
        self.dinero=self.dinero-float(precioMejora)
        