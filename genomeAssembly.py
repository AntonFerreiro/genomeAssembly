###################################################
# PROGRAMA PRINCIPAL QUE EJECUTA LOS SUBPROGRAMAS #
###################################################

import subprocess
import sys
import os
import logging
import shutil
import argparse

# -----------------------
# Configuración de logging con rotación manual
# -----------------------
def setup_logging(verbose_console=False, log_file="log.txt"):
    # Rotación de log: log.txt -> log.txt.old
    if os.path.exists(log_file):
        old_log = log_file + ".old"
        if os.path.exists(old_log):
            os.remove(old_log)
        shutil.move(log_file, old_log)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # siempre guardamos todo en log

    # Handler archivo: siempre DEBUG
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(fh)

    # Handler consola: INFO por defecto, DEBUG si verbose
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG if verbose_console else logging.INFO)
    ch.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logger.addHandler(ch)

# -----------------------
# Directorio base
# -----------------------
BASE = os.path.dirname(os.path.abspath(__file__))

# -----------------------
# CLI: solo verbose de consola
# -----------------------
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true",
                    help="Mostrar salida detallada en consola")
args = parser.parse_args()

setup_logging(verbose_console=args.verbose, log_file=os.path.join(BASE, "logs/log.txt"))

# -----------------------
# Subprogramas
# -----------------------
pipeline = [
    (BASE+"/Scripts", "DIVIDIR.py"),
    (BASE+"/Scripts", "ENSAMBLADO.py"),
    (BASE+"/Scripts", "COMPARAR.py"),
    (BASE+"/Scripts", "SÍNTESIS.py"),
]

# -----------------------
# Entrada de usuario
# -----------------------
partes = int(input("Partes (bases por fragmento)? "))

# -----------------------
# Ejecución del pipeline
# -----------------------
for carpeta, script in pipeline:
    ruta_carpeta = os.path.join(BASE, carpeta)
    ruta_script = os.path.join(ruta_carpeta, script)

    logging.info(f"▶ Ejecutando {script}")

    args_sub = [sys.executable, ruta_script]

    if script == "ENSAMBLADO.py":
        args_sub.append(str(partes))
        args_sub.append("n")

    if script == "DIVIDIR.py":
        args_sub.append(str(partes))
        args_sub.append("y")

    result = subprocess.run(
        args_sub,
        cwd=ruta_carpeta,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.stdout:
        logging.debug(result.stdout)
    if result.stderr:
        logging.error(result.stderr)

    if result.returncode != 0:
        logging.error(f"[ERROR] Error detectado en {script}. Pipeline detenido.")
        sys.exit(result.returncode)

logging.info("[OK] Pipeline completado correctamente")