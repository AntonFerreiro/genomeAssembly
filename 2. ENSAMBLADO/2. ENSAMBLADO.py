# Programa para ordenar secuencias de codones

import datetime
import random
import networkx as nx
import matplotlib.pyplot as plt
import os

hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

base_dir = os.path.dirname(os.path.abspath(__file__))
archivo_nombre = os.path.join(base_dir, "dividido.txt")
resultado_nombre = os.path.join(base_dir, f"resultados/ensamblado_{hora}.txt")

partes = int(input("Partes? "))

##################
# LEER CONTENIDO #
##################

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
longitud_codones = int(longitud/partes)

lectura = []

for i in range(0, longitud - partes + 1, partes):
    resultado = []
    resultado = [contenido[i:i+partes]]
    lectura.append(resultado[0])

print(">> Lectura inicial: "+str(lectura))

#########################
# CONFIRMAR BALANCEADOS #
#########################

G = nx.DiGraph()
conexiones = {}

for i in range(len(lectura)):
    fromNode = lectura[i][:-1]
    toNode = lectura[i][1:]
    G.add_edge(fromNode, toNode)
    conexiones.setdefault(fromNode, [])
    conexiones[fromNode].append(toNode)
print(conexiones)

print("\n--- Análisis de Balance ---")
nodos_desbalanceados = []
for node in G.nodes():
    in_d = G.in_degree(node)
    out_d = G.out_degree(node)
    if in_d != out_d:
        nodos_desbalanceados.append((node, in_d, out_d))

principioyfinal = False
primero = None
ultimo = None

if not nodos_desbalanceados:
    print("El grafo está balanceado.")
else:
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
            print("El grafo NO está balanceado. Hay 2 nodos desbalanceados:")
            for n, i, o in nodos_desbalanceados:
                print(f"  Nodo '{n}': in={i}, out={o}")
            exit()
    else:
      print(f"El grafo NO está balanceado. Hay {len(nodos_desbalanceados)} nodos desbalanceados:")
      for n, i, o in nodos_desbalanceados:
          print(f"  Nodo '{n}': in={i}, out={o}")
      exit()

###########
# ORDENAR #
###########

if principioyfinal:
    conexiones.setdefault(ultimo, [])
    conexiones[ultimo].append(primero)
reconstruccion = []
ciclo_actual = []

if principioyfinal == True:
    inicio = primero
else:
    inicio = 0

def ciclo(actual, primero, empezando):
    if (empezando):
        ciclo_actual.append(primero)
    else:
        if (actual != primero):
            ciclo_actual.append(actual)
        else:
            return
    if conexiones[actual]:
        conexion = conexiones[actual][0]
        if len(conexiones[actual]) == 1:
            conexiones.pop(actual)
        else:
            conexiones[actual].pop(0)
        ciclo(conexion, primero, False)
    else:
        return

ciclo(inicio, inicio, True)
reconstruccion.append(ciclo_actual)
while len(conexiones) > 0:
    ciclo_actual = []
    actual = 0
    for i in range(len(conexiones)):
        num = conexiones.get(i)
        if (num != None):
            actual = i
            break
    claves_lista = list(conexiones.keys())
    actual = claves_lista[actual]
    ciclo(actual, actual, True)
    reconstruccion.append(ciclo_actual)     

print(reconstruccion)

reconstruido = []

# Reconstrucción principal

while len(reconstruccion) > 2:
    nueva_reconstruccion = []
    actual = 0
    numParte0 = 0
    parte_0 = reconstruccion[0]
    parte_1 = reconstruccion[1]
    if primero in parte_1 and ultimo in parte_1:
        for i in parte_1:
            if i == ultimo and i+1 == primero:
                parte_0 = reconstruccion[0]
                parte_1 = reconstruccion[2]
                reconstruccion.pop(2)
                break
    if primero in parte_0 and ultimo in parte_0:
        for i in parte_0:
            if i == ultimo and i+1 == primero:
                parte_0 = reconstruccion[2]
                parte_1 = reconstruccion[1]
                reconstruccion.pop(1)
                numParte0 = 2
                break
    num = -1
    for i in parte_1:
        if i in parte_0:
            num = i
            break
    if num != -1:
        for i in parte_0:
            if i != num:
                nueva_reconstruccion.append(i)
            else:
                for e in parte_1:
                    nueva_reconstruccion.append(e)
                nueva_reconstruccion.append(i)
        reconstruccion[numParte0] = nueva_reconstruccion

# Reconstrucción de los últimos nodos
nueva_reconstruccion = []
actual = 0
parte_0 = reconstruccion[0]
parte_1 = reconstruccion[1]
queParte = 2
numUltimo = -1
subreordenado = []
extra = []
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

while subreordenado[-1] != ultimo:
    cambiar = subreordenado[0]
    subreordenado.pop(0)
    subreordenado.append(cambiar)

if queParte == 1:
    reconstruccion[1] = subreordenado
else:
    reconstruccion[0] = subreordenado

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

# Reconstrucción final

nodos = []
reconstruido = reconstruccion[0]

for i in reconstruido:
    nodos.append(i)

ensamblaje = []

for i in range(len(reconstruido)):
    if i == 0:
        ensamblaje.append(reconstruido[i])
    else:
        ensamblaje.append(reconstruido[i][-1])

print("-- Nodos ordenados: "+str(nodos))
print("-- Ensamblaje final: "+str(ensamblaje))

#####################
# GUARDAR RESULTADO #
#####################

try:
    with open(resultado_nombre, 'w', encoding='utf-8') as archivo_salida:
        archivo_salida.writelines(">> Ensamblaje:"+"\n")
        for i in ensamblaje:
            archivo_salida.writelines(i)
        archivo_salida.writelines("\n"+">> Nodos:"+"\n")
        for i in nodos:
            archivo_salida.writelines(i + "\n")
    print(f"\n✅ Análisis completado. Resultados guardados en: {resultado_nombre}")

except Exception as e:
    print(f"\n❌ Ocurrió un error al escribir el archivo de resultados: {e}")

nx.draw(G, with_labels=True, node_color='lightblue', edge_color='red', arrows=True)
plt.title("Grafo Dirigido")
plt.show()