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



def crear_matriz(filas,columnas,matriz):

    for f in range(filas):

        matriz.append([])

        for c in range(columnas):

            matriz[f].append([])
            


def agregar_notas(preAlumnos, preMaterias, matriz):
    
    Funciones_Reps.mostrar_alumnos(preAlumnos)
    
    opcionA = Funciones_Reps.validar_opcion("seleccione un alumno: ", 1, len(preAlumnos))
    fila = opcionA - 1

    Funciones_Reps.mostrar_materias(preMaterias)
    print("="*60)
    print()
    
    opcionM = Funciones_Reps.validar_opcion("seleccione una materia: ", 1, len(preMaterias))
    columna = opcionM - 1

    matriz[fila][columna].append(Funciones_Reps.validar_nota(1, 10))

def modificar_nota(matriz,estudiantes,materias):

    Funciones_Reps.mostrar_alumnos(estudiantes)

    opcionA = Funciones_Reps.validar_opcion("seleccione un alumno: ",1,len(estudiantes))

    Funciones_Reps.mostrar_materias(materias)

    opcionM = Funciones_Reps.validar_opcion("seleccione la materia: ",1,len(materias))
    
    if len(matriz[opcionA-1][opcionM-1]) == 0:
        
        print("\n--- no hay parcales a modificar ---")
        
    else:
    
        print(f" parciales de {estudiantes[opcionA-1]} en {materias[opcionM-1]} : {matriz[opcionA-1][opcionM-1]}")

        pos = Funciones_Reps.validar_opcion("elija el parcial a modificar: ",1,len(matriz[opcionA-1][opcionM-1]))

        nueva_nota = Funciones_Reps.validar_nota(1,10)
        
        matriz[opcionA-1][opcionM-1][pos-1] = nueva_nota
        

def mostrar_notas_alumno(matriz,estudiantes, materias):
    
    Funciones_Reps.mostrar_alumnos(estudiantes)

    opcionA = Funciones_Reps.validar_opcion("seleccione un alumno: ",1,len(estudiantes))
    
    print(f"\n --- notas de {estudiantes[opcionA-1]} ---")
    print()
    for i in range(len(materias)):
        
        print(f"{materias[i]} - {matriz[opcionA-1][i]}")


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

