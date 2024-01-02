import json
import time




diccionario = [{
    "tipo": str,
    "numero": int,
}]  

elemento = {
    "tipo": str,
    "numero": int,
}
class Fecha:

    def __init__(self, ano, mes):
        self.mes = mes
        self.ano = ano
        self.stop=False
        self.finalizar=False
        
    
    def __str__(self):
        return f"{self.mes}/{self.ano}"

    def cambioFecha(self,ano,mes):
        self.mes = mes
        self.ano = ano

    def cambioStop(self,stop):
        self.stop = stop
    
    def cambioFinalizar(self,finalizar):
        self.finalizar = finalizar


    def incrementar(self,listaUsuarios,bbdd):
        
        # Registra el tiempo de inicio
        inicio = time.time()

        if self.mes == 12:
            self.ano +=  1
            self.mes = 1
        else:
            self.mes += 1


        print(f"{self.mes}/{self.ano}")
        for usuario in listaUsuarios:
            ingresosmensual=0.0
            gastosmensual=0.0
            diccionario = [{}] 
            for diccionario in usuario.produccion(self):
                elemento = {}  
                for idx, elemento in enumerate(usuario.almacen):
                    if elemento["tipo"] == diccionario["tipo"]:
                        if diccionario["numero"] != 0:
                            elemento["numero"] = elemento["numero"] + (diccionario["numero"]/usuario.almacen[idx]["totalano"])*usuario.almacen[idx]["prodHectarea"]
                        usuario.almacen[idx]["numero"] = elemento["numero"]
            #print(usuario.nombre)
            #print("produccion")
            #print(usuario.almacen)

            diccionario = [{}]
            usuario.incremento_prestigio_tiendas()
            for diccionario in usuario.venta():
                #print(diccionario)
                elemento = {}
                for idx, elemento in enumerate(usuario.almacen):
                    if elemento["tipo"] == diccionario["tipo"]:
                        elemento["numero"] = elemento["numero"] - diccionario["numero"]
                        if elemento["numero"] <= 0:
                            diccionario["numero"]=0
                            elemento["numero"] = 0
                        usuario.almacen[idx]["numero"] = elemento["numero"]
                        incrementoprecio = diccionario["numero"] * usuario.almacen[idx]["precio"]
                        ingresosmensual += incrementoprecio
            #print("venta")
            #print(usuario.almacen)

            gastosmensual=usuario.empleados_gastos_mes()
            usuario.dinero = usuario.dinero + ingresosmensual - gastosmensual
            print(ingresosmensual , gastosmensual, usuario.dinero)
            # usuario_dict = json.loads(usuario.mostrar_informacion())
            bbdd.updateusuario(usuario) 
        
                

        # Registra el tiempo de finalización
        fin = time.time()
        # Calcula la diferencia de tiempo
        tiempo_total = fin - inicio
        print(f"Tiempo de ejecución: {tiempo_total} segundos")
 # añadir incremento_mes en tienda
        
