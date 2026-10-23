import archivos
import gestion
import Funciones_Reps as entrada


def crear_matriz(filas, columnas):
    """Crea una matriz de filas x columnas inicializada en cero por comprensión."""
    matriz = [[0] * columnas for f in range(filas)]
    return matriz


def imprimir_matriz_resumen(config, matriz):
    """Imprime la matriz de cantidad de evaluaciones rendidas por período."""
    filas = len(matriz)
    columnas = len(matriz[0])
    print("\nMATRIZ DE EVALUACIONES RENDIDAS POR PERÍODO")
    encabezado = f"{'Período':<20}"
    for c in range(columnas):
        encabezado = encabezado + f"{config['evaluaciones'][c]:>12}"
    print(encabezado)
    print("-" * len(encabezado))
    for f in range(filas):
        print(f"{config['periodos'][f]:<20}", end="")
        for c in range(columnas):
            print("%12d" % matriz[f][c], end="")
        print()


def menu():
    """Muestra el menú principal y devuelve la opción seleccionada."""
    opciones = (
        "Alta de alumno",
        "Agregar nota",
        "Modificar nota",
        "Ver notas de un alumno",
        "Eliminar alumno",
        "Modificar datos de un alumno",
        "Buscar alumno y ver su ficha",
        "Inscribir alumno en una materia",
        "Quitar inscripción sin notas",
        "Agregar materia al catálogo",
        "Listar alumnos",
        "Salir",
    )
    print("\nGESTIÓN DE ALUMNOS Y NOTAS")
    print("-" * 50)
    for i, opcion in enumerate(opciones):
        print(f"{i + 1} - {opcion}")
    print("-" * 50)
    return entrada.validar_opcion("Elegí una opción: ", 1, len(opciones))


def etiqueta_alumno(ficha):
    """Formatea una línea con los datos principales de un alumno."""
    return f"Legajo {ficha['legajo']} | {ficha['apellido']}, {ficha['nombre']} | DNI {ficha['dni']}"


def seleccionar_alumno(config):
    """Busca alumnos activos en el archivo y devuelve el legajo seleccionado."""
    seleccionado = None
    try:
        arch = open(config["alumnos"], "rt", encoding="UTF8")
        hay_alumnos = False
        for linea in arch:
            if archivos.separar(linea, 7)[1] == "1":
                hay_alumnos = True
        if not hay_alumnos:
            print("No hay alumnos cargados. Primero usá Alta de alumno.")
        while hay_alumnos:
            consulta = entrada.leer("Buscar por nombre, apellido, DNI o #legajo (Enter para volver): ")
            if consulta == "":
                break
            coincidencias = 0
            arch.seek(0)
            for linea in arch:
                ficha = gestion.ficha_desde_fila(archivos.separar(linea, 7))
                if gestion.coincide_alumno(ficha, consulta):
                    print(etiqueta_alumno(ficha))
                    coincidencias = coincidencias + 1
            if coincidencias == 0:
                print("No se encontraron alumnos. Probá otra búsqueda.")
            else:
                legajo = entrada.leer("Escribí el legajo de un resultado (Enter para volver): ")
                if legajo == "":
                    break
                fila = archivos.buscar_en_archivo(arch, 7, (0,), (legajo,))
                if fila is not None and gestion.coincide_alumno(gestion.ficha_desde_fila(fila), consulta):
                    seleccionado = legajo
                    break
                print("Ese legajo no pertenece a los resultados mostrados.")
    finally:
        try:
            arch.close()
        except NameError:
            pass
    return seleccionado


def leer_ficha(actual=None):
    """Solicita por teclado los datos personales de un alumno."""
    ficha = {}
    campos = (
        ("nombre", "Nombre"),
        ("apellido", "Apellido"),
        ("dni", "DNI"),
        ("email", "Correo (opcional)"),
        ("telefono", "Teléfono (opcional)"),
    )
    if actual is not None:
        print("Enter conserva un dato. Un guion borra el correo o el teléfono.")
    for clave, titulo in campos:
        mensaje = titulo + ": "
        if actual is not None:
            actual_txt = actual[clave] if actual[clave] != "" else "Sin informar"
            mensaje = f"{titulo} (actual: {actual_txt}): "
        valor = entrada.leer(mensaje)
        if actual is not None and valor == "":
            valor = actual[clave]
        if clave in ("email", "telefono") and valor == "-":
            valor = ""
        ficha[clave] = valor
    return ficha


def agregar_persona(config):
    """Da de alta un nuevo alumno pidiendo sus datos por teclado."""
    ficha = leer_ficha()
    legajo = gestion.alta_alumno(
        config, ficha["nombre"], ficha["apellido"], ficha["dni"], ficha["email"], ficha["telefono"]
    )
    print(f"Legajo asignado: {legajo}. Asigná las materias con la opción 8.")
    return True


def modificar_persona(config):
    """Permite seleccionar un alumno y modificar sus datos personales."""
    cambiado = False
    legajo = seleccionar_alumno(config)
    if legajo is not None:
        ficha = leer_ficha(gestion.obtener_alumno(config, legajo))
        gestion.modificar_alumno(
            config, legajo, ficha["nombre"], ficha["apellido"], ficha["dni"], ficha["email"], ficha["telefono"]
        )
        cambiado = True
    return cambiado


def eliminar_alumno(config):
    """Selecciona un alumno y solicita confirmación para su baja lógica."""
    cambiado = False
    legajo = seleccionar_alumno(config)
    if legajo is not None:
        if entrada.confirmar("¿Confirmás la baja de este alumno?"):
            gestion.eliminar_alumno(config, legajo)
            cambiado = True
    return cambiado


def seleccionar_materia(config):
    """Muestra el catálogo de materias desde el archivo y devuelve el código elegido."""
    elegido = None
    try:
        arch = open(config["materias"], "rt", encoding="UTF8")
        print("\nCATÁLOGO DE MATERIAS")
        for linea in arch:
            codigo, nombre = archivos.separar(linea, 2)
            print(f"{codigo} - {nombre}")
        while True:
            codigo = entrada.leer("Código de materia (0 o Enter para volver): ")
            if codigo in ("0", ""):
                break
            fila = archivos.buscar_en_archivo(arch, 2, (0,), (codigo,))
            if fila is not None:
                elegido = codigo
                break
            print("No existe una materia con ese código.")
    finally:
        try:
            arch.close()
        except NameError:
            pass
    return elegido


def inscribir_alumno(config):
    """Inscribe a un alumno seleccionado en una materia, año y período."""
    cambiado = False
    legajo = seleccionar_alumno(config)
    if legajo is not None:
        materia = seleccionar_materia(config)
        if materia is not None:
            anio = entrada.validar_opcion("Año de cursada (por ejemplo 2026): ", 1900, 2100)
            periodo = entrada.elegir(config["periodos"], "Elegí el período: ")
            if periodo is not None:
                gestion.inscribir(config, legajo, materia, anio, config["periodos"][periodo])
                cambiado = True
    return cambiado


def seleccionar_cursada(config, legajo):
    """Muestra las cursadas de un alumno y devuelve el registro seleccionado."""
    seleccionada = None
    try:
        cursadas = open(config["cursadas"], "rt", encoding="UTF8")
        materias = open(config["materias"], "rt", encoding="UTF8")
        cantidad = 0
        for linea in cursadas:
            fila = archivos.separar(linea, 7)
            if fila[0] == legajo:
                materia = archivos.buscar_en_archivo(materias, 2, (0,), (fila[1],))
                if materia is None:
                    raise ValueError("Una inscripción hace referencia a una materia inexistente.")
                cantidad = cantidad + 1
                print(f"{cantidad} - {materia[1]} | {fila[2]} | {fila[3]}")
        if cantidad == 0:
            print("El alumno no tiene materias asignadas. Usá la opción 8.")
        else:
            print("0 - Volver")
            numero = entrada.validar_opcion("Elegí la materia y su período: ", 0, cantidad)
            if numero != 0:
                cursadas.seek(0)
                contador = 0
                linea = cursadas.readline()
                while linea != "" and seleccionada is None:
                    fila = archivos.separar(linea, 7)
                    if fila[0] == legajo:
                        contador = contador + 1
                        if contador == numero:
                            seleccionada = fila
                    linea = cursadas.readline()
    finally:
        try:
            cursadas.close()
        except NameError:
            pass
        try:
            materias.close()
        except NameError:
            pass
    return seleccionada


def quitar_materia(config):
    """Elimina una inscripción sin notas de un alumno seleccionado."""
    cambiado = False
    legajo = seleccionar_alumno(config)
    if legajo is not None:
        fila = seleccionar_cursada(config, legajo)
        if fila is not None:
            if fila[4:] != ["", "", ""]:
                print("No se puede quitar una inscripción que ya tiene notas.")
            elif entrada.confirmar("¿Quitás esta inscripción?"):
                gestion.quitar_inscripcion(config, legajo, fila[1], fila[2], fila[3])
                cambiado = True
    return cambiado


def editar_nota(config, modificar=False):
    """Carga una nueva nota o modifica una existente en una cursada."""
    cambiado = False
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
                        etiqueta = etiqueta + f" (actual: {gestion.formatear_nota(notas[evaluacion])})"
                    etiquetas.append(etiqueta)
            if len(disponibles) == 0:
                if modificar:
                    print("Esta cursada todavía no tiene notas para modificar.")
                else:
                    print("Ya están cargadas las tres evaluaciones. Usá Modificar nota.")
            else:
                indice = entrada.elegir(etiquetas, "Elegí la evaluación: ")
                if indice is not None:
                    nota = entrada.leer_nota()
                    gestion.registrar_nota(
                        config, legajo, fila[1], fila[2], fila[3], disponibles[indice], nota, modificar
                    )
                    cambiado = True
    return cambiado


def mostrar_notas_alumno(config):
    """Muestra la ficha de un alumno, sus notas, promedios recursivos y matriz resumen."""
    legajo = seleccionar_alumno(config)
    if legajo is not None:
        ficha = gestion.obtener_alumno(config, legajo)
        print("\n" + etiqueta_alumno(ficha))
        print("Correo:", ficha["email"] or "Sin informar")
        print("Teléfono:", ficha["telefono"] or "Sin informar")
        matriz = crear_matriz(len(config["periodos"]), len(config["evaluaciones"]))
        cantidad = 0
        try:
            cursadas = open(config["cursadas"], "rt", encoding="UTF8")
            materias = open(config["materias"], "rt", encoding="UTF8")
            for linea in cursadas:
                fila = archivos.separar(linea, 7)
                if fila[0] == legajo:
                    cantidad = cantidad + 1
                    materia = archivos.buscar_en_archivo(materias, 2, (0,), (fila[1],))
                    if materia is None:
                        raise ValueError("Una inscripción tiene una materia inexistente.")
                    print(f"\n{materia[1]} | {fila[2]} | {fila[3]}")
                    notas = gestion.notas_de_cursada(config, fila)
                    if len(notas) == 0:
                        print("  Sin notas cargadas.")
                    else:
                        f_per = config["periodos"].index(fila[3])
                        for c_ev, evaluacion in enumerate(config["evaluaciones"]):
                            if evaluacion in notas:
                                print(f"  {evaluacion}: {gestion.formatear_nota(notas[evaluacion])}")
                                matriz[f_per][c_ev] = matriz[f_per][c_ev] + 1
                        lista_valores = list(notas.values())
                        promedio = gestion.calcular_promedio(lista_valores)
                        print(f"  Promedio: {gestion.formatear_nota(promedio)}")
        finally:
            try:
                cursadas.close()
            except NameError:
                pass
            try:
                materias.close()
            except NameError:
                pass
        if cantidad == 0:
            print("Sin materias asignadas. Usá la opción 8 para inscribir al alumno.")
        else:
            imprimir_matriz_resumen(config, matriz)
    return False


def listar_alumnos(config):
    """Recorre el archivo de alumnos e imprime todos los que se encuentran activos."""
    cantidad = 0
    try:
        arch = open(config["alumnos"], "rt", encoding="UTF8")
        for linea in arch:
            ficha = gestion.ficha_desde_fila(archivos.separar(linea, 7))
            if ficha["activo"] == "1":
                print(etiqueta_alumno(ficha))
                cantidad = cantidad + 1
    finally:
        try:
            arch.close()
        except NameError:
            pass
    print(f"Total de alumnos activos: {cantidad}.")
    return False


def agregar_materia(config):
    """Solicita el nombre de una materia nueva y la registra en el catálogo."""
    codigo = gestion.alta_materia(config, entrada.leer("Nombre de la nueva materia: "))
    print(f"Materia creada con código {codigo}. Asignala desde la opción 8.")
    return True


def ejecutar_opcion(config, opcion):
    """Ejecuta la función correspondiente a la opción elegida del menú."""
    cambiado = False
    if opcion == 1:
        cambiado = agregar_persona(config)
    elif opcion == 2:
        cambiado = editar_nota(config)
    elif opcion == 3:
        cambiado = editar_nota(config, modificar=True)
    elif opcion == 4 or opcion == 7:
        mostrar_notas_alumno(config)
    elif opcion == 5:
        cambiado = eliminar_alumno(config)
    elif opcion == 6:
        cambiado = modificar_persona(config)
    elif opcion == 8:
        cambiado = inscribir_alumno(config)
    elif opcion == 9:
        cambiado = quitar_materia(config)
    elif opcion == 10:
        cambiado = agregar_materia(config)
    elif opcion == 11:
        listar_alumnos(config)
    return cambiado


