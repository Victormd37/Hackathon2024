import pandas as pd
import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
import imageio
import os


def crear_matriz_tienda(dataset, filas, columnas, capacidad_maxima):
    matriz_tienda = np.empty((filas, columnas), dtype=object)
    fila_actual = 0
    columna_actual = 0

    for indice, producto in dataset.iterrows():
        numero_random = random.randint(50, 100)
        if matriz_tienda[fila_actual, columna_actual] is None:
            matriz_tienda[fila_actual, columna_actual] = [[(producto["id"], numero_random)], numero_random]
        elif matriz_tienda[fila_actual, columna_actual][1] + numero_random < capacidad_maxima:
            matriz_tienda[fila_actual, columna_actual][0].append((producto["id"], numero_random))
            matriz_tienda[fila_actual, columna_actual][1] += numero_random

        else:
            if fila_actual == filas-1:
                columna_actual += 1
                fila_actual = 0
            else:
                fila_actual += 1

            matriz_tienda[fila_actual, columna_actual] = [[(producto["id"], numero_random)], numero_random]

    return matriz_tienda

def crear_grafo_tienda(matriz_tienda):
    nodos = []  # Lista para almacenar todos los nodos
    nodos_fila = set()  # Conjunto para almacenar los nodos de la primera y última fila
    nodos_columna = set()  # Conjunto para almacenar los nodos de cada columna

    # Recorrer la matriz para identificar los nodos
    for col in range(matriz_tienda.shape[1]):
        for row in range(matriz_tienda.shape[0]):
            nodo = (row, col)
            nodos.append(nodo)  # Agregar nodo a la lista de todos los nodos
            nodos_columna.add(nodo)  # Agregar nodo al conjunto de nodos de la columna

            # Si el nodo está en la primera o última fila, agregarlo al conjunto de nodos de fila
            if row == 0 or row == matriz_tienda.shape[0] - 1:
                nodos_fila.add(nodo)

    # Crear el grafo
    G = nx.DiGraph()

    # Añadir nodos al grafo
    for nodo in nodos:
        G.add_node(nodo)

    # Conectar los nodos de la misma columna
    for columna in nodos_columna:
        fila, col = columna
        if fila < matriz_tienda.shape[0] - 1:
            G.add_edge(columna, (fila + 1, col), weight=1)  # Conectar con el nodo debajo (si existe)
        if fila > 0:
            G.add_edge(columna, (fila - 1, col), weight=1)  # Conectar con el nodo encima (si existe)
        if fila == 0 or fila == matriz_tienda.shape[0] - 1:
            if col == 0:
                G.add_edge(columna, (fila, col + 1), weight=1)  # Conectar con el nodo a la derecha (si es el borde izquierdo)
            elif col == matriz_tienda.shape[1] - 1:
                G.add_edge(columna, (fila, col - 1), weight=1)  # Conectar con el nodo a la izquierda (si es el borde derecho)
            else:
                G.add_edge(columna, (fila, col + 1), weight=1)  # Conectar con el nodo a la derecha
                G.add_edge(columna, (fila, col - 1), weight=1)  # Conectar con el nodo a la izquierda

    return G


def tsp_comanda(df,grafo_tienda, comanda, matriz_tienda, nodo_inicial):
    # Inicializar el camino óptimo
    camino_optimo = []
    
    copia_comanda = comanda.copy()
    
    # Crear una copia del grafo para realizar modificaciones sin afectar al original
    grafo_modificado = grafo_tienda.copy()
    
    
    nodos_comanda_disponibles_grafo = []
    productos_grafo = []
    for fila in range(len(matriz_tienda)):
        for columna in range(len(matriz_tienda[0])):
            productos_celda = matriz_tienda[fila][columna][0] if matriz_tienda[fila][columna] else []
            for producto in productos_celda:
                if str(producto[0]) in comanda:
                    nodos_comanda_disponibles_grafo.append((fila, columna))
                    productos_grafo.append(producto)
    

    # Mientras haya productos en la comanda
    while comanda:
        # Obtener el nodo más cercano al último nodo del camino óptimo
        nodo_actual = camino_optimo[-1] if camino_optimo else nodo_inicial
        
        # Obtener los nodos de la comanda que están presentes en la matriz de la tienda
        nodos_comanda_disponibles = []
        productos = []
        for fila in range(len(matriz_tienda)):
            for columna in range(len(matriz_tienda[0])):
                productos_celda = matriz_tienda[fila][columna][0] if matriz_tienda[fila][columna] else []
                for producto in productos_celda:
                    if str(producto[0]) in comanda:
                        nodos_comanda_disponibles.append((fila, columna))
                        productos.append(producto)
                        break


        if nodos_comanda_disponibles:
            # Calcular la distancia mínima y el nodo más cercano en la comanda
            distancia_minima = float('inf')
            nodo_mas_cercano = None
            for fila, columna in nodos_comanda_disponibles:
                distancia = nx.shortest_path_length(grafo_modificado, source=nodo_actual, target=(fila, columna), weight='weight')
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    nodo_mas_cercano = (fila, columna)
                                
            producto_mas_cercano = productos[nodos_comanda_disponibles.index(nodo_mas_cercano)]
                    
            # Agregar el nodo al camino óptimo
            camino_optimo.append(nodo_mas_cercano)
            
            # Obtener la cantidad disponible del producto en la matriz de la tienda
            cantidad_disponible = producto_mas_cercano[1]
            
            # Obtener la cantidad requerida en la comanda
            cantidad_requerida = comanda[str(producto_mas_cercano[0])]
            
            # Calcular la cantidad a tomar (mínimo entre la disponible y la requerida)
            cantidad_a_tomar = min(cantidad_disponible, cantidad_requerida)

            # Actualizar la cantidad en la comanda (si se toma menos de lo requerido)
            if cantidad_a_tomar < cantidad_requerida:
                comanda[str(producto_mas_cercano[0])] -= cantidad_a_tomar
                #print(f"Faltan: {comanda[str(producto_mas_cercano[0])]} productos de {producto_mas_cercano[0]}")
                del comanda[str(producto_mas_cercano[0])] 
            else:
                del comanda[str(producto_mas_cercano[0])]  # Eliminar el producto de la comanda si se toma la cantidad requerida

            # Actualizar la matriz modificada
            matriz_tienda[nodo_mas_cercano[0]][nodo_mas_cercano[1]][1] -= cantidad_a_tomar

            # Imprimir mensaje de cuánto se tomó del producto
            #print(f"Se tomaron {cantidad_a_tomar} unidades del producto en la ubicación {nodo_mas_cercano}")
 
        
        # Si no se encontraron productos de la comanda en la matriz, terminar el bucle
        if not nodos_comanda_disponibles:
            break
        
    for pr in  range(len(productos_grafo)):
        
        nodo = nodos_comanda_disponibles_grafo[pr]
        
        producto = productos_grafo[pr]
        
        cantidad_disponible = producto[1]
            
       
        cantidad_requerida = copia_comanda[str(producto[0])]
        
        # Calcular la cantidad a tomar (mínimo entre la disponible y la requerida)
        cantidad_a_tomar = min(cantidad_disponible, cantidad_requerida)
        
        productos_grafo[pr] = (productos_grafo[pr][0],cantidad_a_tomar)

    # Agregar los nodos intermedios y la conexión con el nodo inicial al camino óptimo
    camino_optimo_intermedio = []
    for i in range(len(camino_optimo) - 1):
        camino_optimo_intermedio.append(camino_optimo[i])
        trayecto_intermedio = nx.shortest_path(grafo_modificado, source=camino_optimo[i], target=camino_optimo[i+1], weight='weight')[1:]
        # Si el siguiente nodo es diferente al actual, agregarlo al camino
        if trayecto_intermedio:
            camino_optimo_intermedio += trayecto_intermedio

    # Si hay nodos en el camino, agregar el último nodo y la conexión con el nodo inicial
    if camino_optimo:
        ultimo_nodo = camino_optimo[-1]
        trayecto_final = nx.shortest_path(grafo_modificado, source=ultimo_nodo, target=nodo_inicial, weight='weight')
        # Si hay un trayecto desde el último nodo hasta el inicial
        if trayecto_final:
            # Si el siguiente nodo es diferente al actual, agregarlo al camino
            if trayecto_final[1] != ultimo_nodo:
                camino_optimo_intermedio += trayecto_final[1:]

    # Agregar la conexión con el nodo inicial
    if camino_optimo_intermedio and camino_optimo_intermedio[-1] != nodo_inicial:
        camino_optimo_intermedio.append(nodo_inicial)

    # Eliminar nodos repetidos consecutivos
    camino_optimo_final = [camino_optimo_intermedio[0]]
    for nodo in camino_optimo_intermedio[1:]:
        if nodo != camino_optimo_final[-1]:
            camino_optimo_final.append(nodo)
            
            
    # Dibujar el grafo con los nodos visitados hasta el momento

    # Lista para almacenar los nombres de los archivos de imagen
    image_files = []
    
    path = []
    
    if camino_optimo_final[0] != nodo_inicial:
        camino_optimo_final.insert(0, nodo_inicial)

    
    # Recorrer cada paso del camino óptimo y guardar cada plot como una imagen PNG
    for x in range(len(camino_optimo_final)):
        lista_aux = camino_optimo_final[0:x+1] 
        fig, ax = plt.subplots(figsize=(8, 8))
        pos = {x: x for x in grafo_modificado.nodes}
        nx.draw(grafo_modificado, ax=ax, node_color='#bbbb22', pos=pos)
        # Resaltar los nodos visitados hasta el momento en azul, excepto el último en rojo
        nx.draw_networkx_nodes(grafo_modificado, ax=ax, nodelist=lista_aux[:-1], node_color='red', pos=pos)
        nx.draw_networkx_labels(grafo_modificado, ax=ax, pos={x: (x[0]+0.2, x[1]+0.2) for x in grafo_modificado.nodes})
                
        if x == 0 and lista_aux[-1] == nodo_inicial and lista_aux[-1] in camino_optimo:
            nx.draw_networkx_nodes(grafo_modificado, ax=ax, nodelist=[lista_aux[-1]], node_color='green', pos=pos)  
            move = f"Start  at location {lista_aux[-1]} and pick {productos_grafo[nodos_comanda_disponibles_grafo.index(lista_aux[-1])][1]} units of {df.loc[df['id'] == productos_grafo[nodos_comanda_disponibles_grafo.index(lista_aux[-1])][0], 'name'].iloc[0]}"
            plt.title(move)
            camino_optimo.remove(lista_aux[-1])
            
        elif  x == 0 and lista_aux[-1] != nodo_inicial:
            nx.draw_networkx_nodes(grafo_modificado, ax=ax, nodelist=[lista_aux[-1]], node_color='blue', pos=pos)  
            move = f"Start  at location {nodo_inicial}"
            plt.title(move)

        elif  x == 0 and lista_aux[-1] == nodo_inicial:
            nx.draw_networkx_nodes(grafo_modificado, ax=ax, nodelist=[lista_aux[-1]], node_color='blue', pos=pos)  
            move = f"Start  at location {lista_aux[-1]}"
            plt.title(move)
            
        elif lista_aux[-1] in camino_optimo:
            nx.draw_networkx_nodes(grafo_modificado, ax=ax, nodelist=[lista_aux[-1]], node_color='green', pos=pos)  
            values = [v for v in camino_optimo if v == lista_aux[-1] ]
            if len(values) == 1:
                move = f"Move at location {lista_aux[-1]} and pick {productos_grafo[nodos_comanda_disponibles_grafo.index(lista_aux[-1])][1]} units of {df.loc[df['id'] == productos_grafo[nodos_comanda_disponibles_grafo.index(lista_aux[-1])][0], 'name'].iloc[0]}"
            else:
                products = []
                for pr in values:
                    products.append((productos_grafo[nodos_comanda_disponibles_grafo.index(pr)][0], productos_grafo[nodos_comanda_disponibles_grafo.index(pr)][1]))
                    productos_grafo.remove(productos_grafo[nodos_comanda_disponibles_grafo.index(pr)])

                product_names = ", ".join([f"{cantidad} units of {df.loc[df['id'] == p_id, 'name'].iloc[0]}" for p_id, cantidad in products])
                move = f"Move at location {lista_aux[-1]}\nand pick {len(products)} products:\n{product_names}"
               
            plt.title(move)
            camino_optimo.remove(lista_aux[-1])
            
        elif x+1 == len(camino_optimo_final):
            nx.draw_networkx_nodes(grafo_modificado, ax=ax, nodelist=[lista_aux[-1]], node_color='purple', pos=pos)  
            move = f"Move to location {lista_aux[-1]} to finish"
            plt.title(move)
            
        elif lista_aux[-1] in camino_optimo and x+1 == len(camino_optimo_final):
            nx.draw_networkx_nodes(grafo_modificado, ax=ax, nodelist=[lista_aux[-1]], node_color='green', pos=pos)  
            move = f"Move at location {lista_aux[-1]} and pick {productos_grafo[nodos_comanda_disponibles_grafo.index(lista_aux[-1])][1]} units of {df.loc[df['id'] == productos_grafo[nodos_comanda_disponibles_grafo.index(lista_aux[-1])][0], 'name'].iloc[0]} to finish"
            plt.title(move)
        
        else:
            nx.draw_networkx_nodes(grafo_modificado, ax=ax, nodelist=[lista_aux[-1]], node_color='blue', pos=pos)  
            move = f"Move to location {lista_aux[-1]}"
            plt.title(move)
        # Guardar el plot como una imagen PNG
        path.append(move)
        filename = f"plot_{x}.png"
        plt.savefig(filename)
        plt.close()
        image_files.append(filename)

    # Crear el GIF a partir de las imágenes guardadas
    with imageio.get_writer('camino_optimo.gif', mode='I', duration=2000) as writer:
        for filename in image_files:
            image = imageio.imread(filename)
            writer.append_data(image)

    # Eliminar los archivos de imagen temporales
    for filename in set(image_files):
        os.remove(filename)


    return camino_optimo_final, path

def do_planning(comanda={}):
    filas = 5
    columnas = 5
    capacidad_maxima = 450
    df = pd.read_csv('products.csv', delimiter=";")
    matriz_tienda = crear_matriz_tienda(df, filas, columnas, capacidad_maxima)
    grafo_tienda = crear_grafo_tienda(matriz_tienda)
    #comanda = {"45": 80, "56": 52, "1068": 73, "562": 2}
    print(comanda)
    nodo_inicial = (0, 0)
    _, path = tsp_comanda(df, grafo_tienda, comanda, matriz_tienda, nodo_inicial)
    for p in path:
        print(p)