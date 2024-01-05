import sqlite3

class DatabaseManagerMongodv:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def obtener_informacion_ciudad(self, nombre_ciudad):
        query = "SELECT poblacion, coordenadas_x, coordenadas_y, idioma_principal, indice_productos FROM ciudades WHERE nombre = ?"
        self.cursor.execute(query, (nombre_ciudad,))
        result = self.cursor.fetchone()
        return result
    
    def obtener_datos_usuario(self, nombre):
        query = "SELECT edad FROM usuarios WHERE nombre = ?"
        self.cursor.execute(query, (nombre,))
        result = self.cursor.fetchone()
        return result
    
    def obtener_informacion_parcela(self, nombre_parcela, nombre_ciudad):
        query = "SELECT tamaño FROM parcelas WHERE nombre_parcela = ? AND nombre_ciudad = ?"
        self.cursor.execute(query, (nombre_parcela,nombre_ciudad,))
        result = self.cursor.fetchone()
        return result
    
    def obtener_informacion_produccion_platacion(self, tipo):
        query = "SELECT * FROM produccion_plantacion WHERE tipo_plantacion = ?"
        self.cursor.execute(query, (tipo,))
        result = self.cursor.fetchone()
        print (result)
        return result

    def obtener_informacion_tienda(self, nombre_tienda, nombre_ciudad):
        query = "SELECT tamaño FROM tiendas WHERE nombre_tienda = ? AND nombre_ciudad = ?"
        self.cursor.execute(query, (nombre_tienda,nombre_ciudad,))
        result = self.cursor.fetchone()
        return result

    def obtener_informacion_empleado(self, nombre_empleado, nombre_ciudad):
        query = "SELECT productividad_empleado,precio_empleado FROM empleados WHERE nombre_empleado = ? AND ciudad_empleado = ?"
        self.cursor.execute(query, (nombre_empleado,nombre_ciudad,))
        result = self.cursor.fetchone()
        return result

    def cerrar_conexion(self):
        self.conn.close()