// Trabajo Practico Final Parte en C - Ezequiel Elias Sacchi

/*Breve Informacion Extra
 * Holi <1+2
 * Se asume que para considerarse como laberinto, la matriz que lo representa debe ser al menos de 2 x 2, igualmente su tamanio maximo no puede exceder 15 x 15
 * La primer dimension del laberinto se entiende como sus filas, mientras que la segunda dimension se entiende como sus columnas Donde Fila(i) x Columna (j) es una ubicacion individual en el laberinto
 * La cantidad maxima de obstaculos es 20
 * La primer linea del Archivo representa el tamanio del laberinto, donde el primer numero sera la cantidad de filas y el segundo la cantidad de columnas
 * La segunda linea del archivo representa la ubicacion de salida, donde el primer numero ubica la salida en tal fila, y el segundo la ubica en tal columna
 * Tener en cuenta el formato del contenido dentro del Archivo de Ejemplo dado, que tenga caracteres impide que funcione el programa.
 * El resto de filas representan las ubicaciones de los obstaculos, el primer numero en la fila y el segundo en la columna.
 */

//Librerias

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

//Constantes simbolicas

#define CaminoLibre 0
#define Obstaculo 1
#define Objetivo 2
#define CaracteresMAX 99
#define TamanioMAXLaberinto 15
#define TamanioMINLaberinto 2
#define EspacioNecesarioParaUbicarSalida 1
#define TamanioDelPar 2
#define ErrorDeTamanioLaberinto -9
#define ErrorDePosDeSalida -3
#define ErrorDeArchivo -6
#define ObstaculosMAX 20
#define False 0
#define True 1
#define TodoBien 0

//prototipos

//funciones
void ImprimirDatos(int ArrayObstaculos[][TamanioDelPar], int TamanioArray, int ArrayConPosSalida[], int ArrayConTamanioLaberinto[]);
int CorroborarTamanioLaberinto(int TamanioLaberinto[]);
int CorroborarSalida(int PosSalida[], int TamanioLaberinto[]);
int CorroborarObstaculo(int ArrayConPosDeObstaculos[][TamanioDelPar], int UbicacionACorroborar, int TamanioLaberinto[]);
int UbicacionRepetida(int ListaConObstaculos[][TamanioDelPar], int TamanioYIndiceARevisar, int UbicacionDeSalida[]);
int AbrirArchivoColocarDatos(int TamanioLaberinto[], int PosDeSalida[], int ListaDeObstaculos[][TamanioDelPar]);
int VerificaUbicacionObstaculo(int UbicacionEnLaberintoA, int UbicacionEnLaberintoB, int ArrayConObstaculos[][TamanioDelPar], int TamanioArrayObstaculos);
void GenerarLaberintoEnArchivo(int ArrayConLaberinto[][TamanioMAXLaberinto], int ArrayConTamanioDeLaberinto[]);
void ImprimirLab(int ArrayConLaberinto[][TamanioMAXLaberinto] , int TotalDeFilas, int TotalDeColumnas);
void CrearLaberinto(int ArrayConTamanio[], int ArrayConObstaculos[][TamanioDelPar], int TamanioArrayObstaculos, int ArrayConSalida[]);

//tests
void test_CorroborarTamanioLaberinto();
void test_CorroborarSalida();
void test_CorroborarObstaculo();
void test_UbicacionRepetida();
void test_VerificaUbicacionObstaculo();
void tests();

void ImprimirDatos(int ArrayObstaculos[][TamanioDelPar], int TamanioArray, int ArrayConPosSalida[], int ArrayConTamanioLaberinto[])
{
    /* ImprimirDatos(): int Array[][], int, int Array[], int Array[] -> void
     * Toma un array bidimensional de tipo enteros donde sus elementos representan la pos de un obstaculo en el laberinto, un entero como su tamanio.
     * y dos array unidimensioanles de enteros, donde sus dos elementos son los campos del par que representa la pos de salida(objetivo) en el caso del primero, y en el caso del segundo, el tamanio del laberinto
     * Finalmente Imprime los elementos dentro de los Array tomado como entrada, como datos relevantes al Laberinto
     * No tiene retorno
     * Por lo anterior, no tiene Tests 
     */
     
    printf("\nEl Tamanio del Laberinto es: %d,%d\n", ArrayConTamanioLaberinto[0], ArrayConTamanioLaberinto[1]);
    printf("\nLa posicion de la Salida (Objetivo) es: %d,%d\n", ArrayConPosSalida[0], ArrayConPosSalida[1]);
    printf("\nLas posiciones de las paredes son:\n");
    for(int Indice = 0, NumPar = 0; Indice < TamanioArray;)
    {
        printf("%d", ArrayObstaculos[Indice][NumPar]);
        if (NumPar == 0)
        {
            NumPar++;
        }
        else
        {
            printf("\n");
            NumPar = 0;
            Indice++;
        }
        if (NumPar == 1)
        {
            printf(",");
        }
    }
}

int CorroborarTamanioLaberinto(int TamanioLaberinto[])
{
    /* CorroborarTamanioLaberinto(): int Array[]
     * Toma un arreglo unidimensional de dos elementos enteros que representan el valor de la matriz del laberinto
     * Revisa que el Tamanio del Laberinto no sea mayor a 15 o menor a 0
     * De corroborarse arroja 1, caso contrario arroja 0
     */
     
     return !(TamanioLaberinto[0] < TamanioMINLaberinto || TamanioLaberinto[0] > TamanioMAXLaberinto || TamanioLaberinto[1] < TamanioMINLaberinto || TamanioLaberinto[1] > TamanioMAXLaberinto);
}

void test_CorroborarTamanioLaberinto()
{
    int TamanioTest[TamanioDelPar] = {4,5}, TamanioTest1[TamanioDelPar] = {-1, 20}, TamanioTest2[TamanioDelPar] = {1, 19}, TamanioTest3[TamanioDelPar] = {17, 2}, TamanioTest4[TamanioDelPar] = {2.2};
    assert(CorroborarTamanioLaberinto(TamanioTest) == True);
    assert(CorroborarTamanioLaberinto(TamanioTest1) == False);
    assert(CorroborarTamanioLaberinto(TamanioTest2) == False);
    assert(CorroborarTamanioLaberinto(TamanioTest3) == False);
    assert(CorroborarTamanioLaberinto(TamanioTest4) == False);
}

int CorroborarSalida(int PosSalida[], int TamanioLaberinto[])
{
    /*CorroborarSalida(): int Array[], int Array[]
     * Toma dos arreglo unidimensiona de dos elementos enteros, el primero representa la posicion de salida (objetivo) en el laberinto y en el otro se halla los valores de la matriz para el laberinto
     * Revisa que el primer campo no sea menor a 0 o mayor al primer campo de la matriz, y lo mismo para el segundo campo.
     * De corroborarse arroja 1, caso contrario 0
     */
     
     return !(PosSalida[0] < 0 || PosSalida[0] >= TamanioLaberinto[0] || PosSalida[1] < 0 || PosSalida[1] >= TamanioLaberinto[1]);
}

void test_CorroborarSalida()
{
    int TamanioTest1[TamanioDelPar] = {9, 9},
        PosDeSalida[TamanioDelPar] = {3,1}, PosDeSalida1[TamanioDelPar] = {9, 9}, PosDeSalida2[TamanioDelPar] = {-2, 3};
    
    assert(CorroborarSalida(PosDeSalida, TamanioTest1) == 1);
    assert(CorroborarSalida(PosDeSalida1, TamanioTest1) == 0);
    assert(CorroborarSalida(PosDeSalida2, TamanioTest1) == 0);
}

int CorroborarObstaculo(int ArrayConPosDeObstaculos[][TamanioDelPar], int UbicacionACorroborar, int TamanioLaberinto[])
{
    /* CorroborarObstaculo(): int Array[][], int, int Array[]
     * Toma un entero como la ubicacion a corroborar. Dos array, uno bidimensional y otro unidimensional. El primero tiene en sus elementos el par que indicia la posicion de un obstaculo. El otro tiene en sus elementos ambos tamanios del laberinto. 
     * Revisa que el primer campo del par a verificar no sea menor a 0, ni sea igual o mayor al primer campo del par en TamanioLaberinto. Analogamente con el segundo campo.
     * Retorna True de corroborarse, caso contrario False
     */

    return !(ArrayConPosDeObstaculos[UbicacionACorroborar][0] < 0 || ArrayConPosDeObstaculos[UbicacionACorroborar][0] >= TamanioLaberinto[0] || 
            ArrayConPosDeObstaculos[UbicacionACorroborar][1] < 0 || ArrayConPosDeObstaculos[UbicacionACorroborar][1] >= TamanioLaberinto[1]);
}

void test_CorroborarObstaculo()
{
    int ListaDeObstaculos[5][2] = {{1,2}, {3,5}, {2,4}, {9,9}, {7,4}}, TamanioLaberinto[2] = {3, 5};
    assert(CorroborarObstaculo(ListaDeObstaculos, 1, TamanioLaberinto) == False);
    assert(CorroborarObstaculo(ListaDeObstaculos, 0, TamanioLaberinto) == True);
    assert(CorroborarObstaculo(ListaDeObstaculos, 2, TamanioLaberinto) == True);
    assert(CorroborarObstaculo(ListaDeObstaculos, 3, TamanioLaberinto) == False);
    assert(CorroborarObstaculo(ListaDeObstaculos, 4, TamanioLaberinto) == False);
}

int UbicacionRepetida(int ListaConObstaculos[][TamanioDelPar], int TamanioYIndiceARevisar, int UbicacionDeSalida[])
{
    /* UbicacionRepetida(): int array[][], int, int array[]
     * Toma una array bidimensional cuyos elementos representan la ubicacion de obstaculos en un laberinto formado por una matriz, un entero que  indica el tamanio total, a la vez que el indice del par a revisar y un array unidimensional con el par que representa la ubicacion de salida (objetivo)
     * Verifica que la ultima ubicacion (como par) en ListaConObstaculos sea igual a la UbicacionDeSalida, de darse cierto. Retorna True. 
     * Caso contrario, Verifica que la ultima ubicacion en ListaConObstaculos sea igual a alguna del resto en la lista donde se asigna Repetida True y es retornado.
     * De no darse nada de lo anterior, retorna Repetida como False d
     */
    
    int CampoDeParAVerificarA = ListaConObstaculos[TamanioYIndiceARevisar][0], CampoDeParAVerificarB = ListaConObstaculos[TamanioYIndiceARevisar][1],
        CampoDeSalidaA = UbicacionDeSalida[0], CampoDeSalidaB = UbicacionDeSalida[1],
        Repetida = CampoDeParAVerificarA == CampoDeSalidaA && CampoDeParAVerificarB == CampoDeSalidaB; // verifica que ningun obstaculo coincida en ubicacion con la de salida
    
    for (int IndiceDePar = 0, CampoDeParEnRestoDeListaA, CampoDeParEnRestoDeListaB; IndiceDePar  < TamanioYIndiceARevisar && Repetida != True; IndiceDePar++)
    {
        CampoDeParEnRestoDeListaA = ListaConObstaculos[IndiceDePar][0];
        CampoDeParEnRestoDeListaB = ListaConObstaculos[IndiceDePar][1];
        Repetida =  CampoDeParEnRestoDeListaA == CampoDeParAVerificarA && CampoDeParEnRestoDeListaB == CampoDeParAVerificarB;
    }
    
    return Repetida;
}

void test_UbicacionRepetida()
{
    
    int ListaTestObstaculos[3][TamanioDelPar] = {{1,2},{9,9}, {9,9}}, ListaTestObstaculos2[2][TamanioDelPar] = {{6,9},{3,1}}, ListaTestObstaculos3[1][TamanioDelPar] = {{1,1}},
        UbicacionSalida[2] = {1, 1};
    assert(UbicacionRepetida(ListaTestObstaculos, 2, UbicacionSalida) == True);
    assert(UbicacionRepetida(ListaTestObstaculos2, 1, UbicacionSalida) == False);
    assert(UbicacionRepetida(ListaTestObstaculos3, 0, UbicacionSalida) == True);
    }

int AbrirArchivoColocarDatos(int TamanioLaberinto[], int PosDeSalida[], int ListaDeObstaculos[][TamanioDelPar])
{   
    /* AbrirArchivoColocarDatos(): int Array[] , int Array[], int Array[][] -> void
     * Toma dos arreglos unidimentionales de tipo entero, el primero 
     * Pide el ingreso de una cadena como el nombre de un Archivo necesariamente con extension .txt, lo abre y coloca los datos hallados en este en el arreglo respectivo, es decir:
     * Los dos primeros datos se aniaden al ArrayDeObjetivo
     * El resto se aniade a ArrayDeParedes
     * No tiene retorno
     * No tiene casos de Test
     */
     
    char NombreDelArchivo[CaracteresMAX] = {};
    int Linea = 0, UbicacionEnLista = 0, CampoDelPar = 0, HayError = 0, AmbosPares, MAXObstaculosLaberinto, CalculoMaxObstaculos;
    scanf("%s", NombreDelArchivo);
    FILE *ArchivoConDatosLaberinto;
    ArchivoConDatosLaberinto = fopen(NombreDelArchivo, "r");
    if (ArchivoConDatosLaberinto == NULL)
    {
        printf("\nEl Archivo NO existe o lo has escrito erroneamente.");
        UbicacionEnLista = ErrorDeArchivo;
    }
    else
    {
        while(!feof(ArchivoConDatosLaberinto) && HayError == 0 && UbicacionEnLista != MAXObstaculosLaberinto)
        {
            if (Linea < 2)
            {
                fscanf(ArchivoConDatosLaberinto, "%d", &TamanioLaberinto[Linea]);
                AmbosPares = Linea == 1;
                if (AmbosPares)
                {
                    if (!CorroborarTamanioLaberinto(TamanioLaberinto))
                    {
                        HayError = ErrorDeTamanioLaberinto;
                        UbicacionEnLista = ErrorDeTamanioLaberinto;
                    }
                    //Teniendo en cuenta que la Salida existe siempre, para aquellos laberintos menores o iguales a 5x5, debe haber al menos un espacio que no sea un obstaculo.
                    CalculoMaxObstaculos = (TamanioLaberinto[0] * TamanioLaberinto[1]) - EspacioNecesarioParaUbicarSalida; 
                    MAXObstaculosLaberinto = CalculoMaxObstaculos < ObstaculosMAX ? CalculoMaxObstaculos : ObstaculosMAX;
                }
            }
            else if (Linea < 4)
            {
                fscanf(ArchivoConDatosLaberinto, "%d", &PosDeSalida[CampoDelPar]);
                CampoDelPar++;
                AmbosPares = CampoDelPar == 2;
                if (AmbosPares)
                {
                    if (!CorroborarSalida(PosDeSalida, TamanioLaberinto))
                    {
                        HayError = ErrorDePosDeSalida;
                        UbicacionEnLista = ErrorDePosDeSalida;
                    }
                    CampoDelPar = 0;
                }
            }
            else
            {
                fscanf(ArchivoConDatosLaberinto, "%d", &ListaDeObstaculos[UbicacionEnLista][CampoDelPar]);
                CampoDelPar++;
                AmbosPares = CampoDelPar == 2;
                
                if (AmbosPares)
                {
                    if (!CorroborarObstaculo(ListaDeObstaculos, UbicacionEnLista, TamanioLaberinto) || UbicacionRepetida(ListaDeObstaculos, UbicacionEnLista, PosDeSalida))
                    {
                        UbicacionEnLista--;
                    }
                    CampoDelPar = 0;
                    UbicacionEnLista++;
                }
            }
            Linea++;
        }
        
    }
    fclose(ArchivoConDatosLaberinto);
    return UbicacionEnLista;
}

int VerificaUbicacionObstaculo(int UbicacionEnLaberintoA, int UbicacionEnLaberintoB, int ArrayConObstaculos[][TamanioDelPar], int TamanioArrayObstaculos)
{
    /*VerificaUbicacionObstaculo(): int, int, int array[][], int
     * Toma dos enteros como una posicion en el laberinto, un arreglo de numeros enteros cuyos elementos representan una posicion  en el laberinto que debe ser ocupada por un obstaculo y un entero como el tamanio del arreglo
     * Revisa en todos los pares de la lista con obstaculos hasta dar con una coincidencia, de darse retorna True. Caso contrario retorna False.
     */
    
    int Verificada = False;
    
    for(int IndiceEnListaObstaculos = 0, CampoA = 0, CampoB = 1; IndiceEnListaObstaculos < TamanioArrayObstaculos && Verificada != True; IndiceEnListaObstaculos++)
    {
        Verificada = UbicacionEnLaberintoA == ArrayConObstaculos[IndiceEnListaObstaculos][CampoA] && UbicacionEnLaberintoB == ArrayConObstaculos[IndiceEnListaObstaculos][CampoB];
    }
    
    return Verificada;
    
}

void test_VerificaUbicacionObstaculo()
{
    int ArrayObstaculosTest[5][TamanioDelPar] = {{1,2},{5,7},{3,9},{2,2}};
    
    assert(VerificaUbicacionObstaculo(1, 2, ArrayObstaculosTest, 5) == True);
    assert(VerificaUbicacionObstaculo(3, 9, ArrayObstaculosTest, 5) == True);
    assert(VerificaUbicacionObstaculo(-3, 20, ArrayObstaculosTest, 5) == False);
    assert(VerificaUbicacionObstaculo(2, 1, ArrayObstaculosTest, 5) == False);
}

void GenerarLaberintoEnArchivo(int ArrayConLaberinto[][TamanioMAXLaberinto], int ArrayConTamanioDeLaberinto[])
{
    /*
     * GenerarLaberintoEnArchivo(): int Array[][], int Array[]
     * Toma un array bidimensional que representa el laberinto construido y un entero como su tamanio
     * Dada cada ubicacion determinada con el tamanoio de laberinto, 
     */
     
    int TamanioLabA = ArrayConTamanioDeLaberinto[0], TamanioLabB = ArrayConTamanioDeLaberinto[1];
    FILE *ArchivoLaberinto = fopen("Laberinto.txt", "w+");
    for(int IndiceLabA = 0; IndiceLabA < TamanioLabA; IndiceLabA++)
    {
        for(int IndiceLabB = 0; IndiceLabB < TamanioLabB; IndiceLabB++)
        {
            fprintf(ArchivoLaberinto, "%d", ArrayConLaberinto[IndiceLabA][IndiceLabB]); 
        }
        fprintf(ArchivoLaberinto, "%s", "\n");
    }
    
}

void ImprimirLab(int ArrayConLaberinto[][TamanioMAXLaberinto], int TotalDeFilas, int TotalDeColumnas)
{
    /* ImprimirLab(): int Array[][], int, int
     * Toma un array bidimensional con el laberinto, y dos enteros que representan filas y columnas
     * Imprime cada par bidimensional del arreglo como  una ubicacion en el laberinto, a cada fin de fila se le agrega un salto de linea
     * No tiene retorno
     * No tiene tests por lo anterior
     */
     
    printf("\nEl laberinto que se genero es el siguiente:\n");
    for(int NumeroDeFila = 0; NumeroDeFila < TotalDeFilas; NumeroDeFila++)
    {
        for(int NumeroDeColumna = 0; NumeroDeColumna < TotalDeColumnas; NumeroDeColumna++)
        {
            printf("%d", ArrayConLaberinto[NumeroDeFila][NumeroDeColumna]); 
        }
        printf("\n");
    }
}

void CrearLaberinto(int ArrayConTamanio[], int ArrayConObstaculos[][TamanioDelPar], int TamanioArrayObstaculos, int ArrayConSalida[])
{
    /*
     * CrearLaberinto(): int Array[], int Array[][], int, int Array[]
     * Toma dos array unidimensionales, el primero representa el tamanio del laberinto y El segundo la ubicacion de salida. Ademas de un array bidimensional con la ubicacion de los obstaculos y un entero como su tamanio
     * Crea Array Bidimensional que representa el laberinto de las medidas de entrada, y agrega obstaculos y la salida en la  ubicacion correspondiente hallada en los array de entrada
     * Rellena aquellas ubicaciones que no tengan obstaculos con una salida con Caminos Libres
     * No tiene retorno
     * Por lo enterior, no tiene tests
     */

    int CantidadFilasLaberinto = ArrayConTamanio[0], CantidadColumnasLaberinto = ArrayConTamanio[1], Laberinto[TamanioMAXLaberinto][TamanioMAXLaberinto] = {},
        UbicacionEnFilaDeSalida = ArrayConSalida[0], UbicacionEnColumnaDeSalida = ArrayConSalida[1];
    
    
    for (int NumeroDeFila = 0; NumeroDeFila < CantidadFilasLaberinto; NumeroDeFila++) //Aniade Caminos Libres y Obstaculos
    {
        for (int NumeroDeColumna = 0; NumeroDeColumna < CantidadColumnasLaberinto; NumeroDeColumna++)
        {
            if (VerificaUbicacionObstaculo(NumeroDeFila, NumeroDeColumna, ArrayConObstaculos, TamanioArrayObstaculos))
            {
                Laberinto[NumeroDeFila][NumeroDeColumna] = Obstaculo;
            }
            else
            {
                Laberinto[NumeroDeFila][NumeroDeColumna] = CaminoLibre;
            }
        }
    }
    
    Laberinto[UbicacionEnFilaDeSalida][UbicacionEnColumnaDeSalida] = Objetivo; // Aniade la Salida(Objetivo)
    ImprimirLab(Laberinto, CantidadFilasLaberinto, CantidadColumnasLaberinto);
    GenerarLaberintoEnArchivo(Laberinto, ArrayConTamanio);

}

void tests()
{
    test_CorroborarTamanioLaberinto();
    test_CorroborarSalida();
    test_CorroborarObstaculo();
    test_VerificaUbicacionObstaculo();
    test_UbicacionRepetida();
}

int main()
{
    tests();
    printf("Trabajo Final, parte en C\n\nIngresa el nombre del archivo con los datos para construir el laberinto:\n");
    
    int TamanioDelLaberinto[TamanioDelPar] = {},
        PosicionDeSalida[TamanioDelPar] = {},
        ListadoDeObstaculos[ObstaculosMAX][TamanioDelPar] = {},
        TamanioListadoDeObstaculos = AbrirArchivoColocarDatos(TamanioDelLaberinto, PosicionDeSalida, ListadoDeObstaculos);
    if (TamanioListadoDeObstaculos == ErrorDeTamanioLaberinto)
    {
        printf("\nEl tamanio obtenido del Archivo esta fuera de los rangos para construir el laberinto.\n");
        return ErrorDeTamanioLaberinto;
    }
    else if (TamanioListadoDeObstaculos == ErrorDePosDeSalida)
    {
        printf("\nLa posicion de la Salida (U objetivo) no coincide con alguna posible dentro del tamanio del laberinto.\n");
        return ErrorDePosDeSalida;
    }
    else if (TamanioListadoDeObstaculos != ErrorDeArchivo)
    {
        ImprimirDatos(ListadoDeObstaculos, TamanioListadoDeObstaculos, PosicionDeSalida,TamanioDelLaberinto);
        CrearLaberinto(TamanioDelLaberinto, ListadoDeObstaculos, TamanioListadoDeObstaculos, PosicionDeSalida);
    }
    
    return TodoBien;
}

