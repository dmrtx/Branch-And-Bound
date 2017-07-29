import Tkinter as tk
import re
import tkFileDialog as filedialog


def readTxtFile():
    # Mostrar una pantalla de seleccion del archivo
    root = tk.Tk();
    root.withdraw();
    file_path = filedialog.askopenfilename();
    cleanedContent = []
    # Recuperar las lineas del archivo de texto
    with open(file_path) as f:
        content = f.readlines()
    for i in content:
        cleanedContent.append(re.sub("\s\s+", " ", i.strip()))
    fL = cleanedContent[0].replace("\n", "").replace("\t", " ").split(' ')
    # Recuperar el numero de dimensiones y la posicion en la que se lee los numeros
    numElementos = int(fL[0])
    capacity = float(fL[1])
    elementos = []
    for i in range(2, numElementos + 2, 1):
        conLine = cleanedContent[i].replace("\n", "").replace("\t", " ").split(' ')
        elementos.append(map(float, conLine))
    return elementos, capacity
