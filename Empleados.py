class Empleados():
    def __init__(self, nombreempleado,ciudad,bbdd):
        self.nombre = nombreempleado
        self.precio,self.comunicacion,self.estudios,self.fuerza,self.liderazgo = bbdd.obtener_informacion_empleado(nombreempleado, ciudad)
       

    def mostrar_informacion(self):
        empleados_dict = {
            "nombre": self.nombre,
            "precio": self.precio,
            "comunicacion":self.comunicacion,
            "estudios":self.estudios,
            "fuerza":self.fuerza,
            "liderazgo":self.liderazgo,
        }
        return empleados_dict