import numpy as np
import random


def crear_tablero(tamaño: int = 10) -> np.ndarray:
    """
    Genera un tablero mediante numpy de dimensiones tamaño x tamaño relleno con "_"

    Args:
        tamaño (int): El tamaño del tablero

    Returns:
        numpy.ndarray

    Raises:
        ValueError

    :Example
        >>> crear_tablero(3)
        [['_' '_' '_']
        ['_' '_' '_']
        ['_' '_' '_']]
    """
    if not isinstance(tamaño, int):
        raise ValueError("tamaño debe ser un número entero")

    tablero = np.full((tamaño,tamaño), "_")
    return tablero


def colocar_barco(barco: list[tuple], tablero: np.ndarray) -> np.ndarray:
    """
    Coloca 'O' en el tablero sobre las posiciones indicadas en barco

    Args:
        barco (list[tuple]): Coordenadas del barco a colocar proporcionadas como una lista de tuplas,
        donde cada tupla es una posición del tablero
        tablero (np.ndarray): Tablero donde se va a colocar el barco

    Raises:
        IndexError: Indica si ya hay un barco en esa coordenada
        IndexError: Avisa si la coordenada indicada está fuera del tablero

    Returns:
        np.ndarray: Tablero con el barco colocado
    """
    try:
        for posicion in barco:
            if tablero[posicion] == "O":
                raise IndexError("Ya hay un barco en esa posición")
    except IndexError:
        raise IndexError("La posición del barco está fuera del tablero")

    for posicion in barco:
        tablero[posicion] = "O"


def disparar(casilla: tuple, tablero: np.ndarray) -> np.ndarray:
    """
    Dispara a una posición del tablero para intentar hundir el barco

    Args:
        casilla (tuple): Coordenadas a las que se dispara
        tablero (np.ndarray): Tablero de juego

    Raises:
        IndexError: Avisa si la coordenada indicada está fuera del tablero

    Returns:
        np.ndarray: Tablero modificado con el disparo. "X" si se ha acertado sobre un barco, "A" si se ha fallado
    """

    try:
        if tablero[casilla] == "O":
            tablero[casilla] = "X"
            return "Tocado"
        else:
            tablero[casilla] = "A"
            return "Agua"
    except IndexError:
        raise IndexError("La posición de disparo está fuera del tablero")


def crear_barco(eslora: int, tamaño_tablero: int = 10) -> list[tuple]:
    """
    Crea una barco de tamaño eslora para un tablero del tamaño indicado,
    devolviendo las coordenadas que lo componen

    Args:
        eslora (int): Tamaño del barco
        tamaño_tablero (int): Tamaño del tablero de juego, por defecto 10

    Returns:
        list[tuple]: Lista con las coordenadas que componen el barco

    Example:
        >>> crear_barco(3)
        [(1, 6), (1, 5), (1, 4)]
    """

    barco = []
    direccion = random.choice(["horizontal", "vertical"])

    # si la orientación es horizontal
    if direccion == "horizontal":
        derecha = random.choice([True, False])  # Colocación del barco hacia izq o dcha desde la posición inicial
        inicio_fila = random.randint(0, tamaño_tablero - 1) # La posición fila no va a variar
        if derecha: # Se suma o resta el tamaño de eslora para asegurar que el barco queda dentro del rango del tablero
            inicio_columna = random.randint(0, tamaño_tablero - eslora)
            for i in range(eslora):
                barco.append((inicio_fila, inicio_columna + i))
        else:
            inicio_columna = random.randint(0 + eslora, tamaño_tablero - 1)
            for i in range(eslora):
                barco.append((inicio_fila, inicio_columna - i))

    # La orientación es vertical
    else:
        arriba = random.choice([True, False])   # Colocación del barco hacia arriba o abajo desde la posición inicial
        inicio_columna = random.randint(0, tamaño_tablero - 1)  # La posición columna no va a variar
        if arriba:
            inicio_fila = random.randint(0 + eslora, tamaño_tablero - 1)
            for i in range(eslora):
                barco.append((inicio_fila - i, inicio_columna))
        else:
            inicio_fila = random.randint(0, tamaño_tablero - eslora)
            for i in range(eslora):
                barco.append((inicio_fila + i, inicio_columna))

    return barco


def colocar_barcos(tablero: np.ndarray, lista_esloras: list[int] = [4, 3, 3, 2, 2, 2]) -> np.ndarray:
    """
    Se apoya de la función crear_barco para generar y ubicar tantos barcos del tamaño
    indicado en el tablero

    Args:
        tablero (np.ndarray): Tablero de juego
        lista_esloras (list[int], optional): Lista con las esloras de los barcos a colocar. Defaults to [4, 3, 3, 2, 2, 2].

    Returns:
        np.ndarray: Tablero de juego con los barcos colocados
    """

    coord_ocupadas = []     # Lista de coordenadas ya ocupadas
    for i in lista_esloras:
        barco = crear_barco(i)
        # Comprobación de las coordenadas del barco creado frente a las de barcos anteriores
        # para evitar ocupar el mismo espacio dos veces
        while any(coord in coord_ocupadas for coord in barco):
            barco = crear_barco(i)
        else:   # Si el espacio está libre, se guardan las coordenadas y se coloca el barco
            for coord in barco:
                coord_ocupadas.append(coord)
            colocar_barco(barco, tablero)

    return tablero
