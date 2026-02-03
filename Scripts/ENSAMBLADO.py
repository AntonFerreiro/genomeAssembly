###################################################
# 2. ENSAMBLADO --> ENSAMBLAR MUESTRA DESORDENADA #
###################################################

# Librerías
import networkx as nx
import matplotlib.pyplot as plt
import sys
from pathlib import Path

# Directorio de archivos
base_dir = Path(__file__).resolve().parent
project_root = Path(__file__).resolve().parents[1]
archivo_nombre = project_root/'Resultados'/'dividido.txt'
grafo_nombre = project_root/'Resultados'/'grafo.png'

resultado_nombre = (
    project_root
    / "Resultados"
    / f"ensamblado.txt"
)

# Si no recibe argumentos al ejecutar, que pida por teclado la longitud de los fragmentos
if len(sys.argv) > 1:
    partes = int(sys.argv[1])
else:
    partes = int(input("Partes? "))

# Intentar leer la muestra desordenada
try:
    with open(archivo_nombre, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
except FileNotFoundError:
    print(f"Error: El archivo '{archivo_nombre}' no se encontró.")
    exit()
except Exception as e:
    print(f"Ocurrió un error al leer el archivo: {e}")
    exit()

# Eliminar espacios y saltos de línea
contenido = contenido.replace(" ", "").replace("\n", "").replace("\r", "")

lectura = []

# Dividir la muestra en fragmentos de longitud k
for i in range(0, len(contenido) - partes + 1, partes):
    resultado = []
    resultado = [contenido[i:i+partes]]
    lectura.append(resultado[0])

print(">> Lectura inicial: "+str(lectura))

# Crear grafo
G = nx.MultiDiGraph()
conexiones = {}

# Añadir cada nodo al grafo y guardarlo en una lista para próximo uso en el ensamblaje
for i in range(len(lectura)):
    fromNode = lectura[i][:-1]
    toNode = lectura[i][1:]
    G.add_edge(fromNode, toNode)
    conexiones.setdefault(fromNode, [])
    conexiones[fromNode].append(toNode)
print(conexiones)

# Revisar si están balanceados
print("\n--- Análisis de Balance ---")
nodos_desbalanceados = []
for node in G.nodes(): # Revisar si tienen = número de entradas que salidas
    in_d = G.in_degree(node)
    out_d = G.out_degree(node)
    if in_d != out_d:
        nodos_desbalanceados.append((node, in_d, out_d))

principioyfinal = False # Variable para ver si tiene un inicio y final determinado
primero = None # Primer nodo
ultimo = None # Último nodo

# Análisis de balance
if not nodos_desbalanceados: # Si no hay nodos desbalanceados
    print("El grafo está balanceado.")
else:
    # Revisar si están desbalanceados porque uno es el primero y el otro el último
    if (len(nodos_desbalanceados) == 2):
        if (nodos_desbalanceados[0][2] == nodos_desbalanceados[0][1]+1) and (nodos_desbalanceados[1][2]+1 == nodos_desbalanceados[1][1]):
            principioyfinal = True
            primero = nodos_desbalanceados[0][0]
            ultimo = nodos_desbalanceados[1][0]
            print(">> Primero: "+primero)
            print(">> Último: "+ultimo)
        elif (nodos_desbalanceados[0][2]+1 == nodos_desbalanceados[0][1]) and (nodos_desbalanceados[1][2] == nodos_desbalanceados[1][1]+1):
            principioyfinal = True
            primero = nodos_desbalanceados[1][0]
            ultimo = nodos_desbalanceados[0][0]
            print(">> Primero: "+primero)
            print(">> Último: "+ultimo)
        else:
            # Si no son el primero y el último
            print("El grafo NO está balanceado. Hay 2 nodos desbalanceados:")
            for n, i, o in nodos_desbalanceados:
                print(f"  Nodo '{n}': in={i}, out={o}")
            exit()
    else:
        # Si hay más de 2 nodos desbalanceados (no son el primero y el último)
        print(f"El grafo NO está balanceado. Hay {len(nodos_desbalanceados)} nodos desbalanceados:")
        for n, i, o in nodos_desbalanceados:
            print(f"  Nodo '{n}': in={i}, out={o}")
        exit()

# Función para hacer los ciclos por recursividad
def ciclo(actual, primero, empezando):
    # Si es el primer nodo del ciclo
    if (empezando):
        ciclo_actual.append(primero)
    # Si no es el primer nodo del ciclo
    else:
        # Revisar si ya se ha completado el ciclo
        if (actual != primero):
            ciclo_actual.append(actual)
        else:
            return
    # Revisar las conexiones y elegir una para continuar el ciclo
    if conexiones[actual]:
        conexion = conexiones[actual][0]
        conexiones[actual].pop(0)
        if len(conexiones[actual]) == 0:
            del conexiones[actual]
        ciclo(conexion, primero, False)
    else:
        return

# Si tiene un principio y un final determinado, agregar conexión del primero con el último
if principioyfinal:
    conexiones.setdefault(ultimo, [])
    conexiones[ultimo].append(primero)

# Reconstrucción
reconstruccion = []
ciclo_actual = []

# Elegir el nodo con el que empezar el ciclo
if principioyfinal == True:
    # Hay un inicio y un final, por lo que usaremos el primero para empezar
    inicio = primero
else:
    # No hay un inicio y un final, por lo que usaremos el primer nodo para empezar
    inicio = next(iter(conexiones))

# Usar la función para obtener el ciclo
ciclo(inicio, inicio, True)
# Guardamos el ciclo en una lista, donde se irán añadiendo todos los que se hagan
reconstruccion.append(ciclo_actual)

# Mientras haya conexiones, continuar con los ciclos
while len(conexiones) > 0:
    ciclo_actual = []
    actual = 0
    # Revisar las conexiones
    for i in range(len(conexiones)):
        num = conexiones.get(i)
        if (num != None):
            actual = i
            break
    # Obtener un fragmento y empezar un nuevo ciclo
    claves_lista = list(conexiones.keys())
    actual = claves_lista[actual]
    ciclo(actual, actual, True)
    # Guardamos el ciclo en la lista
    reconstruccion.append(ciclo_actual) 
print(reconstruccion)

reconstruido = []

# UNIR CICLOS

# Mientras haya más de 2 ciclos, unirlos
while len(reconstruccion) > 2:
    nueva_reconstruccion = []
    actual = 0
    numParte0 = 0
    parte_0 = reconstruccion[0]
    parte_1 = reconstruccion[1]
    # Si el primer nodo y el último nodo están en el primer fragmento, reconstruir aquí
    if primero in parte_1 and ultimo in parte_1:
        for i in range(len(parte_1)):
            nodo_actual = parte_1[i]
            siguiente_nodo = parte_1[i + 1] if i + 1 < len(parte_1) else parte_1[0]
            
            if nodo_actual == ultimo and siguiente_nodo == primero:
                parte_0 = reconstruccion[0]
                parte_1 = reconstruccion[2]
                reconstruccion.pop(2)
                break
    # Si el primer nodo y el último nodo están en el segundo fragmento, reconstruir aquí
    if primero in parte_0 and ultimo in parte_0:
        for i in range(len(parte_0)):
            nodo_actual = parte_0[i]
            siguiente_nodo = parte_0[i + 1] if i + 1 < len(parte_0) else parte_0[0]
                
            if nodo_actual == ultimo and siguiente_nodo == primero:
                parte_0 = reconstruccion[2]
                parte_1 = reconstruccion[1]
                reconstruccion.pop(1)
                numParte0 = 2
                break

    # Buscar el nodo común entre los dos fragmentos
    num = -1
    for i in parte_1:
        # Encuentra el nodo común entre los dos fragmentos
        if i in parte_0:
            num = i
            break
    if num != -1:
        # Unir los dos fragmentos en el que comparten
        for i in parte_0:
            if i != num:
                nueva_reconstruccion.append(i)
            else:
                for e in parte_1:
                    nueva_reconstruccion.append(e)
                nueva_reconstruccion.append(i)
        reconstruccion[numParte0] = nueva_reconstruccion
        if numParte0 == 0:
            reconstruccion.pop(1)
        else:
            reconstruccion.pop(0)

# RECONSTRUCCIÓN DE LOS ÚLTIMOS 2 CICLOS

# Mismo proceso que el de arriba, pero con los últimos 2 ciclos
if len(reconstruccion) == 2:
    nueva_reconstruccion = []
    actual = 0
    parte_0 = reconstruccion[0]
    parte_1 = reconstruccion[1]
    queParte = 2
    numUltimo = -1
    subreordenado = []
    extra = []
    # Si el primer nodo y el último nodo están en el primer fragmento
    if primero in parte_1 and ultimo in parte_1:
        for i in range(len(parte_1)):
            if i == len(parte_1)-1 and parte_1[i] == ultimo and parte_1[0] == primero:
                queParte = 1
                subreordenado = parte_1
                extra = parte_0
                break
            elif parte_1[i] == ultimo and parte_1[i+1] == primero:
                queParte = 1
                subreordenado = parte_1
                extra = parte_0
                break
    if queParte == 2 and (primero in parte_0 and ultimo in parte_0):
        for i in range(len(parte_0)):
            if i == len(parte_0)-1 and parte_0[i] == ultimo and parte_0[0] == primero:
                queParte = 0
                subreordenado = parte_0
                extra = parte_1
                break
            elif parte_0[i] == ultimo and parte_0[i+1] == primero:
                queParte = 0
                subreordenado = parte_0
                extra = parte_1
                break
    # Si el último nodo está en el subreordenado
    if ultimo in subreordenado:
        contador = 0
        max_rotaciones = len(subreordenado) + 1

        while subreordenado[-1] != ultimo and contador < max_rotaciones:
            cambiar = subreordenado[0]
            subreordenado.pop(0)
            subreordenado.append(cambiar)
            contador += 1

    if queParte == 1:
        reconstruccion[1] = subreordenado
    else:
        reconstruccion[0] = subreordenado

    # Unir los dos fragmentos
    num = -1
    for i in subreordenado:
        if i in extra:
            num = i
            break
    if num != -1:
        for i in subreordenado:
            if i != num:
                nueva_reconstruccion.append(i)
            else:
                for e in extra:
                    nueva_reconstruccion.append(e)
                nueva_reconstruccion.append(i)
        reconstruccion[0] = nueva_reconstruccion
    

# RECONSTRUCCIÓN FINAL

nodos = []
reconstruido = reconstruccion[0]

# Meter todas las letras ordenadas en una lista
for i in reconstruido:
    nodos.append(i)

ensamblaje = []

# Meter todas las letras ordenadas en una lista
for i in range(len(reconstruido)):
    if i == 0:
        ensamblaje.append(reconstruido[i])
    else: # Meter la última letra de cada fragmento
        ensamblaje.append(reconstruido[i][-1])

# Si hay un primer y último nodo diferenciado, hacer un corte para que el ensamblaje sea correcto
if principioyfinal:
    corte = None
    for i in range(len(nodos)-1):
        if nodos[i] == ultimo and nodos[i+1] == primero:
            corte = i+1
            break

    if corte is not None:
        nodos = nodos[:corte]
        ensamblaje = ensamblaje[:corte]
else:
    ensamblaje.append(reconstruido[0][-1])

# Mostrar resultados
print("-- Nodos ordenados: "+str(nodos))
print("-- Ensamblaje final: "+str("".join(ensamblaje)))

# Guardar resultados
try:
    with open(resultado_nombre, 'w', encoding='utf-8') as archivo_salida:
        archivo_salida.writelines(str("".join(ensamblaje)))
    print(f"\n✅ Análisis completado. Resultados guardados en: {resultado_nombre}")

except Exception as e:
    print(f"\n❌ Ocurrió un error al escribir el archivo de resultados: {e}")

# Preparar y guardar grafo
nx.draw(G, with_labels=True, node_color='lightblue', edge_color='red', arrows=True)
plt.title("Grafo Dirigido")
plt.savefig(grafo_nombre)

# Si se le pasa un argumento, mostrar el grafo, sino preguntar si se quiere mostrar
if len(sys.argv) > 2:
    recibido = sys.argv[2]
    if recibido == "y" or recibido == "yes":
        plt.show()
else:
    mostrar = input("Mostrar grafo? y/n: ")
    if mostrar == "y" or mostrar == "yes":
        plt.show()