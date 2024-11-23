import networkx as nx
import random
import py5
import time

# Función para generar un laberinto aleatorio (grafo) garantizando que tenga solución
def generar_laberinto(n):
    G = nx.grid_2d_graph(n, n)
    edges = list(G.edges())
    random.shuffle(edges)
    maze = nx.Graph()
    maze.add_edges_from(edges[:n*n - 1])  # Agrega las aristas para el laberinto

    # Verificar que haya una solución entre el inicio y la salida
    while not nx.has_path(maze, inicio, salida):
        maze = nx.Graph()
        maze.add_edges_from(edges[:n*n - 1])

    return maze

# Configuración inicial
n = 5  # Tamaño del laberinto
jugador_pos = (0, 0)  # Posición inicial del jugador
inicio = (0, 0)
salida = (n - 1, n - 1)
tiempo_inicio = time.time()
tiempo_limite = 15  # Tiempo límite de 30 segundos
juego_perdido = False  # Flag para indicar si el jugador ha perdido
juego_ganado = False  # Flag para indicar si el jugador ha ganado
tiempo_restante = tiempo_limite  # Iniciar tiempo restante

def setup():
    py5.size(400, 400)
    py5.background(255)
    py5.stroke(0)

def draw():
    global jugador_pos, juego_perdido, juego_ganado, tiempo_restante

    py5.background(255)
    dibujar_laberinto(laberinto)
    dibujar_jugador(jugador_pos)
    dibujar_salida(salida)

    # Mostrar el tiempo restante
    if not juego_ganado and not juego_perdido:
        tiempo_actual = time.time()
        tiempo_restante = tiempo_limite - (tiempo_actual - tiempo_inicio)
        if tiempo_restante > 0:
            py5.text_size(16)
            py5.fill(0)
            py5.text(f"Tiempo restante: {int(tiempo_restante)}s", 10, 20)
        else:
            juego_perdido = True  # Si el tiempo se acabó, pierdes

    # Si el jugador llega a la salida
    if jugador_pos == salida:
        juego_ganado = True

    # Si se ha perdido o ganado, mostrar mensaje
    if juego_perdido:
        py5.text_size(32)
        py5.fill(255, 0, 0)
        py5.text("¡Perdiste! Tiempo agotado", 50, py5.height / 2)
        mostrar_solucion()
    elif juego_ganado:
        py5.text_size(32)
        py5.fill(0, 255, 0)
        py5.text("¡Ganaste! Llegaste a la salida", 50, py5.height / 2)

def dibujar_laberinto(grafo):
    for (nodo1, nodo2) in grafo.edges():
        x1, y1 = nodo1
        x2, y2 = nodo2
        py5.line(x1 * 80 + 40, y1 * 80 + 40, x2 * 80 + 40, y2 * 80 + 40)

def dibujar_jugador(pos):
    x, y = pos
    py5.fill(0, 0, 255)
    py5.ellipse(x * 80 + 40, y * 80 + 40, 20, 20)

def dibujar_salida(pos):
    x, y = pos
    py5.fill(0, 255, 0)
    py5.ellipse(x * 80 + 40, y * 80 + 40, 20, 20)

def mostrar_solucion():
    py5.stroke(255, 0, 0)
    camino = nx.shortest_path(laberinto, source=inicio, target=salida, method='bfs')
    for i in range(len(camino) - 1):
        x1, y1 = camino[i]
        x2, y2 = camino[i + 1]
        py5.line(x1 * 80 + 40, y1 * 80 + 40, x2 * 80 + 40, y2 * 80 + 40)

def key_pressed():
    global jugador_pos
    if juego_perdido or juego_ganado:
        return  # No permitir más movimientos si el juego terminó

    x, y = jugador_pos
    if py5.key == py5.CODED:
        if py5.key_code == py5.UP and (x, y-1) in laberinto.neighbors((x, y)):
            jugador_pos = (x, y-1)
        elif py5.key_code == py5.DOWN and (x, y+1) in laberinto.neighbors((x, y)):
            jugador_pos = (x, y+1)
        elif py5.key_code == py5.LEFT and (x-1, y) in laberinto.neighbors((x, y)):
            jugador_pos = (x-1, y)
        elif py5.key_code == py5.RIGHT and (x+1, y) in laberinto.neighbors((x, y)):
            jugador_pos = (x+1, y)

# Generar el laberinto asegurándose de que tiene solución
laberinto = generar_laberinto(n)

py5.run_sketch()
