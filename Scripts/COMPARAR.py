##########################################################
# 3. COMPARAR --> COMPARAR MUESTRA ORIGINAL Y ENSAMBLADA #
##########################################################

# Librerías
from pathlib import Path

# Directorio de archivos
base_dir = Path(__file__).resolve().parent
project_root = Path(__file__).resolve().parents[1]
original_nombre = project_root/'Muestras'/'muestra.txt'
ensamblado_nombre = project_root/'Resultados'/'ensamblado.txt'

resultado_nombre = (
    project_root
    / "Resultados"
    / f"comparar.txt"
)

# Intentar leer archivos

# Muestra original
try:
    with open(original_nombre, 'r', encoding='utf-8') as archivo:
        original = archivo.read()
except FileNotFoundError:
    print(f"Error: El archivo '{original_nombre}' no se encontró.")
    exit()
except Exception as e:
    print(f"Ocurrió un error al leer el archivo original: {e}")
    exit()

# Muestra ensamblada
try:
    with open(ensamblado_nombre, 'r', encoding='utf-8') as archivo:
        ensamblado = archivo.read()
except FileNotFoundError:
    print(f"Error: El archivo '{ensamblado_nombre}' no se encontró.")
    exit()
except Exception as e:
    print(f"Ocurrió un error al leer el archivo ensamblado: {e}")
    exit()

# Quitar espacios y saltos de línea
original = original.replace(" ", "").replace("\n", "").replace("\r", "")
ensamblado = ensamblado.replace(" ", "").replace("\n", "").replace("\r", "")

# Función alineación circular
def alineacion_circular(original, ensamblado):
    n = len(original)
    max_coincidencia = 0
    coincidencia = ""

    original_circular = original + original

    # Busca la coincidencia circular más larga, comparando subcadenas
    for i in range(n):
        subcadena = original_circular[i:i+n]
        for j in range(1, n+1):
            if subcadena[:j] == ensamblado[:j]:
                if j > max_coincidencia:
                    max_coincidencia = j
                    coincidencia = subcadena[:j]

    return coincidencia, max_coincidencia

# Usar la función para obtener la coincidencia circular más larga
coincidencia, num = alineacion_circular(original, ensamblado)
longitud = len(original)

# Resultado
print("Coincidencia circular más larga: " + coincidencia) # Resultado con el fragmento más largo
print(f"{(num*100)/longitud:.2f}% | {num} de {longitud}") # Resultado con el porcentaje de coincidencia

# Guardar resultados
try:
    with open(resultado_nombre, 'w', encoding='utf-8') as archivo_salida:
        archivo_salida.writelines(
            f"Coincidencia circular más larga: {coincidencia}\n"
            f"{(num*100)/longitud:.2f}% | {num} de {longitud}"
        )
    print(f"\n✅ Análisis completado. Resultados guardados en: {resultado_nombre}")

except Exception as e:
    print(f"\n❌ Ocurrió un error al escribir el archivo de resultados: {e}")