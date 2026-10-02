"""Interfaz de consola. Se conserva el nombre del módulo del proyecto original.

Los datos ahora se relacionan mediante diccionarios, en lugar de índices de una
matriz: eliminar un alumno no cambia las materias ni las notas de los demás.
"""

from datetime import date

import Funciones_Reps as entrada
import gestion


def menu():
    print("\nGESTIÓN DE ALUMNOS Y NOTAS")
    print("-" * 50)
    print("1 - Alta de alumno")
    print("2 - Agregar nota")
    print("3 - Modificar nota")
    print("4 - Ver notas de un alumno")
    print("5 - Eliminar alumno")
    print("6 - Modificar datos de un alumno")
    print("7 - Buscar alumno y ver su ficha")
    print("8 - Inscribir alumno en una materia")
    print("9 - Quitar inscripción sin notas")
    print("10 - Agregar materia al catálogo")
    print("11 - Listar alumnos")
    print("12 - Salir")
    print("-" * 50)
    print("Podés escribir /cancelar para volver al menú.")
    return entrada.validar_opcion("Elegí una opción: ", 1, 12)


def etiqueta_alumno(legajo, alumno):
    return f"Legajo {legajo} | {alumno['apellido']}, {alumno['nombre']} | DNI {alumno['dni']}"


def seleccionar_alumno(datos):
    if not datos["alumnos"]:
        print("No hay alumnos cargados. Primero usá Alta de alumno.")
        return None
    while True:
        consulta = entrada.leer("Buscar por nombre, apellido, DNI completo o #legajo (Enter para volver): ")
        if not consulta:
            return None
        resultados = gestion.buscar_alumnos(datos, consulta)
        if not resultados:
            print("No se encontraron alumnos. Probá otra búsqueda.")
            continue
        indice = entrada.elegir([etiqueta_alumno(codigo, alumno) for codigo, alumno in resultados],
                                "Seleccioná un resultado: ")
        return resultados[indice][0] if indice is not None else None


def leer_ficha(actual=None):
    ficha = {}
    campos = (("nombre", "Nombre"), ("apellido", "Apellido"), ("dni", "DNI"),
              ("email", "Correo electrónico (opcional)"), ("telefono", "Teléfono (opcional)"))
    if actual is not None:
        print("Enter conserva el dato actual. Un guion borra el correo o el teléfono.")
    for clave, titulo in campos:
        anterior = actual[clave] if actual is not None else ""
        mensaje = f"{titulo} (actual: {anterior or 'Sin informar'}): " if actual is not None else f"{titulo}: "
        valor = entrada.leer(mensaje)
        if actual is not None and not valor:
            valor = anterior
        if clave in ("email", "telefono") and valor == "-":
            valor = ""
        ficha[clave] = valor
    return ficha


def agregar_persona(datos):
    ficha = leer_ficha()
    legajo = gestion.alta_alumno(datos, **ficha)
    print(f"Legajo asignado: {legajo}. Para asignar materias usá la opción 8.")
    return True


def modificar_persona(datos):
    legajo = seleccionar_alumno(datos)
    if legajo is None:
        return False
    ficha = leer_ficha(datos["alumnos"][legajo])
    gestion.modificar_alumno(datos, legajo, **ficha)
    return True


def eliminar_alumno(datos):
    legajo = seleccionar_alumno(datos)
    if legajo is None:
        return False
    alumno = datos["alumnos"][legajo]
    cantidad = sum(len(i["notas"]) for i in alumno["inscripciones"])
    print(etiqueta_alumno(legajo, alumno))
    print(f"Se eliminarán su ficha, {len(alumno['inscripciones'])} inscripciones y {cantidad} notas.")
    if not entrada.confirmar("¿Confirmás la eliminación?"):
        print("Eliminación cancelada.")
        return False
    gestion.eliminar_alumno(datos, legajo)
    return True


def seleccionar_materia(datos):
    materias = sorted(datos["materias"].items(), key=lambda par: gestion.normalizar(par[1]))
    indice = entrada.elegir([nombre for codigo, nombre in materias], "Elegí una materia: ")
    return materias[indice][0] if indice is not None else None


def leer_anio():
    while True:
        texto = entrada.leer(f"Año de cursada (Enter = {date.today().year}): ")
        try:
            anio = int(texto) if texto else date.today().year
            gestion.validar_periodo(anio, gestion.PERIODOS[0])
            return anio
        except ValueError:
            print("Ingresá un año entre 1900 y 2100.")


def inscribir_alumno(datos):
    legajo = seleccionar_alumno(datos)
    if legajo is None:
        return False
    materia = seleccionar_materia(datos)
    if materia is None:
        return False
    anio = leer_anio()
    indice = entrada.elegir(gestion.PERIODOS, "Elegí el período de cursada: ")
    if indice is None:
        return False
    gestion.inscribir(datos, legajo, materia, anio, gestion.PERIODOS[indice])
    return True


def seleccionar_inscripcion(datos, legajo):
    inscripciones = datos["alumnos"][legajo]["inscripciones"]
    if not inscripciones:
        print("El alumno no tiene materias asignadas. Inscribilo con la opción 8.")
        return None
    ordenadas = sorted(inscripciones, key=lambda i: (
        i["anio"], gestion.PERIODOS.index(i["periodo"]), datos["materias"][i["materia"]]))
    opciones = [f"{datos['materias'][i['materia']]} | {i['anio']} | {i['periodo']}" for i in ordenadas]
    indice = entrada.elegir(opciones, "Elegí la materia y su período: ")
    return ordenadas[indice] if indice is not None else None


def quitar_materia(datos):
    legajo = seleccionar_alumno(datos)
    if legajo is None:
        return False
    inscripcion = seleccionar_inscripcion(datos, legajo)
    if inscripcion is None:
        return False
    if inscripcion["notas"]:
        print("No se puede quitar una inscripción que ya tiene notas.")
        return False
    if not entrada.confirmar("¿Quitás esta inscripción?"):
        return False
    gestion.quitar_inscripcion(datos, legajo, inscripcion["materia"], inscripcion["anio"], inscripcion["periodo"])
    return True


def editar_nota(datos, modificar=False):
    legajo = seleccionar_alumno(datos)
    if legajo is None:
        return False
    inscripcion = seleccionar_inscripcion(datos, legajo)
    if inscripcion is None:
        return False
    print("Se permite una nota para Parcial 1, una para Parcial 2 y una para Final.")
    disponibles = [e for e in gestion.EVALUACIONES if (e in inscripcion["notas"]) == modificar]
    if not disponibles:
        if modificar:
            print("Esta materia y período todavía no tienen notas para modificar.")
        else:
            print("Ya están cargadas las tres evaluaciones. Usá Modificar nota para corregirlas.")
        return False
    if not modificar and inscripcion["notas"]:
        print("Las evaluaciones ya cargadas se corrigen con Modificar nota.")
    opciones = [f"{e} (actual: {inscripcion['notas'][e]:g})" if modificar else e for e in disponibles]
    indice = entrada.elegir(opciones, "Elegí la evaluación: ")
    if indice is None:
        return False
    nota = entrada.validar_nota()
    gestion.registrar_nota(datos, legajo, inscripcion["materia"], inscripcion["anio"],
                           inscripcion["periodo"], disponibles[indice], nota, modificar=modificar)
    return True


def agregar_notas(datos):
    return editar_nota(datos)


def modificar_nota(datos):
    return editar_nota(datos, modificar=True)


def mostrar_notas_alumno(datos):
    legajo = seleccionar_alumno(datos)
    if legajo is not None:
        print("\n" + gestion.informe_alumno(datos, legajo))
    return False


def listar_alumnos(datos):
    if not datos["alumnos"]:
        print("No hay alumnos cargados.")
    for legajo, alumno in sorted(datos["alumnos"].items(), key=lambda par: int(par[0])):
        print(etiqueta_alumno(legajo, alumno))
    return False


def agregar_materia(datos):
    nombre = entrada.leer("Nombre de la nueva materia: ")
    gestion.alta_materia(datos, nombre)
    print("La materia se asigna a cada alumno desde la opción 8.")
    return True


# Diccionario de funciones: relaciona las opciones del menú con sus acciones.
ACCIONES = {
    1: agregar_persona, 2: agregar_notas, 3: modificar_nota,
    4: mostrar_notas_alumno, 5: eliminar_alumno, 6: modificar_persona,
    7: mostrar_notas_alumno, 8: inscribir_alumno, 9: quitar_materia,
    10: agregar_materia, 11: listar_alumnos,
}

