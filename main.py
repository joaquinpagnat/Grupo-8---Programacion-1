import Crear_Matriz
import gestion


# Programa principal: cada opción llama directamente a su función.
config = gestion.configuracion()
opcion = 12
try:
    gestion.preparar_archivos(config)
    opcion = 0
except FileNotFoundError as error:
    print("No se encontró un archivo necesario para iniciar:", error)
except PermissionError as error:
    print("No hay permiso para acceder a los archivos:", error)
except OSError as error:
    print("No se pudieron preparar los archivos:", error)
except UnicodeError as error:
    print("Un archivo contiene texto con una codificación inválida:", error)
except ValueError as error:
    print("No se pudo iniciar por un problema con los datos:", error)
except KeyboardInterrupt:
    print("\nInicio cancelado.")
except:
    print("Ocurrió un error inesperado al iniciar. El programa se cerrará.")

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
    except FileNotFoundError as error:
        print("No se encontró un archivo necesario:", error)
    except PermissionError as error:
        print("No hay permiso para leer o guardar el archivo:", error)
    except OSError as error:
        print("Ocurrió un problema al leer o guardar los archivos:", error)
    except UnicodeError as error:
        print("Un archivo contiene texto con una codificación inválida:", error)
    except ValueError as error:
        print("Los datos no son válidos:", error)
    except:
        print("Ocurrió un error inesperado. Volviendo al menú.")
