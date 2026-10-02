"""Programa principal. Abrir con Iniciar.bat o ejecutar python main.py."""

import Crear_Matriz
import gestion


def main():
    config = gestion.configuracion()
    preparado = False
    try:
        gestion.preparar_archivos(config)
        preparado = True
    except (OSError, ValueError) as error:
        print("No se pudo iniciar:", error)

    if preparado:
        print("Cada cambio se guarda automáticamente en archivos de texto.")
        print("Si es el primer inicio, se incluyen 15 alumnos y 11 materias de ejemplo.")
        while True:
            try:
                opcion = Crear_Matriz.menu()
                if opcion == 12:
                    print("Hasta luego. Los cambios realizados quedaron guardados.")
                    break
                if Crear_Matriz.ejecutar_opcion(config, opcion):
                    print("Operación realizada. Cambios guardados correctamente.")
            except KeyboardInterrupt:
                print("\nOperación cancelada. Volviendo al menú.")
            except EOFError:
                print("\nPrograma cerrado. Se conservaron las operaciones ya guardadas.")
                break
            except (ValueError, OSError, UnicodeError) as error:
                print("No se pudo completar la operación:", error)


# Programa principal (clase 02).
main()
