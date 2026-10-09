import Crear_Matriz
import gestion


# Programa principal: cada opción llama directamente a su función.
config = gestion.configuracion()
opcion = 0
try:
    gestion.preparar_archivos(config)
except (OSError, ValueError) as error:
    print("No se pudo iniciar:", error)
    opcion = 12

while opcion != 12:
    try:
        opcion = Crear_Matriz.menu()
        if opcion == 1:
            Crear_Matriz.agregar_persona(config)
        elif opcion == 2:
            Crear_Matriz.editar_nota(config)
        elif opcion == 3:
            Crear_Matriz.editar_nota(config, modificar=True)
        elif opcion == 4 or opcion == 7:
            Crear_Matriz.mostrar_notas_alumno(config)
        elif opcion == 5:
            Crear_Matriz.eliminar_alumno(config)
        elif opcion == 6:
            Crear_Matriz.modificar_persona(config)
        elif opcion == 8:
            Crear_Matriz.inscribir_alumno(config)
        elif opcion == 9:
            Crear_Matriz.quitar_materia(config)
        elif opcion == 10:
            Crear_Matriz.agregar_materia(config)
        elif opcion == 11:
            Crear_Matriz.listar_alumnos(config)
        else:
            print("Hasta luego. Los cambios realizados quedaron guardados.")
    except KeyboardInterrupt:
        print("\nOperación cancelada. Volviendo al menú.")
    except EOFError:
        print("\nPrograma cerrado.")
        opcion = 12
    except (ValueError, OSError) as error:
        print("No se pudo completar la operación:", error)
