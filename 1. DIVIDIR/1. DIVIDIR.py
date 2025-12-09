# Programa para, desde una secuencia de ADN, obtener codones
# Posibilidad de desordenarla, para desde el siguiente programa, ordenarlos

import datetime
import random
import os

desordenar = input("Desordenar? y/n: ")
partes = int(input("Partes (bases por fragmento)? "))
if desordenar == "y" or desordenar == "yes":
    desordenar = True
else:
    desordenar = False

hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

base_dir = os.path.dirname(os.path.abspath(__file__))
archivo_nombre = os.path.join(base_dir, "muestra.txt")
resultado_nombre = os.path.join(base_dir, "resultados", f"dividido_{desordenar}_{hora}.txt")

try:
    with open(archivo_nombre, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
except FileNotFoundError:
    print(f"Error: El archivo '{archivo_nombre}' no se encontró.")
    exit()
except Exception as e:
    print(f"Ocurrió un error al leer el archivo: {e}")
    exit()

contenido = contenido.replace(" ", "").replace("\n", "").replace("\r", "")
longitud = len(contenido)

solape = partes - 1  # número de bases compartidas
paso = partes - solape

fragmentos = [contenido[i:i+partes] for i in range(0, longitud, paso)]

fragmentos_final = []

for f in fragmentos:
    if len(f) == partes:
        fragmentos_final.append(f)
    else:
        num = partes-len(f)
        resultado = f
        for x in range(num):
            resultado = resultado+"X"
        fragmentos_final.append(resultado)
        break

if desordenar:
    random.shuffle(fragmentos_final)

try:
    with open(resultado_nombre, 'w', encoding='utf-8') as f:
        for frag in fragmentos_final:
            f.write(frag + "\n")
    print(f"\n✅ Análisis completado. Resultados guardados en: {resultado_nombre}")

except Exception as e:
    print(f"\n❌ Ocurrió un error al escribir el archivo de resultados: {e}")