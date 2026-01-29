from pathlib import Path

base_dir = Path(__file__).resolve().parent
project_root = Path(__file__).resolve().parents[1]
original_nombre = project_root/'Muestras'/'muestra.txt'
ensamblado_nombre = project_root/'Resultados'/'ensamblado.txt'

resultado_nombre = (
    project_root
    / "Resultados"
    / f"comparar.txt"
)

try:
    with open(original_nombre, 'r', encoding='utf-8') as archivo:
        original = archivo.read()
except FileNotFoundError:
    print(f"Error: El archivo '{original_nombre}' no se encontró.")
    exit()
except Exception as e:
    print(f"Ocurrió un error al leer el archivo original: {e}")
    exit()

try:
    with open(ensamblado_nombre, 'r', encoding='utf-8') as archivo:
        ensamblado = archivo.read()
except FileNotFoundError:
    print(f"Error: El archivo '{ensamblado_nombre}' no se encontró.")
    exit()
except Exception as e:
    print(f"Ocurrió un error al leer el archivo ensamblado: {e}")
    exit()

original = original.replace(" ", "").replace("\n", "").replace("\r", "")
ensamblado = ensamblado.replace(" ", "").replace("\n", "").replace("\r", "")

def alineacion_circular(original, ensamblado):
    n = len(original)
    max_coincidencia = 0
    coincidencia = ""

    original_circular = original + original

    for i in range(n):
        subcadena = original_circular[i:i+n]
        for j in range(1, n+1):
            if subcadena[:j] == ensamblado[:j]:
                if j > max_coincidencia:
                    max_coincidencia = j
                    coincidencia = subcadena[:j]

    return coincidencia, max_coincidencia

coincidencia, num = alineacion_circular(original, ensamblado)
longitud = len(original)

print("Coincidencia circular más larga: " + coincidencia)
print(f"{(num*100)/longitud:.2f}% | {num} de {longitud}")

try:
    with open(resultado_nombre, 'w', encoding='utf-8') as archivo_salida:
        archivo_salida.writelines(
            f"Coincidencia circular más larga: {coincidencia}\n"
            f"{(num*100)/longitud:.2f}% | {num} de {longitud}"
        )
    print(f"\n✅ Análisis completado. Resultados guardados en: {resultado_nombre}")

except Exception as e:
    print(f"\n❌ Ocurrió un error al escribir el archivo de resultados: {e}")