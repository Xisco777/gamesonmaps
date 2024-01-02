class EmpleadosElectronica():
    def __init__(self, nombreempleado,ciudad,bbdd):
        self.nombre = nombreempleado
        self.productividad,self.precio,self.tipo = bbdd.obtener_informacion_empleado_electronica(nombreempleado, ciudad)
        #dificultad (entre 0 y 1)

    def mostrar_informacion(self):
        print(f"Nombre Empleado: {self.nombre}")
        print(f"Productividad: {self.productividad}")
        print(f"Precio: {self.precio}")
        print(f"Tipo: {self.tipo}")