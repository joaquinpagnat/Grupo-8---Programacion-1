import gestion


def leer(mensaje):
    """Lee una cadena por teclado quitando espacios en los extremos."""
    texto = input(mensaje).strip()
    return texto


def validar_opcion(mensaje, minimo, maximo):
    """Solicita un número entero validando que se encuentre entre minimo y maximo."""
    while True:
        try:
            numero = int(leer(mensaje))
            assert minimo <= numero <= maximo
        except ValueError:
            print("Sólo se permiten números enteros. Intente nuevamente.")
        except AssertionError:
            print(f"Debe ingresar un número entre {minimo} y {maximo}.")
        else:
            break
    return numero


def elegir(opciones, mensaje="Elegí una opción: "):
    """Muestra una secuencia de opciones numeradas y devuelve el subíndice elegido."""
    for i, opcion in enumerate(opciones):
        print(f"{i + 1} - {opcion}")
    print("0 - Volver")
    numero = validar_opcion(mensaje, 0, len(opciones))
    indice = numero - 1 if numero != 0 else None
    return indice


def leer_nota():
    """Solicita y valida una calificación numérica entre 1 y 10."""
    while True:
        try:
            nota = gestion.validar_nota(leer("Nota entre 1 y 10: "))
        except ValueError as mensaje:
            print(mensaje)
        else:
            break
    return nota


def confirmar(mensaje):
    """Solicita confirmación por sí o por no al usuario."""
    while True:
        try:
            texto = leer(mensaje + " (s/n): ").lower()
            assert texto in ("s", "si", "sí", "n", "no")
        except AssertionError:
            print("Respuesta inválida. Ingrese 's' o 'n'.")
        else:
            break
    return texto in ("s", "si", "sí")


