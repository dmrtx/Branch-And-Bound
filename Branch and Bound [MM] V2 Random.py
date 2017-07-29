import random as rnd
import time

import numpy as np

import ReadFile as rF

# Guardar los candidatos potenciales
potentialCantidatos = []
# Guarda los nodos padre
itemCandidatos = []
# Guarda datos de los cantidatos tamano y lugar donde hay un float
indexCandidatos = []
# Almacena las preferencias de los hijos
indexPlantillas = {}
# Indice
indexIdNodos = 0
# Nodo potencial con el mayor valor
LB = None
# Variable que indica si se debe borrar los nodos con valor menor a LB
delMenores = True
# Variable que alamacena los valores de los nodos para no utilizar uno que tenga un valor igual
indexX = []
timeTotal = 0
maxTime = 60


# Imprimir el resultado
def printResult(elmts, resultado):
    tmpRes = []
    print "X = [",
    for i, j in zip(range(1, numElementos + 1), elmts):
        if (resultado[i] == 1):
            tmpRes.append(j[3])
    tmpRes = np.sort(tmpRes)
    for i in tmpRes:
        print(str(i) + " , "),
    print "]"


# Recuperar el valor total
def getValue(ksChild):
    valKS = 0.0
    for i, j in zip(range(1, numElementos + 1), range(0, numElementos)):
        if ksChild[i] != -1:
            valKS += ksChild[i] * elementos[j][1]
    return valKS


# Recuperar el peso total
def getWeight(ksChild):
    valKS = 0.0
    for i, j in zip(range(1, numElementos + 1), range(0, numElementos)):
        if ksChild[i] != -1:
            valKS += ksChild[i] * elementos[j][0]
    return valKS


# Crear hijo, a partir de lo marcado
def createChild(ksChild):
    indexPer = -1
    countKap = getWeight(ksChild)
    # Comprueba si la capacidad actual del nodo es menor a la maxima, para agregar
    if countKap <= capacity:
        for indexEl in range(0, numElementos, 1):
            # Comprueba el item del nodo es -1
            if (ksChild[indexEl + 1] == -1.0):
                # Comprueba si al agregar el elemento se sobrepasa la capacidad
                if (countKap + elementos[indexEl][0] > capacity):
                    cp = int(capacity - countKap)
                    # Si la capacidad es mayor al valor actual se asigna un float
                    if (cp > 0):
                        el = int(elementos[indexEl][0])
                        ksChild[indexEl + 1] = float(cp) / float(el)
                        indexPer = indexEl + 1
                    else:
                        ksChild[indexEl + 1] = 0.0
                else:
                    ksChild[indexEl + 1] = 1.0
                countKap += elementos[indexEl][0]
        return ksChild, indexPer
    else:
        return None, None


# Imprime solucion
def printSolution():
    valPC = 0
    pcMax = []
    for i in potentialCantidatos:
        if (i[1] > valPC):
            pcMax = i
            valPC = i[1]
    printResult(elementos, pcMax[0])
    print("Beneficio: " + str(valPC))
    print("Peso: " + str(getWeight(pcMax[0])))
    print("Tiempo: " + str(timeTotal))


def startBranchAndBound():
    global elementos, indexCandidatos, indexPlantillas, indexIdNodos, LB, delMenores, indexX, timeTotal
    oldTime = time.time()
    elementos = [x + [0.0] + [j] for x, j in zip(elementos, range(1, len(elementos) + 1, 1))]
    # Calcular el ratio de volumen sobre el beneficio
    for i in elementos:
        i[2] = i[1] / i[0]  # Valor/Volumen
    # Ordenar los elementos de mayor a menor
    elementos.sort(key=lambda x: x[2], reverse=True)
    # Llenar el knapsack padre, el primer elemento es un Id para la rama
    fKnapSack = [0]
    fKnapSack.extend([-1.0 for i in range(0, len(elementos), 1)])
    # LLenar el primer elementos con los datos mas prometedores
    fKnapSack, indexPer = createChild(fKnapSack)
    while (True):
        # Declarar los nuevos hijos que se van a crear
        childKS1 = [indexIdNodos + 1]
        childKS2 = [indexIdNodos + 2]
        indexIdNodos += 2;
        # Buscar las preferencias del padre para juntarlas con las del los hijos\
        try:
            prefFather = indexPlantillas[fKnapSack[0]]
        except:
            # Cuando no encuentra preferencias del padre
            prefFather = []
        # Almacenar las preferencias de los hijos
        indexPlantillas[childKS1[0]] = [[indexPer, 0.0]] + prefFather
        indexPlantillas[childKS2[0]] = [[indexPer, 1.0]] + prefFather
        # Generar los dos hijos de nuevos, a partir del indice que va permanente
        childKS1.extend([-1.0 for i in range(0, len(elementos), 1)])
        # Recorrer las preferencias el primer hijo
        for i in indexPlantillas[childKS1[0]]:
            childKS1[i[0]] = i[1]
        childKS2.extend([-1.0 for i in range(0, len(elementos), 1)])
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
                if LB is None or (int(valueChild1) > LB):
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
                if LB is None or (int(valueChild2) > LB):
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
        if len(itemCandidatos) > 0 and timeTotal < maxTime:
            # Elige un nodo con mayor valor para que se divida
            itemMax = rnd.randrange(0, len(indexCandidatos))
            if (indexCandidatos[itemMax][1] < LB or LB is None):
                # Seleccionamos el nuevo padre para la siguiente iteracion
                fKnapSack = itemCandidatos[itemMax]
                indexPer = indexCandidatos[itemMax][1]
                print("\tItem: " + str(indexCandidatos[itemMax][0])),
                del (indexCandidatos[itemMax])
                del (itemCandidatos[itemMax])
            else:
                printSolution()
                break
        else:
            printSolution()
            break
        timeTotal = time.time() - oldTime
        print "\tTime: " + str(int(timeTotal)),
        print "\tBest: " + str(LB),
        print "\t# Candidatos: " + str(len(indexCandidatos))


elementos, capacity = rF.readTxtFile()
numElementos = len(elementos)
startBranchAndBound()
