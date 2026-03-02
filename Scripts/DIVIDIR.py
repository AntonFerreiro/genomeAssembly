import random
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(
    description="Divide una secuencia en fragmentos para el ensamblaje"
)

# Flags obligatorios si quieres pasar por CLI
parser.add_argument(
    "-p", "--partes",
    type=int,
    help="Número de bases por fragmento"
)

parser.add_argument(
    "-s", "--shuffle",
    action="store_true",
    help="Desordenar los fragmentos"
)

args = parser.parse_args()

# -----------------------
# Resolver valores
# -----------------------

# PARTES
if args.partes is not None:
    partes = args.partes
else:
    partes = int(input("Partes (bases por fragmento)? "))

# DESORDENAR
if args.shuffle:
    desordenar = True
else:
    recibido = input("Desordenar fragmentos? [y/n]: ").strip().lower()
    desordenar = recibido in ["y", "yes"]

# -----------------------
# Directorios y archivos
# -----------------------
project_root = Path(__file__).resolve().parents[1]
archivo_nombre = project_root / 'Muestras' / 'muestra.txt'
resultado_nombre = project_root / "Resultados" / "dividido.txt"

# -----------------------
# Leer archivo
# -----------------------
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

# -----------------------
# Fragmentar
# -----------------------
fragmentos = [contenido[i:i+partes] for i in range(0, longitud, partes - (partes - 1))]
fragmentos_final = [f for f in fragmentos if len(f) == partes]

# -----------------------
# Desordenar si toca
# -----------------------
if desordenar:
    random.shuffle(fragmentos_final)

# -----------------------
# Guardar resultados
# -----------------------
try:
    with open(resultado_nombre, 'w', encoding='utf-8') as f:
        for frag in fragmentos_final:
            f.write(frag + "\n")
    print(f"\n[OK] Análisis completado. Resultados guardados en: {resultado_nombre}")
except Exception as e:
    print(f"\n[ERROR] Ocurrió un error al escribir el archivo de resultados: {e}")