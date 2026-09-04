import Funciones_Reps

def menu():
    print("Bienvenido al sistema de gestion de notas.")
    print("1 - Alta de alumno")
    print("2 - Agregar Nota")
    print("3 - Modificar Nota")
    print("4 - Ver notas de un alumno")
    print("5 - Salir")


    opcion = Funciones_Reps.validar_opcion("elija una opcion: ", 1, 5)
    return opcion

def crear_matriz(filas, columnas, matriz):
    for f in range(filas):
        matriz.append([])
        for c in range(columnas):
            matriz[f].append([])


def mostrar_alumnos(preAlumnos):
    for i in range(len(preAlumnos)):
        print(f"{i+1} = {preAlumnos[i]}")
    print()

def mostrar_materias(preMaterias):
    for i in range(len(preMaterias)):
        print(f"{i+1} = {preMaterias[i]}")
    print()

def agregar_notas(preAlumnos, preMaterias, matriz):
    
    mostrar_alumnos(preAlumnos)
    
    opcionA = Funciones_Reps.validar_opcion("seleccione un alumno: ", 1, len(preAlumnos))
    fila = opcionA - 1

    mostrar_materias(preMaterias)
    print("="*60)
    print()
    
    opcionM = Funciones_Reps.validar_opcion("seleccione una materia: ", 1, len(preMaterias))
    columna = opcionM - 1

    matriz[fila][columna].append(Funciones_Reps.validar_nota(1, 10))

def agregar_persona(preAlumnos, preMaterias, matriz):

    nombre = input("Ingrese el nombre y apellido del alumno: ").title()
    preAlumnos.append(nombre)
    nueva_fila = []
    for c in range(len(preMaterias)):
        nueva_fila.append([])
        matriz.append(nueva_fila)
    
    print(f"\n¡{nombre} se dio de alta correctamente!")


def validar_nombre_persona(preAlumnos, preMaterias, Matriz):
    pass
