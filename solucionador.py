#!/usr/bin/python
# -*- coding: utf-8 -*-

# ~ Trabajo Practico Final Parte en Python - Ezequiel Elías Sacchi

# ~ Breve información extra
    # ~  Usé de Python3
    # ~  La primer dimensión del laberinto, representado como una Matriz, se entiende como filas, mientras que la segunda dimensión se entiende como columnas. 
    # ~  Donde Fila(i) x Columna (j) es una ubicación individual de alguna de las estructuras(Obstaculo, Salida, Camino) en el laberinto. 
    # ~  Se espera que el archivo con el laberinto esté en la misma carpeta que éste código fuente.
    # ~  El código fue hecho en Linux Ubuntu 18.04.1 LTS'.
    # ~  Con el fin de correr el test en Linux(Ubuntu), desde la terminar en la carpeta donde se encuentra este archivo usar: python3 -m pytest -s EzequielEliasSacchi_Parte2_TPFinal.py
    # ~  De no contar con pytest instalado, desde la terminar correr los siguientes códigos:
    # ~  1) pip install -U pytest  // -> pip es una herramienta que instala paquetes de python y nos permite instalar el framkework pytest
    # ~  2) pip3 install pytest // instala pytest respectivo a python3
    # ~  En caso de que se utilice el mismo editor - Geany -, puede que se requiera que en Constuir/Build, Configurar Comandos/Set Commands en la Sección Execute/Ejecutar haya que aclarar el uso de python3
    # ~  Chauuu <1+2

# ~ Modulos
from random import *

# ~ Constantes "simbólicas" (python no tiene constantes reales) - no se modifica su valor a lo largo del programa
# ~ Nota: Algunos valores de éstas se repiten, más no su nomenclatura. Ésto es con la intención de añadir legibilidad al código.
FilasMax = 15
ColumnasMax = 15
TamanioFormacionMin = 2 # La fomacion u orden de una matriz pueden ser columnas y filas.
Abajo = 1
Arriba = -1
Adelante = 1
Atras = -1
NoHay = 0
Inicio = 0
Bajar = 'Abajo'
Subir = 'Arriba'
Delante = 'Adelante'
Detras  = 'Atras'
Obstaculo = '1'
Salida = '2'

# ~ Funciones
def CorregirArchivo(NombreDelArchivo):
    """
    CorregirArchivo(NombreDelArchivo): str -> str
    Toma una Cadena que representa el nombre del Archivo
    Si la cadena tiene la extension .txt, la retorna tal cual está. Caso contrario le agrega la extensión y la retorna.
    """
    
    if '.txt' not in NombreDelArchivo:
        NombreDelArchivo = NombreDelArchivo + '.txt'
        
    return NombreDelArchivo

def test_CorregirArchivo():
    
    assert CorregirArchivo('Hola') == 'Hola.txt'
    assert CorregirArchivo('Hola.txt') == 'Hola.txt'

def FormatoDeLaberintoCorrecto(MatrizLaberinto, CantidadFilas, CantidadColumnas):
    """
    FormatoDeLaberintoCorrecto(ArchivoLaberinto): Str -> Boolean
    Toma una cadena que representa el laberinto
    Verifica que:
        1_ El laberinto NO sea una carácter vacío ya sea por a) El Archivo contenía sólo saltos de línea o  b) El Archivo contenía un carácter vacío
        2_ Todos sus caracteres sean '1', '2', o '0'
        3_ Ni sus Filas o Columnas discrepen en tamaño
    Donde se den los casos anteriores retorna True, caso contrario False
    """
    
    Verificacion = True
    Estructuras = list('012')
    Fila = 0
    Columna = 0
    ExisteSalida = False
    while Verificacion and Fila < CantidadFilas:
        Verificacion = len(MatrizLaberinto[Fila]) == CantidadColumnas
        while Columna < CantidadColumnas and Verificacion:
            Estructura = MatrizLaberinto[Fila][Columna]
            Verificacion = Estructura in Estructuras
            if not ExisteSalida:
                ExisteSalida = Estructura == '2'
            Columna += 1
        Columna = 0
        Fila += 1
    Verificacion = ExisteSalida
    
    return Verificacion

def test_FormatoDeLaberintoCorrecto():
    
    assert FormatoDeLaberintoCorrecto([['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                                       ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                       ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0'], 
                                       ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                       ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                       ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                       ['0', '0', '0', '0', '0', '0', '1', '2', '1', '1', '0']],
                                       7, 11) == True
    assert FormatoDeLaberintoCorrecto([['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                                       ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                       ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0'], 
                                       ['0', 'a', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                       ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                       ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                       ['0', '0', '0', '0', '0', '0', '1', '2', '1', '1', '0']],
                                       7, 11) == False
    assert FormatoDeLaberintoCorrecto([['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                                       ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                       ['0', '0', '0', ' ', '0', '0', '0', '0', '0', '1', '0'], 
                                       ['0', 'a', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                       ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                       ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                       ['0', '0', '0', '0', '0', '0', '1', '2', '1', '1', '0']],
                                       7, 11) == False
    assert FormatoDeLaberintoCorrecto([['0', '2'],
                                       ['1', '1'],
                                       [' ', ' ']],
                                       2, 3) == False
    assert FormatoDeLaberintoCorrecto([['0', '0'],
                                       ['1', '1']],
                                       2, 2) == False

def ImprimirLaberinto(Laberinto):
    """
    ImprimirLab(Laberinto): [[int]] -> None
    Toma una lista de lista de enteros e imprime cada elemento de las listas interiores en una linea, por cada lista interior de modo tal de tener un laberinto con la forma de una matriz
    No tiene retorno
    No tiene tests por lo anterior
    """
    
    for Fila in Laberinto:
        print(('').join(Fila))

def DeterminarMovimientos(UbicacionSiguienteAVerificar, LimitesAVerificar, ValorDeFilaEnLaberintoAVerificar,
                         ValorDeColumnaEnLaberintoAVerificar, LaberintoDondeVerificar, MovimientoARealizar, 
                         ListadoDeMovimientosPosiblesASeguir, CaminosRecorridoActualmente, CaminosRecorridosAnteriormente):
    """
    DeterminarMovimiento(UbicacionSiguienteAVerificar, LimitesAVerificar, ValorDeFilaEnLaberintoAVerificar,
                         ValorDeColumnaEnLaberintoAVerificar, LaberintoDondeVerificar, MovimientoARealizar, 
                         ListadoDeMovimientosPosiblesASeguir, CaminosRecorridoActualmente, CaminosRecorridosAnteriormente):
    int, int, int, int, [[char]], str, [str], [[int,int]], [[int,int]] -> None
    Toma cuatro enteros que representan en el siguiente orden:
        1) Una posicion adyacente a la actual, 
        2) El limite de Fila o Columna que tiene el laberinto
        3) El indice en Filas del laberinto a corroborar su valor (que puede ser igual al primer punto)
        4) El indice en Columnas del laberinto a corroborar su valor (que puede ser igual al primer punto)
        nota: inevitablemente alguno de los indices toma el valor de la posicion adyacente a la actual, que es lo que buscamos verificar.
    Una lista de listas de caracteres que representa el laberinto, MovimientoARealizar que representa la Direccion a tomar de darse las condiciones posteriormente mencionadas,
    Una Lista de cadenas que contiene estos movimientos a realizar, y dos listas de listas de dos campos enteros que representan los caminos que ya hemos recorrido en algun punto.
    Determina entonces si la posición siguiente cumple con que:
        1) No se sale de los límites del laberinto
        2) No es un obstáculo
        3) No fue ya recorrida en el trayecto actual
        4) No fue anteriormente determinada como una ubicación donde no encontramos dirección siguiente para recorrer
    de darse lo anterior, agrega a la ListadoDeMovimientosPosiblesASeguir el MovimientoARealizar declarado.
    No tiene retorno
    Por lo anterior no tiene tests
    """
    
    if 0 <= UbicacionSiguienteAVerificar and UbicacionSiguienteAVerificar < LimitesAVerificar \
       and LaberintoDondeVerificar[ValorDeFilaEnLaberintoAVerificar][ValorDeColumnaEnLaberintoAVerificar] !=  Obstaculo \
       and [ValorDeFilaEnLaberintoAVerificar, ValorDeColumnaEnLaberintoAVerificar] not in CaminosRecorridoActualmente \
       and [ValorDeFilaEnLaberintoAVerificar, ValorDeColumnaEnLaberintoAVerificar] not in CaminosRecorridosAnteriormente:
           ListadoDeMovimientosPosiblesASeguir.append(MovimientoARealizar)

def DeterminarDireccion(Laberinto, UbicacionActual, CantidadDeFilas, CantidadDeColumnas, CaminosRecorridoActualmente, CaminosRecorridosAnteriormente):
    """
    DeterminarDireccion(Laberinto, UbicacionActual, CantidadDeFilas, CantidadDeColumnas, CaminoRecorrido, CaminosRecordados): [[str]], [int, int], int, int, [[int, int]], [[int, int]] -> str
    Toma una lista de listas de carácteres como laberinto, una lista de dos campos enteros como la ubicacion actual en el laberinto, dos enteros que representan el numero de filas y columnas que tiene el laberinto
    y dos listas de listas de dos campos enteros que representan respectivamente:
        1) el camino recorrido actualmente (que son las ubicaciones recorridas desde la entrada)
        2) y caminos recorridos anteriormente (que son aquellas reconocidas de algun otro trayecto anterior, es decir, la ultima ubicacion en recorridos actuales
           donde no se halló dirección alguna y por lo tanto volvimos a la entrada)
    y por cada movimiento determinado posible, elige uno al azar como Direccion a seguir en el laberinto. De no haber movimientos posibles, retorna NoHay como Direccion.
        
    Finalmente elegira una dirección al azar a seguir de las posibles la retorna. Caso contraro retornara que NoHay direcciones.
    """
    
    FilaActual = UbicacionActual[0]
    ColumnaActual = UbicacionActual[1]
    
    MovimientosPosibles = []
    
    # ~ La invocacion debajo de cada invocacion corroboran que podamos, desde la ubicacion que nos encontremos en el laberinto en el momento, si: 
    # ~ podemos ir para arriba
    DeterminarMovimientos(FilaActual + Arriba, CantidadDeFilas, FilaActual + Arriba, ColumnaActual, Laberinto, Subir, MovimientosPosibles, CaminosRecorridoActualmente, CaminosRecorridosAnteriormente)
    # ~ podemos ir para abajo
    DeterminarMovimientos(FilaActual + Abajo, CantidadDeFilas, FilaActual + Abajo, ColumnaActual, Laberinto, Bajar, MovimientosPosibles, CaminosRecorridoActualmente, CaminosRecorridosAnteriormente)
    
    # ~ podemos ir para la derecha(adelante)
    DeterminarMovimientos(ColumnaActual + Adelante, CantidadDeColumnas, FilaActual, ColumnaActual + Adelante, Laberinto, Delante, MovimientosPosibles, CaminosRecorridoActualmente, CaminosRecorridosAnteriormente)
    # ~ podemos ir para la izquierda(atras)
    DeterminarMovimientos(ColumnaActual + Atras, CantidadDeColumnas, FilaActual, ColumnaActual + Atras, Laberinto, Detras, MovimientosPosibles, CaminosRecorridoActualmente, CaminosRecorridosAnteriormente)
   
    CantidadDeDirecciones = len(MovimientosPosibles)
    Direccion = MovimientosPosibles[randrange(CantidadDeDirecciones)] if CantidadDeDirecciones != NoHay else NoHay 
    
    return Direccion
    
def test_DeterminarDireccion():
                                #Esta Lista de Listas es el laberinto
    assert DeterminarDireccion([['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                                ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0'], 
                                ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                ['0', '0', '0', '0', '0', '0', '1', '2', '1', '1', '0']], 
                                [0,0], 7, 11, [], [[0,1]]) == Bajar
    assert DeterminarDireccion([['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                                ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0'], 
                                ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                ['0', '0', '0', '0', '0', '0', '1', '2', '1', '1', '0']], 
                                [0,0], 7, 11, [], [[1,0],[0,1]]) == NoHay
    assert DeterminarDireccion([['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                                ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                                ['0', '1', '1', '1', '1', '0', '1', '1', '1', '0', '0'], 
                                ['0', '1', '1', '1', '1', '0', '1', '1', '1', '0', '0'], 
                                ['0', '1', '1', '1', '1', '0', '1', '2', '1', '0', '0'], 
                                ['0', '0', '0', '0', '0', '0', '1', '1', '1', '0', '0']], 
                                [6,10], 7, 11, [[6, 9]], []) == Subir
    assert DeterminarDireccion([['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                                ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0'], 
                                ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                ['0', '0', '0', '0', '0', '0', '1', '2', '1', '1', '0']], 
                                [6,5], 7, 11, [], [[0,1]]) == Detras
    assert DeterminarDireccion([['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                                ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0'], 
                                ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                                ['0', '0', '0', '0', '0', '0', '1', '2', '1', '1', '0']], 
                                [2, 4], 7, 11, [], [[2,3]]) == Delante
    
def BuscarSalida(Laberinto, CantidadDeFilas, CantidadDeColumnas):
    """
    BuscarSalida(Laberinto): [[str]], int, int -> [(int,int)]
    Toma una lista de listas de un campo con un carácter que representa el laberinto y dos enteros que representan las cantidad de filas y columnas en dicho orden
    Se ubica en la Entrada ([0,0]) y:
        a_ si es un obstáculo determina que no hay salida
        b_ si es la salida misma lo menciona, concluyendo el programa
        c_ determina la dirección siguiente a tomar desde ahí, descartando aquellas que estan obstaculizadas, recorridas actualmente o anteriormente
           c_1) donde la determinación sea 'NoHay': Reinicializa la UbicacionActual a Entrada, repitiendo el proceso anterior hasta que:
                c_1_i) El obstáculo anteriormente recorrido sea la misma Entrada, lo que significa que no hay salida
                c_1_ii) Encuentra la salida
                Por lo que Ambos terminos anteriores son la condicion de cierre del ciclo de búsqueda.
    Finalmente retorna la lista de las ubicaciones recorridas actualmente DESDE el punto de partida (Entrada) HASTA:
    i) La ubicación de Salida
    ii) La misma Entrada al no haber Salida, es decir, no hubo recorrido hasta la salida por que no existe.
    nota: en Ambos casos es el misma variable con el mismo tipo de retorno
    """
    
    Fila = Inicio
    Columna = Inicio
    CaminosRecorridosActualmente = []
    CaminosRecorridosAnteriormente = [] # Son aquellas ultimas ubicaciones de los CaminosLibresRecorridosActual donde DeterminarDireccion(.. , ..) arrojo 'NoHay'
    Entrada = [Inicio,Inicio]
    EstructuraEnEntrada = Laberinto[Entrada[0]][Entrada[1]]
    HaySalida = EstructuraEnEntrada != Obstaculo
    SalidaEncontrada = EstructuraEnEntrada == Salida
    
    if SalidaEncontrada:
        print('\nLa entrada es la misma Salida.\n')
    if not HaySalida:
        print('\nNo se puede acceder al Laberinto ya que la entrada esta obstaculizada.\n')
    while not SalidaEncontrada and HaySalida:
        UbicacionActual = [Fila,Columna]
        CaminosRecorridosActualmente.append(UbicacionActual)
        FilaUbicacionActual = UbicacionActual[0]
        ColumnaUbicacionActual = UbicacionActual[1]
        
        EstructuraEnUbicacionActual = Laberinto[FilaUbicacionActual][ColumnaUbicacionActual]
        SalidaEncontrada = EstructuraEnUbicacionActual == Salida
        
        Direccion = DeterminarDireccion(Laberinto, UbicacionActual, CantidadDeFilas, CantidadDeColumnas, CaminosRecorridosActualmente, CaminosRecorridosAnteriormente)
        Fila += Abajo if Direccion == Bajar else Arriba if Direccion == Subir else NoHay
        Columna += Adelante if Direccion == Delante else Atras if Direccion == Detras else NoHay

        if NoHay == Direccion and SalidaEncontrada != True:
            Fila = Inicio
            Columna = Inicio
            
            if Entrada in CaminosRecorridosAnteriormente:                
                HaySalida = False
                print('\nNo hay recorrido con el cual se pueda llegar a la Salida del laberinto.\n')
                
            else:                
                CaminosRecorridosAnteriormente.append(UbicacionActual)
                CaminosRecorridosActualmente = []
                
        elif SalidaEncontrada:            
            print('\nLa salida al laberinto es: \n\n' + ('\n').join([str(Ubicacion) for Ubicacion in CaminosRecorridosActualmente]))
            MostrarLaberintoRecorrido(Laberinto, CaminosRecorridosActualmente, CantidadDeFilas, CantidadDeColumnas)
    
    return CaminosRecorridosActualmente

def test_BuscarSalida():
    """
    Nota: El test de esta funcion es valido solo para: 
        - TODOS los casos en que el laberinto no tenga salida
        - Los casos en que el laberinto tenga un solo recorrido posible (de pasos únicos) para llegar a la SALIDA
    """                   
                         #La la lista de listas de caracteres debajo es el laberinto
                         #En el test debajo la Entrada del Laberinto es un Obstáculo
    assert BuscarSalida([['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '0', '0', '0', '0', '0', '1', '2', '1', '1', '0']]
                         , 7, 11) == []
                         #En el test debajo la Entrada del Laberinto es la Salida
    assert BuscarSalida([['2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '0', '0', '0', '0', '0', '1', '2', '1', '1', '0']]
                         , 7, 11) == []
                         #En el test debajo la Entrada no tiene alguna direccion posible por la cual ir
    assert BuscarSalida([['0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                         ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '0', '0', '0', '0', '0', '1', '2', '1', '1', '0']]
                         , 7, 11) == [[0, 0]]
                         #En el test debajo la Salida esta completamente rodeada de obstáculos y no se puede acceder a ella desde el laberinto
    assert BuscarSalida([['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '0', '0', '0', '0', '0', '1', '2', '1', '1', '0']]
                         , 7, 11) == [[0, 0]]
                         #En el test debajo la Salida esta completamente rodeada de obstáculos y hay camino libre alrededor de éstos
    assert BuscarSalida([['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
                         ['0', '1', '1', '1', '1', '0', '1', '1', '1', '0', '0'], 
                         ['0', '1', '1', '1', '1', '0', '1', '2', '1', '0', '0'], 
                         ['0', '1', '1', '1', '1', '0', '1', '1', '1', '0', '0'], 
                         ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']]
                         , 7, 11) == [[0, 0]]
                         #En el test debajo se puede llegar a la Salida
    assert BuscarSalida([['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],  
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0'], 
                         ['0', '0', '0', '0', '0', '0', '0', '2', '1', '1', '0']]
                         , 7, 11) == [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7]]

def MostrarLaberintoRecorrido(Laberinto, Recorrido, NumeroDeFilas, NumeroDeColumnas):
    """
    MostrarLaberintoRecorrido(Laberinto, Recorrido, NumeroDeFilas, NumeroDeColumnas): [[char]], [[int,int]], int, int -> None
    Toma Una lista de listas de cadenas como el Laberinto, Una lista de listas de dos elementos neteros que definen el recorrido hasta la salida (si la hay, si no la hay marca la posicion de inicio), y dos enteros que representan los valores de la matriz dada como laberinto
    Reemplaza el valor de todas las ubicaciones en el laberinto que se hallen en la lista de Recorrido por un '+' y posteriormente imprime el laberinto resuelto
    No tiene retorno
    Por lo anterior, no tiene test
    """
    
    for Ubicacion in Recorrido[0 : len(Recorrido) - 1]:
        Laberinto[Ubicacion[0]][Ubicacion[1]] = '+'
        
    print('\nEL laberinto recorrido es: \n')
    
    ImprimirLaberinto(Laberinto)

def ResolverLaberinto():
    """
    ResolverLaberinto(): None -> None
    Pide como ingreso una cadena que representa el nombre del archivo guardado en la carpeta donde se halla este mismo código fuente.
    Abre dicho archivo para determinar posteriormente si:
        - Es un laberinto válido, donde  lo sea:
            - Determina su tamaño en filas y columnas.
            - Crear la matriz que representa el laberinto como estructura recorrible.
            - Buscar su resolucion e imprimirla.
          Donde no:
            - Imprime los mensajes de error correspondientes.
    No tiene retorno
    No tiene casos de test  por lo anterior
    """
    
    print('Trabajo Práctico Final Parte en Python - Ezequiel Elías Sacchi // Resolucion del Laberinto\n')
    
    NombreArchivoLaberinto = CorregirArchivo(input("Ingresa el Nombre del Archivo con el Laberinto\n"))
    try:
        Laberinto = open(NombreArchivoLaberinto, "r")
    except IOError:
        print("\nEl Archivo no existe o lo escribiste mal.\n")
    else:
        MatrizLaberinto = [list(Fila.replace('\n', '')) for Fila in Laberinto if Fila != '\n']
        Laberinto.close()
        NumeroDeFilas = len(MatrizLaberinto)
        if TamanioFormacionMin <= NumeroDeFilas and NumeroDeFilas <= FilasMax:
            NumeroDeColumnas = len(MatrizLaberinto[0])
            if FormatoDeLaberintoCorrecto(MatrizLaberinto, NumeroDeFilas, NumeroDeColumnas) and TamanioFormacionMin <= NumeroDeColumnas and NumeroDeColumnas <=  ColumnasMax:
                print("\nEl Número De Columnas es: " + str(NumeroDeColumnas) + "\n" + "\nEl Número De Filas es: " + str(NumeroDeFilas) + "\n\nEl laberinto a Resolver es el siguiente:\n\n" )
                
                ImprimirLaberinto(MatrizLaberinto)
                BuscarSalida(MatrizLaberinto, NumeroDeFilas, NumeroDeColumnas)
                
            else:
                print("\nOcurrió alguno de éstos errores:\n*) Alguno de los caracteres no son correctos para el formato interno de las estructuras del laberinto\n*) Se excede el máximo de Columnas\n*) Hay disparidad en el tamaño de las Filas o Columnas")
        else:
            print("\nOcurrió alguno de estos errores:\n*) El laberinto es de puros saltos de línea\n*) Es sólo es un caracter vacío o excede el máximo de Filas\n*) No satisface el tamaño mínimo del laberinto")

# ~ Invocacion
ResolverLaberinto()
