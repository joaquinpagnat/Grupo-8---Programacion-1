"""Entrada por teclado y opciones; funciones y excepciones de las clases 02 y 08."""

import gestion


def leer(mensaje):
    texto = input(mensaje).strip()
    if texto.lower() == "/cancelar":
        raise KeyboardInterrupt
    return texto


def validar_opcion(mensaje, minimo, maximo):
    while True:
        try:
            numero = int(leer(mensaje))
            if minimo <= numero <= maximo:
                break
            print(f"Elegí un número entre {minimo} y {maximo}.")
        except ValueError:
            print("Ingresá un número entero.")
    return numero


def elegir(opciones, mensaje="Elegí una opción: "):
    for i in range(len(opciones)):
        print(f"{i + 1} - {opciones[i]}")
    print("0 - Volver")
    numero = validar_opcion(mensaje, 0, len(opciones))
    indice = numero - 1 if numero != 0 else None
    return indice


def leer_nota():
    while True:
        try:
            nota = gestion.validar_nota(leer("Nota entre 1 y 10 (admite coma o punto decimal): "))
            break
        except ValueError as error:
            print(error)
    return nota


def confirmar(mensaje):
    while True:
        texto = leer(mensaje + " (s/n): ").lower()
        if texto in ("s", "si", "sí", "n", "no", ""):
            break
        print("Respondé s o n.")
    return texto in ("s", "si", "sí")
