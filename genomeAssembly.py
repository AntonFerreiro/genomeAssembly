###################################################
# PROGRAMA PRINCIPAL QUE EJECUTA LOS SUBPROGRAMAS #
###################################################

# Librerías
import subprocess
import sys
import os

# Directorio base
BASE = os.path.dirname(os.path.abspath(__file__))

# Subprogramas
pipeline = [
    (BASE+"/Scripts", "DIVIDIR.py"),
    (BASE+"/Scripts", "ENSAMBLADO.py"),
    (BASE+"/Scripts", "COMPARAR.py"),
    (BASE+"/Scripts", "SÍNTESIS.py"),
]

# Pedir la longitud de los fragmentos
partes = int(input("Partes (bases por fragmento)? "))

# Ejecutar cada subprograma
for carpeta, script in pipeline:
    ruta_carpeta = os.path.join(BASE, carpeta)
    ruta_script = os.path.join(ruta_carpeta, script)

    print(f"\n-- Ejecutando {script} en {carpeta}")

    args = [sys.executable, ruta_script]
    # Pasar argumentos
    # En caso de ensamblado, la longitud del fragmento y que no muestre grafo
    if script in ["ENSAMBLADO.py"]:
        args.append(str(partes))
        args.append("n")
    # En caso de dividir, la longitud del fragmento y que desordene
    if script in ["DIVIDIR.py"]:
        args.append(str(partes))
        args.append("y")

    # Ejecutar el subprograma
    result = subprocess.run(
        args,
        cwd=ruta_carpeta
    )

    # Detección de errores
    if result.returncode != 0:
        print("Error detectado. Pipeline detenido.")
        break