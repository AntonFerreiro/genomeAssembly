import sys
from pathlib import Path
import borjafork as dna

base_dir = Path(__file__).resolve().parent
project_root = Path(__file__).resolve().parents[1]
archivo_nombre = project_root/'Resultados'/'ensamblado.txt'

resultado_nombre = (
    project_root
    / "Resultados"
    / f"síntesis.txt"
)

if len(sys.argv) >= 2:
    secuencia = sys.argv[1]
else:
    try:
        with open(archivo_nombre, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
    except FileNotFoundError as e:
        print(f"Error: El archivo '{archivo_nombre}' no se encontró.")
        exit(e)
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        exit()
    #except:
    #    secuencia = input("Introduzca la secuencia: \n")
resultado = dna.proteinList(secuencia)
print("Resultado:" + resultado)

try:
    with open(resultado_nombre, 'w', encoding='utf-8') as archivo_salida:
        archivo_salida.writelines(str("".join(resultado)))
    print(f"\n✅ Síntesis completada. Resultados guardados en: {resultado_nombre}")

except Exception as e:
    print(f"\n❌ Ocurrió un error al escribir el archivo de resultados: {e}")
