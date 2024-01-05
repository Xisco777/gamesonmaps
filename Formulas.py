import random



factorRoboParcela=0.5
def roboParcela(seguridad):
    return random.expovariate(factorRoboParcela) > seguridad

factorRoboCasa=0.7
def roboCasa(seguridad):
    return random.expovariate(factorRoboCasa) > seguridad

cantidadMultaRoboCasa_valor=20000
def cantidadMultaRoboCasa():
    return cantidadMultaRoboCasa_valor

cantidadMultaRoboParcela_valor=20000
def cantidadMultaRoboParcela():
    return cantidadMultaRoboParcela_valor

cantidadMultaRoboTienda_valor=20000
def cantidadMultaRoboTienda():
    return cantidadMultaRoboTienda_valor

factorCantidadRoboCasa=0.5
def cantidadRoboCasa():
    return random.expovariate(factorCantidadRoboCasa)*1000

factorRoboParcelaLibre=0.5
def randomRoboParcelaLibre():
    resultado = random.expovariate(factorRoboParcelaLibre)*1000
    return int(resultado)

maxRandomProduccionParcelasMensual=1.05
minRandomProduccionParcelasMensual=0.95
def randMesProducParcelas():
    return random.uniform(minRandomProduccionParcelasMensual, maxRandomProduccionParcelasMensual)

def calculoProduccionParcelasMes(factormultiplicacion,produccionmes,indiceproduccionempleados,calidadterreno,indiceproductividadempleados,numeroPlantaciones,tamaño):
    calidadTerrenoCalculo=float(calidadterreno)/10+0.85
    resultado=randMesProducParcelas() * float(factormultiplicacion) * float(produccionmes) * indiceproduccionempleados * calidadTerrenoCalculo * indiceproductividadempleados
    resultado=tamaño/numeroPlantaciones*resultado
    #print(resultado,factormultiplicacion,produccionmes,indiceproduccionempleados,calidadTerrenoCalculo,indiceproductividadempleados)
    return resultado

def indiceProductividadEmpleadosParcelas(productividad,numeroEmpleados):
    indiceproductividadempleados = (productividad/numeroEmpleados)/10+0.75
    return indiceproductividadempleados

maxRandomVentaTiendasMensual=1.05
minRandomVentaTiendasMensual=0.95
def randMesVentaTiendas():
    return random.uniform(minRandomVentaTiendasMensual, maxRandomVentaTiendasMensual)

numeroProductosTienda=21
indiceInicialVariedadProductosTienda=0.2
def indiceVariedadProductosTienda(numero_tipos_diferentes):
    resultado=indiceInicialVariedadProductosTienda + (numero_tipos_diferentes/numeroProductosTienda)
    return resultado

ventaPosicionTiendaMes=1000
def calculoVentaTiendasMes(indiceproduccionempleados,indiceVariedadProductos,prestigio,indiceproductividadempleados):
    prestigio=float(prestigio)/50+0.85
    resultado=randMesVentaTiendas() * indiceproduccionempleados  * indiceVariedadProductos * prestigio * indiceproductividadempleados * ventaPosicionTiendaMes
    #print(resultado,indiceproduccionempleados,indiceVariedadProductos,prestigio,indiceproductividadempleados)
    return resultado

def indiceProductividadEmpleadosTiendas(productividad,numeroEmpleados):
    indiceproductividadempleados = (productividad/numeroEmpleados)/10+0.75
    return indiceproductividadempleados


dineroInicial=300000
def obtenerDineroInicial():
    return dineroInicial

HectareasPorEmpleado=3
def GetHectareasPorEmpleado():
    return HectareasPorEmpleado

factormultiplicacion=1.25
def Getfactormultiplicacion():
    return factormultiplicacion

URL="http://localhost:8083/"  #url de este servido, donde se alojan las imagenes.
def GetURL():
    return URL

import matplotlib.pyplot as plt

# lambda_value = 0.2
# resultados = []

# for _ in range(1000):
#     numero_exponencial = random.expovariate(lambda_value)
    
#     resultados.append(numero_exponencial)

# # Crear un histograma
# plt.hist(resultados, bins=20, edgecolor='black', alpha=0.7)
# plt.xlabel('Valor Exponencial')
# plt.ylabel('Frecuencia')
# plt.title('Histograma de 100 Valores Exponenciales')
# plt.show()