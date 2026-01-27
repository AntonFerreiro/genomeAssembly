import subprocess
import sys
import os

BASE = os.path.dirname(os.path.abspath(__file__))

pipeline = [
    (BASE+"/1. DIVIDIR", "DIVIDIR.py"),
    (BASE+"/2. ENSAMBLADO", "ENSAMBLADO.py"),
    (BASE+"/4. SÍNTESIS", "SÍNTESIS.py"),
]

for carpeta, script in pipeline:
    ruta_carpeta = os.path.join(BASE, carpeta)
    ruta_script = os.path.join(ruta_carpeta, script)

    print(f"\n-- Ejecutando {script} en {carpeta}")

    result = subprocess.run(
        [sys.executable, ruta_script],
        cwd=ruta_carpeta
    )

    if result.returncode != 0:
        print("Error detectado. Pipeline detenido.")
        break
