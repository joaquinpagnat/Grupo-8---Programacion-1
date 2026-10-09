"""Menús del proyecto. Se conserva el nombre original del archivo."""

import archivos
import gestion
import Funciones_Reps as entrada


def menu():
    opciones = (
        "Alta de alumno", "Agregar nota", "Modificar nota", "Ver notas de un alumno",
        "Eliminar alumno", "Modificar datos de un alumno", "Buscar alumno y ver su ficha",
        "Inscribir alumno en una materia", "Quitar inscripción sin notas",
        "Agregar materia al catálogo", "Listar alumnos", "Salir",
    )
    print("\nGESTIÓN DE ALUMNOS Y NOTAS")
    print("-" * 55)
    for i in range(len(opciones)):
        print(f"{i + 1} - {opciones[i]}")
    print("-" * 55)
    print("/cancelar o Ctrl+C vuelve al menú durante una operación.")
    return entrada.validar_opcion("Elegí una opción: ", 1, len(opciones))


def etiqueta_alumno(ficha):
    return f"Legajo {ficha['legajo']} | {ficha['apellido']}, {ficha['nombre']} | DNI {ficha['dni']}"


def seleccionar_alumno(config):
    consulta = entrada.leer("Buscar por nombre, apellido, DNI o #legajo (Enter para volver): ")
    seleccionado = None
    archivo = None
    if consulta != "":
        try:
            archivo = open(config["alumnos"], "rt", encoding="utf-8")
            cantidad = 0
            for linea in archivo:
                ficha = gestion.ficha_desde_fila(archivos.separar(linea, 7))
                if gestion.coincide_alumno(ficha, consulta):
                    print(etiqueta_alumno(ficha))
                    cantidad += 1
            if cantidad == 0:
                print("No se encontraron alumnos. Podés volver a buscar desde el menú.")
            else:
                legajo = entrada.leer("Escribí el legajo de un resultado (Enter para volver): ")
                if legajo != "":
                    fila = archivos.buscar_en_archivo(archivo, 7, (legajo,))
                    if fila is not None and gestion.coincide_alumno(gestion.ficha_desde_fila(fila), consulta):
                        seleccionado = legajo
                    else:
                        print("Ese legajo no pertenece a los resultados mostrados.")
        except:
            archivos.cerrar([archivo])
            raise
        archivos.cerrar([archivo])
    return seleccionado


def leer_ficha(actual=None):
    ficha = {}
    campos = (("nombre", "Nombre"), ("apellido", "Apellido"), ("dni", "DNI"),
              ("email", "Correo (opcional)"), ("telefono", "Teléfono (opcional)"))
    if actual is not None:
        print("Enter conserva un dato. Un guion borra el correo o el teléfono.")
    for clave, titulo in campos:
        mensaje = titulo + ": "
        if actual is not None:
            mensaje = titulo + " (actual: " + (actual[clave] or "Sin informar") + "): "
        valor = entrada.leer(mensaje)
        if actual is not None and valor == "":
            valor = actual[clave]
        if clave in ("email", "telefono") and valor == "-":
            valor = ""
        ficha[clave] = valor
    return ficha


def agregar_persona(config):
    ficha = leer_ficha()
    legajo = gestion.alta_alumno(config, ficha["nombre"], ficha["apellido"], ficha["dni"],
                                ficha["email"], ficha["telefono"])
    print(f"Legajo asignado: {legajo}. Asigná las materias con la opción 8.")


def modificar_persona(config):
    legajo = seleccionar_alumno(config)
    if legajo is not None:
        ficha = leer_ficha(gestion.obtener_alumno(config, legajo))
        gestion.modificar_alumno(config, legajo, ficha["nombre"], ficha["apellido"],
                                 ficha["dni"], ficha["email"], ficha["telefono"])
        print("Cambios guardados correctamente.")


def eliminar_alumno(config):
    legajo = seleccionar_alumno(config)
    if legajo is not None:
        print("El alumno dejará de aparecer en las búsquedas y sus notas quedarán fuera del uso normal.")
        if entrada.confirmar("¿Confirmás la baja de este alumno?"):
            gestion.eliminar_alumno(config, legajo)
            print("Cambios guardados correctamente.")


def seleccionar_materia(config):
    elegido = None
    archivo = None
    try:
        archivo = open(config["materias"], "rt", encoding="utf-8")
        print("\nCATÁLOGO DE MATERIAS")
        for linea in archivo:
            codigo, nombre = archivos.separar(linea, 2)
            print(f"{codigo} - {nombre}")
        while True:
            codigo = entrada.leer("Código de materia (0 o Enter para volver): ")
            if codigo in ("0", ""):
                break
            fila = archivos.buscar_en_archivo(archivo, 2, (codigo,))
            if fila is not None:
                elegido = codigo
                break
            print("No existe una materia con ese código.")
    except:
        archivos.cerrar([archivo])
        raise
    archivos.cerrar([archivo])
    return elegido


def inscribir_alumno(config):
    legajo = seleccionar_alumno(config)
    if legajo is not None:
        materia = seleccionar_materia(config)
        if materia is not None:
            anio = entrada.validar_opcion("Año de cursada (por ejemplo 2026): ", 1900, 2100)
            periodo = entrada.elegir(config["periodos"], "Elegí el período: ")
            if periodo is not None:
                gestion.inscribir(config, legajo, materia, anio, config["periodos"][periodo])
                print("Cambios guardados correctamente.")


def seleccionar_cursada(config, legajo):
    seleccionada = None
    cursadas = None
    materias = None
    try:
        cursadas = open(config["cursadas"], "rt", encoding="utf-8")
        materias = open(config["materias"], "rt", encoding="utf-8")
        cantidad = 0
        for linea in cursadas:
            fila = archivos.separar(linea, 7)
            if fila[0] == legajo:
                materia = archivos.buscar_en_archivo(materias, 2, (fila[1],))
                if materia is None:
                    raise ValueError("Una inscripción hace referencia a una materia inexistente.")
                cantidad += 1
                print(f"{cantidad} - {materia[1]} | {fila[2]} | {fila[3]}")
        if cantidad == 0:
            print("El alumno no tiene materias asignadas. Usá la opción 8.")
        else:
            print("0 - Volver")
            numero = entrada.validar_opcion("Elegí la materia y su período: ", 0, cantidad)
            if numero != 0:
                cursadas.seek(0)
                contador = 0
                for linea in cursadas:
                    fila = archivos.separar(linea, 7)
                    if fila[0] == legajo:
                        contador += 1
                        if contador == numero:
                            seleccionada = fila
                            break
    except:
        archivos.cerrar([materias, cursadas])
        raise
    archivos.cerrar([materias, cursadas])
    return seleccionada


def quitar_materia(config):
    legajo = seleccionar_alumno(config)
    if legajo is not None:
        fila = seleccionar_cursada(config, legajo)
        if fila is not None:
            if fila[4:] != ["", "", ""]:
                print("No se puede quitar una inscripción que ya tiene notas.")
            elif entrada.confirmar("¿Quitás esta inscripción?"):
                gestion.quitar_inscripcion(config, legajo, fila[1], fila[2], fila[3])
                print("Cambios guardados correctamente.")


def editar_nota(config, modificar=False):
    legajo = seleccionar_alumno(config)
    if legajo is not None:
        fila = seleccionar_cursada(config, legajo)
        if fila is not None:
            notas = gestion.notas_de_cursada(config, fila)
            disponibles = []
            etiquetas = []
            for evaluacion in config["evaluaciones"]:
                if (evaluacion in notas) == modificar:
                    disponibles.append(evaluacion)
                    etiqueta = evaluacion
                    if modificar:
                        etiqueta += " (actual: " + gestion.formatear_nota(notas[evaluacion]) + ")"
                    etiquetas.append(etiqueta)
            if len(disponibles) == 0:
                if modificar:
                    print("Esta cursada todavía no tiene notas para modificar.")
                else:
                    print("Ya están cargadas las tres evaluaciones. Usá Modificar nota.")
            else:
                print("Se permite una nota para Parcial 1, una para Parcial 2 y una para Final.")
                if not modificar and len(notas) > 0:
                    print("Las evaluaciones ya cargadas se corrigen con Modificar nota.")
                indice = entrada.elegir(etiquetas, "Elegí la evaluación: ")
                if indice is not None:
                    nota = entrada.leer_nota()
                    gestion.registrar_nota(config, legajo, fila[1], fila[2], fila[3],
                                           disponibles[indice], nota, modificar)
                    print("Cambios guardados correctamente.")


def mostrar_notas_alumno(config):
    legajo = seleccionar_alumno(config)
    if legajo is not None:
        ficha = gestion.obtener_alumno(config, legajo)
        print("\n" + etiqueta_alumno(ficha))
        print("Correo:", ficha["email"] or "Sin informar")
        print("Teléfono:", ficha["telefono"] or "Sin informar")
        cursadas = None
        materias = None
        cantidad = 0
        try:
            cursadas = open(config["cursadas"], "rt", encoding="utf-8")
            materias = open(config["materias"], "rt", encoding="utf-8")
            for linea in cursadas:
                fila = archivos.separar(linea, 7)
                if fila[0] == legajo:
                    cantidad += 1
                    materia = archivos.buscar_en_archivo(materias, 2, (fila[1],))
                    if materia is None:
                        raise ValueError("Una inscripción tiene una materia inexistente.")
                    print(f"\n{materia[1]} | {fila[2]} | {fila[3]}")
                    notas = gestion.notas_de_cursada(config, fila)
                    if len(notas) == 0:
                        print("  Sin notas cargadas.")
                    for evaluacion in config["evaluaciones"]:
                        if evaluacion in notas:
                            print("  " + evaluacion + ": " + gestion.formatear_nota(notas[evaluacion]))
        except:
            archivos.cerrar([materias, cursadas])
            raise
        archivos.cerrar([materias, cursadas])
        if cantidad == 0:
            print("Sin materias asignadas. Usá la opción 8 para inscribir al alumno.")


def listar_alumnos(config):
    archivo = None
    cantidad = 0
    try:
        archivo = open(config["alumnos"], "rt", encoding="utf-8")
        for linea in archivo:
            ficha = gestion.ficha_desde_fila(archivos.separar(linea, 7))
            if ficha["activo"] == "1":
                print(etiqueta_alumno(ficha))
                cantidad += 1
    except:
        archivos.cerrar([archivo])
        raise
    archivos.cerrar([archivo])
    print(f"Total de alumnos activos: {cantidad}.")


def agregar_materia(config):
    codigo = gestion.alta_materia(config, entrada.leer("Nombre de la nueva materia: "))
    print(f"Materia creada con código {codigo}. Asignala desde la opción 8.")
