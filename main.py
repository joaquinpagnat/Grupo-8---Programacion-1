"""Ejecutar con: python main.py (Python 3.9 o posterior)."""

from copy import deepcopy
from pathlib import Path

import Crear_Matriz
import Funciones_Reps
import gestion


RUTA_DATOS = Path(__file__).resolve().with_name("datos.json")


def main(ruta_datos=RUTA_DATOS):
    try:
        datos = gestion.cargar_datos(ruta_datos)
    except (OSError, ValueError) as error:
        print(f"No se pudo abrir el sistema: {error}")
        print("El archivo original se conserva. Revisalo o restaurá una copia antes de volver a iniciar.")
        return 1

    print("Cada cambio se guarda automáticamente en datos.json.")
    while True:
        try:
            opcion = Crear_Matriz.menu()
            if opcion == 12:
                print("Hasta luego. Los cambios realizados quedaron guardados.")
                return 0
            # Trabajamos sobre una copia: cancelar o fallar al guardar no deja cambios a medias.
            nuevos = deepcopy(datos)
            hubo_cambios = Crear_Matriz.ACCIONES[opcion](nuevos)
            if hubo_cambios:
                gestion.guardar_datos(nuevos, ruta_datos)
                datos = nuevos
                print("Operación realizada. Cambios guardados correctamente.")
        except Funciones_Reps.CancelarOperacion:
            print("Operación cancelada. No se aplicaron cambios.")
        except ValueError as error:
            print(f"No se aplicaron cambios: {error}")
        except OSError as error:
            print(f"No se pudo guardar: {error}. No se aplicaron los cambios de esta operación.")
        except (EOFError, KeyboardInterrupt):
            print("\nPrograma cerrado. Se conservaron las operaciones ya guardadas.")
            return 0


if __name__ == "__main__":
    raise SystemExit(main())

