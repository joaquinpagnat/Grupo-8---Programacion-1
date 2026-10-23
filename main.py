import Crear_Matriz
import gestion


def main():
    """ Ejecuta el ciclo principal del sistema de gestión de alumnos y notas """
    config = gestion.configuracion()
    preparado = False
    try:
        gestion.preparar_archivos(config)
        preparado = True
    except FileNotFoundError as mensaje:
        print("No se puede abrir el archivo:", mensaje)
    except (ValueError, OSError) as mensaje:
        print("No se pudo iniciar el sistema:", mensaje)

    if preparado:
        opcion = 0
        while opcion != 12:
            try:
                opcion = Crear_Matriz.menu()
                if opcion == 12:
                    print("Programa finalizado. Los cambios quedaron guardados.")
                elif Crear_Matriz.ejecutar_opcion(config, opcion):
                    print("Operación realizada. Cambios guardados correctamente.")
            except FileNotFoundError as mensaje:
                print("No se puede abrir el archivo:", mensaje)
            except (ValueError, AssertionError) as mensaje:
                print("Datos inválidos:", mensaje)
            except OSError as mensaje:
                print("Error de archivo:", mensaje)
            except KeyboardInterrupt:
                print("\nOperación cancelada por el usuario.")


# Programa principal
main()


