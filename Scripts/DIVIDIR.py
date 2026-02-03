#####################################################################
# 1. DIVIDIR --> DE LA MUESTRA ORIGINAL A FRAGMENTOS (+ DESORDENAR) #
#####################################################################

# Librerías
import random
import sys
from pathlib import Path

# Si no recibe argumentos al ejecutar, que pida por teclado la longitud de los fragmentos
if len(sys.argv) > 1:
    partes = int(sys.argv[1])
else:
    partes = int(input("Partes (bases por fragmento)? "))

# Si no recibe argumentos al ejecutar, que pida por teclado si desordenar los fragmentos
desordenar = False
if len(sys.argv) > 2:
    recibido = sys.argv[2]
else:
    recibido = input("Desordenar? y/n: ")

if recibido == "y" or recibido == "yes":
        desordenar = True

# Directorio de archivos
project_root = Path(__file__).resolve().parents[1]
base_dir = Path(__file__).resolve().parent
archivo_nombre = project_root/'Muestras'/'muestra.txt'

resultado_nombre = (
    project_root
    / "Resultados"
    / f"dividido.txt"
)

# Intentar leer archivo de la muestra original
try:
    with open(archivo_nombre, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
except FileNotFoundError:
    print(f"Error: El archivo '{archivo_nombre}' no se encontró.")
    exit()
except Exception as e:
    print(f"Ocurrió un error al leer el archivo: {e}")
    exit()

# Eliminar espacios y saltos de línea
contenido = contenido.replace(" ", "").replace("\n", "").replace("\r", "")
longitud = len(contenido)

# Fragmentar la muestra original en longitud de partes k
fragmentos = [contenido[i:i+partes] for i in range(0, longitud, partes - (partes - 1))]

fragmentos_final = []

# Guardar fragmentos en lista final
for f in fragmentos:
    if len(f) == partes:
        fragmentos_final.append(f)

# Desordenar fragmentos si es el caso
if desordenar:
    random.shuffle(fragmentos_final)

# Guardar resultados
try:
    with open(resultado_nombre, 'w', encoding='utf-8') as f:
        for frag in fragmentos_final:
            f.write(frag + "\n")
    print(f"\n✅ Análisis completado. Resultados guardados en: {resultado_nombre}")

except Exception as e:
    print(f"\n❌ Ocurrió un error al escribir el archivo de resultados: {e}")