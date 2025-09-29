from utils import *
import numpy as np
import random

tamaño_tablero = 10

# Constructor del tablero a visualizar
numeracion = np.array(["/",0,1,2,3,4,5,6,7,8,9])
tablero_vis = crear_tablero(11)
tablero_vis[0, :] = numeracion
tablero_vis[:, 0] = numeracion

# Generar el tablero del jugado
tablero_jugador = crear_tablero(tamaño_tablero)
colocar_barcos(tablero_jugador)

# Generar el tablero de la maquina
tablero_skynet = crear_tablero(tamaño_tablero)
colocar_barcos(tablero_skynet)

# Generar un tablero vacío para mostrar los intentos del jugador
tablero_vacio = crear_tablero(tamaño_tablero)

# Turno incial y cantidad de turnos de juego
turno = 1
turnos_totales = 10

# Contador inicial con la cantidad de casillas ocupadas por barcos
barcos_jugador = np.count_nonzero(tablero_jugador == "O")
barcos_skynet = np.count_nonzero(tablero_skynet == "O")

# Registro de ataques de Skynet
coord_skynet = []

# La partida continua mientras no se acaben los turnos y queden barcos en alguno de los tableros
while turno <= 10 and barcos_jugador > 0 and barcos_skynet > 0:
    print(f"Turno {turno} de {turnos_totales}")
    print("Tu Tablero")
    tablero_vis[1: 11, 1: 11] = tablero_jugador
    print(tablero_vis)
    print()
    print("Tablero enemigo")
    tablero_vis[1: 11, 1: 11] = tablero_vacio
    print(tablero_vis)

    # Inicializamos el ataque
    ataque = "Empezamos"
    while ataque != "Agua":    

        disparo_en_rango = False
        # Comprobador para la casilla a la que disparar
        while not disparo_en_rango:
            casilla = input("Introduce la casilla a la que vas a disparar (fila,columna): ")
            try:
                fila, columna = map(int, casilla.split(","))
                if 0 <= fila < tamaño_tablero and 0 <= columna < tamaño_tablero:
                    disparo_en_rango = True
                else:
                    print("Las coordenas de ataque no son válidas, insertelas de nuevo.")
            except ValueError:
                print("Las coordenadas están mal introducidas. Usar formato fila,columna")

        # Ataque sobre el tablero enemigo
        ataque = disparar((fila, columna), tablero_skynet)
        print(ataque)
        if ataque == "Tocado":
            tablero_vacio[(fila, columna)] = "X"
            tablero_vis[1: 11, 1: 11] = tablero_vacio
            print(tablero_vis)
        else:
            tablero_vacio[(fila, columna)] = "A"
        # Comrprobación del número de barcos enemigos que quedan
        barcos_skynet = np.count_nonzero(tablero_skynet == "O")

        # Si no quedan barcos enemigos, has ganado
        if barcos_skynet == 0:
            print("Has ganado")
            break

    # Ataque de Skynet
    ataque_skynet = "Turno enemigo"
    while ataque_skynet != "Agua":
        fila_skynet = random.randint(0, tamaño_tablero - 1)
        columna_skynet = random.randint(0, tamaño_tablero - 1)

        # Bucle while para evitar que Skynet ataque dos veces el mismo sitio
        while (fila_skynet, columna_skynet) in coord_skynet:
            fila_skynet = random.randint(0, tamaño_tablero - 1)
            columna_skynet = random.randint(0, tamaño_tablero - 1)

        ataque_skynet = disparar((fila_skynet, columna_skynet), tablero_jugador)
        print(f"El enemigo ha atacado las coordenadas: ({fila_skynet}, {columna_skynet})")
        print(ataque_skynet)

        # Comprobación del número de barcos aliados que quedan
        barcos_jugador = np.count_nonzero(tablero_jugador == "O")

        # Si no quedan barcos aliados, has perdido
        if barcos_jugador == 0:
            print("Has perdido")
            break

    # Avance en un turno
    turno += 1

else:
    print("Fin de la partida, no hay ganador")
    if barcos_jugador > barcos_skynet:
        print("Pero le has hecho más daño que él a tí")
    else:
        print("Y encima has perdido más barcos que el enemigo")
