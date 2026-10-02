"""Pruebas con assert (clase 08). Solo se importan módulos del proyecto.

Ejecutar desde la carpeta del programa: python pruebas.py
Se usan exclusivamente archivos que comienzan con prueba_.
"""

import archivos
import gestion


def comprobar(condicion, mensaje):
    assert condicion, mensaje
    print("OK:", mensaje)


def comprobar_error(operacion, mensaje):
    rechazado = False
    try:
        operacion()
    except ValueError:
        rechazado = True
    comprobar(rechazado, mensaje)


def contar(ruta):
    cantidad = 0
    archivo = None
    try:
        archivo = open(ruta, "rt", encoding="utf-8")
        for linea in archivo:
            cantidad += 1
    finally:
        if archivo is not None:
            archivo.close()
    return cantidad


def ejecutar():
    config = gestion.configuracion("prueba_")
    gestion.crear_demostracion(config)
    periodo = config["periodos"][0]
    comprobar(contar(config["alumnos"]) == 15, "15 alumnos de ejemplo")
    comprobar(contar(config["materias"]) == 11, "11 materias de ejemplo")
    comprobar(contar(config["cursadas"]) == 45, "Tres inscripciones por alumno de ejemplo")
    comprobar(config["evaluaciones"] == ("Parcial 1", "Parcial 2", "Final"), "Dos parciales y un final")
    alumno = gestion.obtener_alumno(config, "1")
    comprobar(gestion.coincide_alumno(alumno, "matias lopez"), "Búsqueda sin tildes")
    comprobar(gestion.coincide_alumno(alumno, "LOPEZ"), "Búsqueda sin distinguir mayúsculas")
    comprobar(gestion.coincide_alumno(alumno, "90.000.001"), "Búsqueda por DNI con puntos")
    comprobar(gestion.coincide_alumno(alumno, "#1"), "Búsqueda por legajo")
    comprobar(not gestion.coincide_alumno(alumno, ""), "La búsqueda vacía no muestra todo")
    comprobar_error(lambda: gestion.alta_alumno(config, "Otro", "Alumno", "90000001"), "Rechazo de DNI duplicado")
    legajo = gestion.alta_alumno(config, "Ana María", "O'Connor-López", "12.345.678", "ana@example.com", "+54 11 1234-5678")
    comprobar(legajo == "16", "Legajo automático")
    comprobar(gestion.obtener_alumno(config, legajo)["telefono"] == "+54 11 1234-5678", "Datos de contacto guardados")
    otro = gestion.alta_alumno(config, "Ana María", "O'Connor-López", "23456789")
    comprobar(otro != legajo, "Permite homónimos con DNI distintos")
    for dni in ("123", "abcdefg", "123456789"):
        comprobar_error(lambda: gestion.alta_alumno(config, "Luis", "Pérez", dni), "DNI inválido: " + dni)
    comprobar_error(lambda: gestion.alta_alumno(config, "123", "Pérez", "34567890"), "Nombre inválido")
    comprobar_error(lambda: gestion.alta_alumno(config, "Luis", "Pérez", "34567890", "sin-correo"), "Correo inválido")
    comprobar_error(lambda: gestion.alta_alumno(config, "Luis", "Pérez", "34567890", "", "abc"), "Teléfono inválido")
    gestion.inscribir(config, legajo, "1", 2026, periodo)
    comprobar_error(lambda: gestion.inscribir(config, legajo, "1", 2026, periodo), "No duplica inscripciones")
    comprobar_error(lambda: gestion.registrar_nota(config, otro, "1", 2026, periodo, "Parcial 1", 8), "Solo carga notas en materias asignadas")
    comprobar_error(lambda: gestion.inscribir(config, legajo, "999", 2026, periodo), "Rechaza materias inexistentes")
    comprobar_error(lambda: gestion.inscribir(config, legajo, "1", 0, periodo), "Rechaza años inválidos")
    comprobar_error(lambda: gestion.inscribir(config, legajo, "1", 2026, "Inválido"), "Rechaza períodos inválidos")
    gestion.inscribir(config, legajo, "1", 2026, config["periodos"][1])
    gestion.inscribir(config, legajo, "1", 2027, periodo)
    gestion.registrar_nota(config, legajo, "1", 2026, periodo, "Parcial 1", "8,5")
    fila = gestion.obtener_cursada(config, legajo, "1", 2026, periodo)
    comprobar(gestion.notas_de_cursada(config, fila) == {"Parcial 1": 8.5}, "Notas en un diccionario")
    comprobar(gestion.obtener_cursada(config, legajo, "1", 2027, periodo)[4] == "", "Notas separadas por año")
    comprobar(gestion.obtener_cursada(config, legajo, "1", 2026, config["periodos"][1])[4] == "", "Notas separadas por período")
    comprobar_error(lambda: gestion.registrar_nota(config, legajo, "1", 2026, periodo, "Parcial 1", 9), "No duplica una evaluación")
    comprobar_error(lambda: gestion.registrar_nota(config, legajo, "1", 2026, periodo, "Parcial 3", 9), "No permite una cuarta evaluación")
    for nota in ("abc", "nan", "inf", "0", "11"):
        comprobar_error(lambda: gestion.validar_nota(nota), "Nota inválida: " + nota)
    gestion.registrar_nota(config, legajo, "1", 2026, periodo, "Parcial 1", 9, modificar=True)
    comprobar(gestion.obtener_cursada(config, legajo, "1", 2026, periodo)[4] == "9.0", "Modificación de nota")
    comprobar_error(lambda: gestion.registrar_nota(config, legajo, "1", 2026, periodo, "Final", 6, modificar=True), "No modifica evaluaciones vacías")
    gestion.registrar_nota(config, legajo, "1", 2026, periodo, "Parcial 2", 7)
    gestion.registrar_nota(config, legajo, "1", 2026, periodo, "Final", 8)
    comprobar(len(gestion.notas_de_cursada(config, gestion.obtener_cursada(config, legajo, "1", 2026, periodo))) == 3, "Máximo de tres notas")
    gestion.modificar_alumno(config, legajo, "Ana", "Pérez", "12345678")
    comprobar(gestion.obtener_alumno(config, legajo)["apellido"] == "Pérez", "Modificación de alumno")
    comprobar(gestion.obtener_cursada(config, legajo, "1", 2026, periodo)[4] == "9.0", "Editar ficha conserva las notas")
    comprobar_error(lambda: gestion.modificar_alumno(config, legajo, "Ana", "Pérez", "23456789"), "Editar DNI no admite duplicados")
    comprobar_error(lambda: gestion.quitar_inscripcion(config, legajo, "1", 2026, periodo), "Protege inscripciones con notas")
    gestion.quitar_inscripcion(config, legajo, "1", 2027, periodo)
    comprobar_error(lambda: gestion.obtener_cursada(config, legajo, "1", 2027, periodo), "Quita inscripciones sin notas")
    comprobar_error(lambda: gestion.alta_materia(config, "  MATEMATICA "), "No duplica materias por mayúsculas o tildes")
    codigo = gestion.alta_materia(config, "Programación 1")
    comprobar(gestion.obtener_materia(config, codigo) == "Programación 1", "Alta de materia")
    comprobar(gestion.formatear_nota("8.5") == "8,5", "Formato de notas sin corchetes")
    gestion.eliminar_alumno(config, legajo)
    comprobar_error(lambda: gestion.obtener_alumno(config, legajo), "Baja de alumno")
    comprobar_error(lambda: gestion.obtener_cursada(config, legajo, "1", 2026, periodo), "La baja oculta sus notas")
    comprobar(gestion.obtener_materia(config, "1") == "Matemática", "La baja no borra materias")
    comprobar(gestion.obtener_alumno(config, "1")["nombre"] == "Matías", "La baja no afecta a otros alumnos")
    gestion.preparar_archivos(config)
    comprobar_error(lambda: gestion.obtener_alumno(config, legajo), "Reiniciar no repone alumnos eliminados")
    nuevo = gestion.alta_alumno(config, "Nuevo", "Alumno", "12345678")
    comprobar(nuevo == "18", "No reutiliza legajos al eliminar")
    comprobar(archivos.existe(config["alumnos"] + ".bak"), "Conserva copia previa al guardar")
    print("\nTodas las comprobaciones finalizaron correctamente.")


# Programa de pruebas.
ejecutar()
