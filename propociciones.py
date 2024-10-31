import re
import tkinter as tk
from tkinter import ttk
import itertools

class Nodo:
    def __init__(self, valor, izquierda=None, derecha=None):
        self.valor = valor
        self.izquierda = izquierda
        self.derecha = derecha

def descomponer_proposicion(proposicion):
    partes = re.split(r'\s+(y|and|o|or|no|not)\s+', proposicion)
    proposiciones_simples = []
    operador = None

    for parte in partes:
        if parte.lower() in ["y", "and"]:
            operador = "AND"
        elif parte.lower() in ["o", "or"]:
            operador = "OR"
        elif parte.lower() in ["no", "not"]:
            operador = "NOT"
        else:
            proposiciones_simples.append(parte.strip())

    return proposiciones_simples, operador

def construir_arbol(proposiciones_simples, operador):
    if operador == "AND":
        return Nodo(proposiciones_simples[0], 
                    Nodo("Sí", Nodo(proposiciones_simples[1], Nodo("Sí"), Nodo("No"))),
                    Nodo("No", Nodo(proposiciones_simples[1], Nodo("Sí"), Nodo("No"))))
    elif operador == "OR":
        return Nodo(proposiciones_simples[0], 
                    Nodo("Sí", Nodo(proposiciones_simples[1], Nodo("Sí"), Nodo("No"))),
                    Nodo("No", Nodo(proposiciones_simples[1], Nodo("Sí"), Nodo("No"))))
    elif operador == "NOT":
        return Nodo(proposiciones_simples[0], 
                    Nodo("No", Nodo(proposiciones_simples[1], Nodo("No"), Nodo("Sí"))),
                    Nodo("Sí", Nodo(proposiciones_simples[1], Nodo("No"), Nodo("Sí"))))
    return None

def evaluar_proposicion(proposiciones_simples, operador):
    valores = []
    for proposicion in proposiciones_simples:
        while True:
            valor = input(f"¿Es '{proposicion}' verdadera o falsa? (true/false): ").strip().lower()
            if valor in ["true", "false"]:
                valores.append(valor == "true")
                break
            else:
                print("Por favor, ingresa 'true' o 'false'.")

    if operador == "AND":
        resultado = all(valores)
    elif operador == "OR":
        resultado = any(valores)
    elif operador == "NOT":
        resultado = not valores[0]
    else:
        resultado = None

    return resultado, valores

def imprimir_arbol(nodo, nivel=0):
    if nodo is not None:
        imprimir_arbol(nodo.derecha, nivel + 1)
        print(' ' * 4 * nivel + '-> ' + nodo.valor)
        imprimir_arbol(nodo.izquierda, nivel + 1)

def mostrar_arbol(nodo, nivel=0):
    if nodo is not None:
        mostrar_arbol(nodo.derecha, nivel + 1)
        print(' ' * 4 * nivel + '-> ' + nodo.valor)
        mostrar_arbol(nodo.izquierda, nivel + 1)

def seleccionar_proposicion(proposiciones_simples):
    ventana = tk.Tk()
    ventana.title("Seleccionar Proposición")

    label = tk.Label(ventana, text="Seleccione la proposición que desea comprobar:")
    label.pack()

    seleccion = tk.StringVar()
    for proposicion in proposiciones_simples:
        radio = tk.Radiobutton(ventana, text=proposicion, variable=seleccion, value=proposicion)
        radio.pack(anchor=tk.W)

    def confirmar_seleccion():
        seleccionada = seleccion.get()
        if seleccionada:
            ventana.destroy()
            print(f"Ha seleccionado la proposición: {seleccionada}")
        else:
            mensaje.config(text="Por favor, seleccione una proposición para comprobar.")

    boton = tk.Button(ventana, text="Comprobar", command=confirmar_seleccion)
    boton.pack()

    mensaje = tk.Label(ventana, text="")
    mensaje.pack()

    ventana.mainloop()
    return seleccion.get()

def mostrar_tabla_proposiciones(proposiciones, operador):
    ventana = tk.Tk()
    ventana.title("Tabla de Proposiciones")
    tree = ttk.Treeview(ventana, columns=("Número", "Proposición", "Operador", "Letra"), show="headings")
    tree.heading("Número", text="Número")
    tree.heading("Proposición", text="Proposición")
    tree.heading("Operador", text="Operador")
    tree.heading("Letra", text="Letra")

    letras = "abcdefghijklmnopqrstuvwxyz"
    for i, proposicion in enumerate(proposiciones, start=1):
        letra = letras[i-1]
        tree.insert("", tk.END, values=(i, proposicion, operador, letra))

    tree.pack()
    ventana.mainloop()

def generar_expresion_logica(proposiciones, operador):
    letras = "abcdefghijklmnopqrstuvwxyz"
    if operador == "AND":
        return " ^ ".join(letras[i] for i in range(len(proposiciones)))
    elif operador == "OR":
        return " v ".join(letras[i] for i in range(len(proposiciones)))
    elif operador == "NOT":
        return "¬" + letras[0]
    return ""

def generar_tabla_verdad(proposiciones, operador):
    n = len(proposiciones)
    combinaciones = list(itertools.product([0, 1], repeat=n))
    tabla = []

    for combinacion in combinaciones:
        fila = {}
        for i, proposicion in enumerate(proposiciones):
            fila[proposicion] = combinacion[i]
        if operador == "AND":
            fila["Resultado"] = all(fila[prop] for prop in proposiciones)
        elif operador == "OR":
            fila["Resultado"] = any(fila[prop] for prop in proposiciones)
        elif operador == "NOT":
            fila["Resultado"] = not fila[proposiciones[0]]
        tabla.append(fila)

    return tabla

def mostrar_tabla_verdad(tabla, proposiciones):
    ventana = tk.Tk()
    ventana.title("Tabla de Verdad")
    tree = ttk.Treeview(ventana, columns=proposiciones + ["Resultado"], show="headings")
    for prop in proposiciones + ["Resultado"]:
        tree.heading(prop, text=prop)
    
    for fila in tabla:
        valores = [fila[prop] for prop in proposiciones]
        resultado = fila["Resultado"]
        tree.insert("", "end", values=valores + [resultado])
    
    tree.pack()
    ventana.mainloop()

def guardar_resultados(proposiciones, operador, resultado, valores, expresion_logica, tabla_verdad):
    with open("resultados.txt", "w") as file:
        file.write("Proposiciones Simples:\n")
        for prop in proposiciones:
            file.write(f"- {prop}\n")
        file.write(f"\nOperador: {operador}\n")
        file.write(f"\nResultado de la Evaluación: {resultado}\n")
        file.write(f"\nValores de las Proposiciones: {valores}\n")
        file.write(f"\nExpresión Lógica: {expresion_logica}\n")
        file.write("\nTabla de Verdad:\n")
        for fila in tabla_verdad:
            file.write(f"{fila}\n")

def mostrar_arbol_grafico(nodo, canvas, x, y, dx, dy):
    if nodo is not None:
        canvas.create_text(x, y, text=nodo.valor, font=("Arial", 12, "bold"))
        if nodo.izquierda:
            canvas.create_line(x, y, x - dx, y + dy, arrow=tk.LAST)
            mostrar_arbol_grafico(nodo.izquierda, canvas, x - dx, y + dy, dx // 2, dy)
        if nodo.derecha:
            canvas.create_line(x, y, x + dx, y + dy, arrow=tk.LAST)
            mostrar_arbol_grafico(nodo.derecha, canvas, x + dx, y + dy, dx // 2, dy)

def crear_interfaz_arbol(arbol):
    ventana = tk.Tk()
    ventana.title("Árbol de Decisiones")
    canvas = tk.Canvas(ventana, width=800, height=600, bg="white")
    canvas.pack()
    mostrar_arbol_grafico(arbol, canvas, 400, 50, 200, 100)
    ventana.mainloop()

def mostrar_expresion_logica(expresion_logica):
    ventana = tk.Tk()
    ventana.title("Expresión Lógica")
    label = tk.Label(ventana, text="Expresión Lógica Generada:")
    label.pack()
    expresion = tk.Label(ventana, text=expresion_logica, font=("Arial", 14))
    expresion.pack()
    ventana.mainloop()

# Ejemplo de uso
num_proposiciones = int(input("¿Cuántas proposiciones deseas evaluar? "))
proposiciones = []
for i in range(num_proposiciones):
    proposicion = input(f"Introduce la proposición {i+1}: ")
    proposiciones.append(proposicion)

proposicion_compuesta = " y ".join(proposiciones)
proposiciones_simples, operador = descomponer_proposicion(proposicion_compuesta)
seleccionada = seleccionar_proposicion(proposiciones_simples)
arbol = construir_arbol(proposiciones_simples, operador)
resultado, valores = evaluar_proposicion(proposiciones_simples, operador)

print("Árbol de Decisiones:")
imprimir_arbol(arbol)

expresion_logica = generar_expresion_logica(proposiciones_simples, operador)
print("\nExpresión lógica:", expresion_logica)

tabla_verdad = generar_tabla_verdad(proposiciones_simples, operador)
print("\nTabla de verdad:")
for fila in tabla_verdad:
    print(fila)

mostrar_tabla_verdad(tabla_verdad, proposiciones_simples)

guardar_resultados(proposiciones_simples, operador, resultado, valores, expresion_logica, tabla_verdad)

# Mostrar el árbol de decisiones
print("Árbol de Decisiones:")
imprimir_arbol(arbol)
crear_interfaz_arbol(arbol)
