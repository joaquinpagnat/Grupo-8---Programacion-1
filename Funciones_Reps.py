"""Lectura de datos y menús con validación de entradas."""

import gestion


class CancelarOperacion(Exception):
    """Se vuelve al menú sin aplicar cambios incompletos."""


def leer(mensaje):
    texto = input(mensaje).strip()
    if texto.casefold() == "/cancelar":
        raise CancelarOperacion
    return texto


def validar_opcion(mensaje, minimo, maximo):
    if minimo > maximo:
        raise ValueError("No hay opciones disponibles.")
    while True:
        try:
            opcion = int(leer(mensaje))
        except ValueError:
            print("Ingresá un número entero.")
            continue
        if minimo <= opcion <= maximo:
            return opcion
        print(f"Elegí una opción entre {minimo} y {maximo}.")


def elegir(opciones, mensaje="Elegí una opción: "):
    if not opciones:
        print("No hay opciones disponibles.")
        return None
    for numero, opcion in enumerate(opciones, 1):
        print(f"{numero} - {opcion}")
    print("0 - Volver")
    numero = validar_opcion(mensaje, 0, len(opciones))
    return numero - 1 if numero else None


def validar_nota():
    while True:
        try:
            return gestion.validar_nota(leer("Nota entre 1 y 10 (se aceptan decimales): "))
        except ValueError as error:
            print(error)


def confirmar(mensaje):
    while True:
        respuesta = leer(f"{mensaje} (s/n): ").casefold()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no", ""):
            return False
        print("Respondé s o n.")

