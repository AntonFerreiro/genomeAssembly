import datetime
from pathlib import Path
import os

base_dir = Path(__file__).resolve().parent
project_root = Path(__file__).resolve().parents[1]
archivo_nombre = project_root/'Resultados'/'ensamblado.txt'

resultado_nombre = (
    project_root
    / "Resultados"
    / f"síntesis.txt"
)

try:
    with open(archivo_nombre, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read().replace(" ", "").replace("\n", "").replace("\r", "")
except FileNotFoundError:
    print(f"Error: El archivo '{archivo_nombre}' no se encontró.")
    exit()
except Exception as e:
    print(f"Ocurrió un error al leer el archivo: {e}")
    exit()

lectura = []

for i in range(0, len(contenido) - 3 + 1, 3):
    resultado = []
    resultado = [contenido[i:i+3]]
    lectura.append(resultado[0])

print(">> Lectura inicial: "+str(lectura))

adn_a_arn = []

for i in lectura:
    i = i.replace("T", "1").replace("C", "2").replace("A", "3").replace("G", "4")
    i = i.replace("1", "A").replace("2", "G").replace("3", "U").replace("4", "C")
    adn_a_arn.append(i)

print(">> Lectura ADN a ARN: "+str(adn_a_arn))

codigo_genetico = {
    "UUU": "Phe", "UUC": "Phe",
    "UUA": "Leu", "UUG": "Leu", "CUU": "Leu", "CUC": "Leu", "CUA": "Leu", "CUG": "Leu",
    "UCU": "Ser", "UCC": "Ser", "UCA": "Ser", "UCG": "Ser", "AGU": "Ser", "AGC": "Ser",
    "UAU": "Tyr", "UAC": "Tyr",
    "UAA": "[STOP]", "UAG": "[STOP]", "UGA": "[STOP]",
    "UGU": "Cys", "UGC": "Cys",
    "UGG": "Trp",
    "CCU": "Pro", "CCC": "Pro", "CCA": "Pro", "CCG": "Pro",
    "CAU": "His", "CAC": "His",
    "CAA": "Gln", "CAG": "Gln",
    "CGU": "Arg", "CGC": "Arg", "CGA": "Arg", "CGG": "Arg", "AGA": "Arg", "AGG": "Arg",
    "AUU": "Ile", "AUC": "Ile", "AUA": "Ile",
    "AUG": "[MET]",
    "ACU": "Thr", "ACC": "Thr", "ACA": "Thr", "ACG": "Thr",
    "AAU": "Asn", "AAC": "Asn",
    "AAA": "Lys", "AAG": "Lys",
    "GUU": "Val", "GUC": "Val", "GUA": "Val", "GUG": "Val",
    "GCU": "Ala", "GCC": "Ala", "GCA": "Ala", "GCG": "Ala",
    "GAU": "Asp", "GAC": "Asp",
    "GAA": "Glu", "GAG": "Glu",
    "GGU": "Gly", "GGC": "Gly", "GGA": "Gly", "GGG": "Gly"
}

resultado = ""

for i in adn_a_arn:
    resultado = resultado + codigo_genetico[i] + " "

print(">> Resultado: "+resultado)

os.makedirs(os.path.dirname(resultado_nombre), exist_ok=True)
try:
    with open(resultado_nombre, 'w', encoding='utf-8') as archivo_salida:
        archivo_salida.writelines(resultado)
    print(f"\n✅ Análisis completado. Resultados guardados en: {resultado_nombre}")
except Exception as e:
    print(f"\n❌ Ocurrió un error al escribir el archivo de resultados: {e}")