import time
from fractions import Fraction

import numpy as np

import ReadFile as rF

potentialCantidatos = []
indexCandidatos = []
indexPlantillas = {}
indexIdNodos = 0
LB = 0


# Imprimir el resultado
def printResult(elmts, resultado):
    for i, j in zip(range(1, numElementos + 1), elmts):
        print(str(int(resultado[i].__float__())) + ": " + str(j[3]))


# Recuperar el valor total
def getValue(ksChild):
    """

    :rtype: int
    """
    valKS = 0.0
    for i, j in zip(range(1, numElementos + 1), range(0, numElementos)):
        if ksChild[i] != Fraction(-1):
            valKS += ksChild[i].__float__() * elementos[j][1]
    return valKS


# Recuperar el valor total
def getWeight(ksChild):
    """

    :rtype: int
    """
    valKS = 0.0
    for i, j in zip(range(1, numElementos + 1), range(0, numElementos)):
        if ksChild[i] != Fraction(-1):
            valKS += ksChild[i].__float__() * elementos[j][0]
    return valKS


# Crear hijo, a partir de lo marcado
def createChild(ksChild):
    oldTime = time.time()
    indexPer = -1
    countKap = getWeight(ksChild)
    if countKap <= capacity:
        for indexEl in range(0, numElementos, 1):
            if (ksChild[indexEl + 1] == Fraction(-1)):
                if (countKap + elementos[indexEl][0] > capacity):
                    cp = int(capacity - countKap)
                    if (cp > 0):
                        el = int(elementos[indexEl][0])
                        ksChild[indexEl + 1] = Fraction(cp, el)
                        indexPer = indexEl + 1
                    else:
                        ksChild[indexEl + 1] = Fraction(0)
                else:
                    ksChild[indexEl + 1] = Fraction(1)
                countKap += elementos[indexEl][0]
        return ksChild, indexPer
    else:
        return None, None


def startBranchAndBound():
    oldTime = time.time()
    global elementos, indexCandidatos, indexPlantillas, indexIdNodos, LB
    elementos = [x + [0.0] + [j] for x, j in zip(elementos, range(1, len(elementos) + 1, 1))]
    # Calcular el ratio de volumen sobre el beneficio
    for i in elementos:
        i[2] = i[1] / i[0]  # Valor/Volumen
    # Ordenar los elementos de mayor a menor
    elementos.sort(key=lambda x: x[2], reverse=True)
    # Llenar el knapsack padre, el primer elemento es un Id para la rama
    fKnapSack = [0]
    fKnapSack.extend([Fraction(-1) for i in range(0, len(elementos), 1)])
    # LLenar el primer elementos con los datos mas prometedores
    fKnapSack, indexPer = createChild(fKnapSack)
    while (True):
        # Declarar los nuevos hijos que se van a crear
        ksChild1 = [indexCount + 1]
        ksChild2 = [indexCount + 2]
        indexCount += 2;
        # Buscar las preferencias del padre para juntarlas con las del los hijos\
        try:
            prefFather = indexPlantillas[fKnapSack[0]]
        except:
            # Cuando no encuentra preferencias del padre
            prefFather = []
        # Almacenar las preferencias de los hijos
        indexPlantillas[ksChild1[0]] = [[indexPer, Fraction(0)]] + prefFather
        indexPlantillas[ksChild2[0]] = [[indexPer, Fraction(1)]] + prefFather
        # Generar los dos hijos de nuevos, a partir del indice que va permanente
        ksChild1.extend([Fraction(-1) for i in range(0, len(elementos), 1)])
        # Recorrer las preferencias el primer hijo
        for i in indexPlantillas[ksChild1[0]]:
            ksChild1[i[0]] = i[1]
        ksChild2.extend([Fraction(-1) for i in range(0, len(elementos), 1)])
        # Recorrer las preferencias el segundo hijo
        for i in indexPlantillas[ksChild2[0]]:
            ksChild2[i[0]] = i[1]
        # LLenar los hijos nuevos a partir del creado anteriormente, con las preferencias ya indicadas
        ksChild1, indexPer1 = createChild(ksChild1)
        ksChild2, indexPer2 = createChild(ksChild2)

        # Guardar los y su valor para encontrar el mayor
        if (ksChild1 is not None and indexPer1 is not None):
            # if (ksChild1 not in potentialCantidatos):
            potentialCantidatos.append(ksChild1)
            vaKSChild1 = getValue(ksChild1)
            indexCandidatos.append([vaKSChild1, indexPer1])
            if indexPer1 == -1:
                if vaKSChild1 > LB:
                    LB = vaKSChild1
                    # else:
                    #     print("Rechazaod")
        if (ksChild2 is not None and indexPer2 is not None):
            # if (ksChild2 not in potentialCantidatos):
            potentialCantidatos.append(ksChild2)
            vaKSChild2 = getValue(ksChild2)
            indexCandidatos.append([vaKSChild2, indexPer2])
            if indexPer2 == -1:
                if vaKSChild2 > LB:
                    LB = vaKSChild2
                    # else:
                    #     print("Rechazaod")
        # Elegir el item con valor mas grande para realizar el branch
        itemMax = np.argmax(indexCandidatos, axis=0)[0]
        if (indexCandidatos[itemMax][1] != -1):
            # Seleccionamos el nuevo padre para la siguiente iteracion
            fKnapSack = potentialCantidatos[itemMax]
            indexPer = indexCandidatos[itemMax][1]
            # Comparar si el item elegido tiene el mismo valor entero que un candidato potencial
            if int(indexCandidatos[itemMax][0]) == LB:
                # Recuperar el maximo candidato
                maxCandidato = 0
                for i in range(0, len(indexCandidatos)):
                    if indexCandidatos[i][1] == -1:
                        if indexCandidatos[i][0] > indexCandidatos[maxCandidato][0]:
                            maxCandidato = i
                print ("Item mayor elegido")
                printResult(elementos, potentialCantidatos[maxCandidato])
                print "Valor: ",
                print getValue(potentialCantidatos[maxCandidato])
                break
            print("Item Elegido"),
            print(indexCandidatos[itemMax][0]),
            # print(potentialCantidatos[itemMax]),
            # print("item Elegido maximo")
            del (indexCandidatos[itemMax])
            del (potentialCantidatos[itemMax])
        else:
            printResult(elementos, potentialCantidatos[itemMax])
            print(indexCandidatos[itemMax][0])
            print("solucion maxima econtrada")
            break
        print ("\tTime: " + str(time.time() - oldTime))


elementos, capacity = rF.readTxtFile()
numElementos = len(elementos)
startBranchAndBound()
