import subprocess
import sys
import os

BASE = os.path.dirname(os.path.abspath(__file__))

pipeline = [
    (BASE+"/Scripts", "DIVIDIR.py"),
    (BASE+"/Scripts", "ENSAMBLADO.py"),
    (BASE+"/Scripts", "COMPARAR.py"),
    (BASE+"/Scripts", "SÍNTESIS.py"),
]

partes = int(input("Partes (bases por fragmento)? "))

for carpeta, script in pipeline:
    ruta_carpeta = os.path.join(BASE, carpeta)
    ruta_script = os.path.join(ruta_carpeta, script)

    print(f"\n-- Ejecutando {script} en {carpeta}")

    args = [sys.executable, ruta_script]
    if script in ["ENSAMBLADO.py"]:
        args.append(str(partes))
        args.append("n")
    if script in ["DIVIDIR.py"]:
        args.append(str(partes))
        args.append("y")

    result = subprocess.run(
        args,
        cwd=ruta_carpeta
    )

    if result.returncode != 0:
        print("Error detectado. Pipeline detenido.")
        break