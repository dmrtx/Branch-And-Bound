import time
from fractions import Fraction

import numpy as np

import ReadFile as rF

potentialCantidatos = []
itemCandidatos = []
indexCandidatos = []
# Almacena
indexPlantillas = {}
indexIdNodos = 0
LB = None
delMenores = True
indexX = []


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
            valKS += ksChild[i] * elementos[j][1]
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


def printSolution():
    valPC = 0
    pcMax = []
    for i in potentialCantidatos:
        if (i[1] > valPC):
            pcMax = i
            valPC = i[1]
    printResult(elementos, pcMax[0])
    print(valPC)
    print("solucion maxima econtrada")


def startBranchAndBound():
    oldTime = time.time()
    global elementos, indexCandidatos, indexPlantillas, indexIdNodos, LB, delMenores, indexX
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
        childKS1 = [indexCount + 1]
        childKS2 = [indexCount + 2]
        indexCount += 2;
        # Buscar las preferencias del padre para juntarlas con las del los hijos\
        try:
            prefFather = indexPlantillas[fKnapSack[0]]
        except:
            # Cuando no encuentra preferencias del padre
            prefFather = []
        # Almacenar las preferencias de los hijos
        indexPlantillas[childKS1[0]] = [[indexPer, Fraction(0)]] + prefFather
        indexPlantillas[childKS2[0]] = [[indexPer, Fraction(1)]] + prefFather
        # Generar los dos hijos de nuevos, a partir del indice que va permanente
        childKS1.extend([Fraction(-1) for i in range(0, len(elementos), 1)])
        # Recorrer las preferencias el primer hijo
        for i in indexPlantillas[childKS1[0]]:
            childKS1[i[0]] = i[1]
        childKS2.extend([Fraction(-1) for i in range(0, len(elementos), 1)])
        # Recorrer las preferencias el segundo hijo
        for i in indexPlantillas[childKS2[0]]:
            childKS2[i[0]] = i[1]
        # LLenar los hijos nuevos a partir del creado anteriormente, con las preferencias ya indicadas
        childKS1, indPerm1 = createChild(childKS1)
        childKS2, indPerm2 = createChild(childKS2)

        # Guardar los y su valor para encontrar el mayor
        if (childKS1 is not None and indPerm1 is not None):
            valueChild1 = getValue(childKS1)
            if indPerm1 == -1 and (valueChild1 > LB or LB is None):
                potentialCantidatos.insert(0, [childKS1, valueChild1])
                LB = valueChild1
                delMenores = True
            else:
                if LB is None or (int(valueChild1) > LB and valueChild1 not in indexX):
                    itemCandidatos.append(childKS1)
                    indexCandidatos.append([valueChild1, indPerm1])
                    indexX.append(valueChild1)
        if (childKS2 is not None and indPerm2 is not None):
            valueChild2 = getValue(childKS2)
            if indPerm2 == -1 and (valueChild2 > LB or LB is None):
                potentialCantidatos.append([childKS2, valueChild2])
                LB = valueChild2
                delMenores = True
            else:
                if LB is None or (int(valueChild2) > LB and valueChild2 not in indexX):
                    itemCandidatos.append(childKS2)
                    indexCandidatos.append([valueChild2, indPerm2])
                    indexX.append(valueChild2)
        # Eliminar los items menores cuando se encuentra un nuevo LB mayor al anterior
        if (delMenores is True and LB is not None):
            for i, j in zip(indexCandidatos, itemCandidatos):
                if (int(i[0]) <= LB):
                    indexCandidatos.remove(i)
                    itemCandidatos.remove(j)
            delMenores = False
        # Si todavia hay items por procesar, continuars
        if len(itemCandidatos) > 0:
            itemMax = np.argmax(indexCandidatos, axis=0)[0]
            if (indexCandidatos[itemMax][1] < LB or LB is None):
                # Seleccionamos el nuevo padre para la siguiente iteracion
                fKnapSack = itemCandidatos[itemMax]
                indexPer = indexCandidatos[itemMax][1]
                print("\tItem Elegido: " + str(indexCandidatos[itemMax][0])),
                del (indexCandidatos[itemMax])
                del (itemCandidatos[itemMax])
            else:
                printSolution()
                break
        else:
            printSolution()
            break
        print "\tTime: " + str(int(time.time() - oldTime)),
        print "\tBest: " + str(LB),
        print "\t# Candidatos: " + str(len(indexCandidatos))


elementos, capacity = rF.readTxtFile()
numElementos = len(elementos)
startBranchAndBound()
