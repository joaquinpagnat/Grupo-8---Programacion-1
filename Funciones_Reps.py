
def validar_opcion(mensaje,minimo,maximo):

    opcion = int(input(mensaje))

    while opcion < minimo or opcion > maximo:

        opcion = int(input(f"elija una opcion entre {minimo} y {maximo}: "))

    return opcion


def validar_nota(minimo,maximo):

    nota = int(input("ingresa la nota: "))

    while nota < minimo or nota > maximo:

        nota = nota = int(input(f"ingresa una nota entre {minimo} y {maximo}: "))

    return nota

def mostrar_alumnos(estudiantes):

    for i in range(len(estudiantes)):
        print(f"{i+1} = {estudiantes[i]}")
    print()

def mostrar_materias(materias):
    for i in range(len(materias)):
        print(f"{i+1} = {materias[i]}")
    print()
    
