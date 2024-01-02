import argparse
import requests

# Configurar el parser
parser = argparse.ArgumentParser(description="Descripción de lo que hace el script")

# Agregar argumentos
parser.add_argument("arg1", type=str, help="Accion")


# Parsear los argumentos
args = parser.parse_args()

# Acceder a los argumentos
print(f"Argumento 1: {args.arg1}")

# URL del servidor FastAPI
urlInicioPartida = "http://localhost:8000/inicioPartida/"
urlStopPartida = "http://localhost:8000/stopPartida/"
urlContinuarPartida = "http://localhost:8000/continuarPartida/"
urlFinalizarPartida = "http://localhost:8000/finalizarPartida/"
urlReinicioPartida = "http://localhost:8000/reinicioPartida/"


if args.arg1=="inicio":
    # Hacer la solicitud GET
    response = requests.get(urlInicioPartida)

if args.arg1=="stop":
    # Hacer la solicitud GET
    response = requests.get(urlStopPartida)

if args.arg1=="continuar":
    # Hacer la solicitud GET
    response = requests.get(urlContinuarPartida)

if args.arg1=="finalizar":
    # Hacer la solicitud GET
    response = requests.get(urlFinalizarPartida)

if args.arg1=="reinicio":
    # Hacer la solicitud GET
    response = requests.get(urlReinicioPartida)
   
if response.status_code == 200:
    print("ok")
else:
    print("fail")
# print(response.json())
# Verificar si la solicitud fue exitosa (código de respuesta 200)
# if response.status_code == 200:
#     # Extraer la respuesta JSON
#     data = response.json()
#     token = data["token"]
#     tienda = data["tienda"]
#     print(f"Token: {token}")
#     print(f"Tienda: {tienda}")
# else:
#     print(f"Error al hacer la solicitud. Código de respuesta: {response.status_code}")