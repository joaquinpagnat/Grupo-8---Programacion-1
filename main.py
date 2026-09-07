import Crear_Matriz, Funciones_Reps

def main():

    matriz = []
    

    # Listas de alumnos y materias
    preAlumnos = [
        "Matias Lopez", "Carlos Gomez", "Daniela Fernandez", "Juan Perez", 
        "Sofia Rodriguez", "Lucia Gonzalez", "Pedro Martinez", "Florencia Sanchez", 
        "Valentina Romero", "Diego Diaz", "Martina Alvarez", "Alejandro Ruiz", 
        "Camila Alonso", "Gabriel Torres", "Julieta Silva"
    ]
    
    preMaterias = [
        "Matematica", "Literatura", "Electrotecnia", "Ingles", 
        "Fisica", "Quimica", "Historia", "Geografia", 
        "Biologia", "Informatica", "Educacion Fisica"
    ]

    filas = len(preAlumnos)
    columnas = len(preMaterias)
    
    Crear_Matriz.crear_matriz(filas, columnas, matriz)


    opcion = 0

    
    while opcion != 5:
        
        opcion = Crear_Matriz.menu()

        if opcion == 1:
            print("\n--- Has elegido Alta de alumno ---")
            Crear_Matriz.agregar_persona(preAlumnos, preMaterias, matriz)
            
            
        elif opcion == 2:
            print("\n--- Has elegido Agregar Nota ---")
            Crear_Matriz.agregar_notas(preAlumnos, preMaterias, matriz)
            print("¡Nota agregada con éxito!\n")
            
        elif opcion == 3:
            print("\n--- Has elegido Modificar Nota ---")
            Crear_Matriz.modificar_nota(matriz,preAlumnos,preMaterias)
            
        elif opcion == 4:
            print("\n--- Has elegido Ver notas ---")
            Crear_Matriz.mostrar_notas_alumno(matriz,preAlumnos, preMaterias)
            
        elif opcion == 5:
            print("\n¡Gracias por usar el sistema!")

main()
        
