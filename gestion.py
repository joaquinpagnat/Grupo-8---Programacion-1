"""Reglas del programa. Solo se importa el módulo propio archivos."""

import archivos


def configuracion(prefijo=""):
    # Diccionario de configuración y tuplas de opciones fijas (clase 07).
    return {
        "alumnos": prefijo + "alumnos.txt",
        "materias": prefijo + "materias.txt",
        "cursadas": prefijo + "cursadas.txt",
        "anterior": prefijo + "datos.json",
        "periodos": ("1.er cuatrimestre", "2.º cuatrimestre", "Anual"),
        "evaluaciones": ("Parcial 1", "Parcial 2", "Final"),
        "anio_demo": 2026,
    }


def preparar_archivos(config):
    presentes = 0
    for nombre in ("alumnos", "materias", "cursadas"):
        if archivos.existe(config[nombre]):
            presentes += 1
    if presentes == 0:
        if archivos.existe(config["anterior"]):
            raise ValueError("Hay un datos.json de la versión anterior. Conservá ese archivo para migrar sus datos; no se reemplazó por ejemplos.")
        crear_demostracion(config)
    elif presentes != 3:
        raise ValueError("Falta uno de los archivos de datos. Restaurá alumnos.txt, materias.txt y cursadas.txt de la misma copia.")


def crear_demostracion(config):
    nombres = (
        ("Matías", "López"), ("Carlos", "Gómez"), ("Daniela", "Fernández"),
        ("Juan", "Pérez"), ("Sofía", "Rodríguez"), ("Lucía", "González"),
        ("Pedro", "Martínez"), ("Florencia", "Sánchez"), ("Valentina", "Romero"),
        ("Diego", "Díaz"), ("Martina", "Álvarez"), ("Alejandro", "Ruiz"),
        ("Camila", "Alonso"), ("Gabriel", "Torres"), ("Julieta", "Silva"),
    )
    materias = ("Matemática", "Literatura", "Electrotecnia", "Inglés", "Física",
                "Química", "Historia", "Geografía", "Biología", "Informática", "Educación Física")
    # Estas listas se construyen con datos de ejemplo, no cargando un archivo.
    alumnos = []
    catalogo = []
    cursadas = []
    for i in range(len(materias)):
        catalogo.append([str(i + 1), materias[i]])
    for i in range(len(nombres)):
        legajo = str(i + 1)
        nombre, apellido = nombres[i]
        alumnos.append([legajo, "1", nombre, apellido, str(90000001 + i),
                        "alumno" + legajo + "@example.com", ""])
        for posicion, desplazamiento in enumerate((0, 3, 6)):
            materia = str((i + desplazamiento) % len(materias) + 1)
            periodo = config["periodos"][0] if posicion < 2 else config["periodos"][1]
            cursadas.append([legajo, materia, str(config["anio_demo"]), periodo, "", "", ""])
    archivos.crear(config["materias"], catalogo)
    archivos.crear(config["alumnos"], alumnos)
    archivos.crear(config["cursadas"], cursadas)


def normalizar(texto):
    """Ignora mayúsculas y tildes con el procedimiento de las clases 05 y 06."""
    con_tilde = "áéíóúü"
    sin_tilde = "aeiouu"
    resultado = ""
    for caracter in texto.lower():
        if caracter in con_tilde:
            resultado += sin_tilde[con_tilde.index(caracter)]
        else:
            resultado += caracter
    return " ".join(resultado.split())


def solo_digitos(texto):
    valido = texto != ""
    for caracter in texto:
        if caracter not in "0123456789":
            valido = False
    return valido


def validar_nombre(texto, campo):
    texto = " ".join(texto.split())
    hay_letras = False
    if len(texto) < 1 or len(texto) > 80:
        raise ValueError(campo + ": ingresá entre 1 y 80 caracteres.")
    for caracter in texto:
        if caracter.isalpha():
            hay_letras = True
        elif caracter not in " '-’":
            raise ValueError(campo + ": usá letras, espacios, apóstrofes o guiones.")
    if not hay_letras:
        raise ValueError(campo + ": debe contener letras.")
    return texto


def validar_ficha(nombre, apellido, dni, email="", telefono=""):
    nombre = validar_nombre(nombre, "Nombre")
    apellido = validar_nombre(apellido, "Apellido")
    dni = dni.strip().replace(".", "").replace(" ", "")
    if not solo_digitos(dni) or len(dni) not in (7, 8):
        raise ValueError("El DNI debe tener 7 u 8 dígitos.")
    email = email.strip()
    if email != "":
        if len(email) > 254 or email.count("@") != 1:
            raise ValueError("Correo inválido. Ejemplo: nombre@dominio.com.")
        usuario, dominio = email.split("@")
        if usuario == "" or "." not in dominio or dominio[0] == "." or dominio[-1] == ".":
            raise ValueError("Correo inválido. Ejemplo: nombre@dominio.com.")
        for caracter in email:
            if caracter in " ;\t\r\n":
                raise ValueError("El correo no puede contener espacios ni punto y coma.")
    telefono = telefono.strip()
    if telefono != "":
        digitos = 0
        for i, caracter in enumerate(telefono):
            if caracter in "0123456789":
                digitos += 1
            elif caracter == "+" and i == 0:
                pass
            elif caracter not in "() -":
                raise ValueError("El teléfono contiene un carácter inválido.")
        if not 6 <= digitos <= 15 or len(telefono) > 25:
            raise ValueError("El teléfono debe tener entre 6 y 15 dígitos.")
    return {"nombre": nombre, "apellido": apellido, "dni": dni,
            "email": email, "telefono": telefono}


def ficha_desde_fila(fila):
    return {"legajo": fila[0], "activo": fila[1], "nombre": fila[2],
            "apellido": fila[3], "dni": fila[4], "email": fila[5], "telefono": fila[6]}


def fila_desde_ficha(ficha):
    return [ficha["legajo"], ficha["activo"], ficha["nombre"], ficha["apellido"],
            ficha["dni"], ficha["email"], ficha["telefono"]]


def obtener_alumno(config, legajo):
    fila = archivos.buscar(config["alumnos"], 7, (0,), (str(legajo),))
    if fila is None or fila[1] != "1":
        raise ValueError("No existe un alumno activo con ese legajo.")
    return ficha_desde_fila(fila)


def verificar_dni(config, dni, excluir=""):
    archivo = None
    try:
        archivo = open(config["alumnos"], "rt", encoding="utf-8")
        for linea in archivo:
            fila = archivos.separar(linea, 7)
            if fila[1] == "1" and fila[0] != excluir and int(fila[4]) == int(dni):
                raise ValueError("Ya existe un alumno con ese DNI (legajo " + fila[0] + ").")
    finally:
        if archivo is not None:
            archivo.close()


def alta_alumno(config, nombre, apellido, dni, email="", telefono=""):
    ficha = validar_ficha(nombre, apellido, dni, email, telefono)
    verificar_dni(config, ficha["dni"])
    ficha["legajo"] = archivos.siguiente_codigo(config["alumnos"], 7)
    ficha["activo"] = "1"
    archivos.guardar_registro(config["alumnos"], 7, (0,), (ficha["legajo"],), fila_desde_ficha(ficha))
    return ficha["legajo"]


def modificar_alumno(config, legajo, nombre, apellido, dni, email="", telefono=""):
    anterior = obtener_alumno(config, legajo)
    ficha = validar_ficha(nombre, apellido, dni, email, telefono)
    verificar_dni(config, ficha["dni"], anterior["legajo"])
    ficha["legajo"] = anterior["legajo"]
    ficha["activo"] = "1"
    archivos.guardar_registro(config["alumnos"], 7, (0,), (ficha["legajo"],), fila_desde_ficha(ficha))


def eliminar_alumno(config, legajo):
    ficha = obtener_alumno(config, legajo)
    ficha["activo"] = "0"
    # Baja lógica: desaparece del uso normal y sus notas quedan inaccesibles.
    archivos.guardar_registro(config["alumnos"], 7, (0,), (ficha["legajo"],), fila_desde_ficha(ficha))


def coincide_alumno(ficha, consulta):
    consulta = normalizar(consulta)
    coincide = False
    if ficha["activo"] == "1" and consulta != "":
        if consulta[0] == "#":
            coincide = consulta[1:] == ficha["legajo"]
        else:
            posible_dni = consulta.replace(".", "").replace(" ", "")
            if solo_digitos(posible_dni):
                coincide = int(posible_dni) == int(ficha["dni"])
            else:
                texto = normalizar(ficha["nombre"] + " " + ficha["apellido"])
                coincide = True
                for palabra in consulta.split():
                    if palabra not in texto:
                        coincide = False
    return coincide


def obtener_materia(config, codigo):
    fila = archivos.buscar(config["materias"], 2, (0,), (str(codigo),))
    if fila is None:
        raise ValueError("La materia no existe.")
    return fila[1]


def alta_materia(config, nombre):
    nombre = " ".join(nombre.split())
    if not 1 <= len(nombre) <= 80 or not nombre.replace(" ", "").replace("-", "").isalnum():
        raise ValueError("La materia debe tener de 1 a 80 caracteres: letras, números, espacios o guiones.")
    archivo = None
    mayor = 0
    try:
        archivo = open(config["materias"], "rt", encoding="utf-8")
        for linea in archivo:
            fila = archivos.separar(linea, 2)
            mayor = max(mayor, int(fila[0]))
            if normalizar(fila[1]) == normalizar(nombre):
                raise ValueError("Ya existe una materia con ese nombre.")
    finally:
        if archivo is not None:
            archivo.close()
    codigo = str(mayor + 1)
    archivos.guardar_registro(config["materias"], 2, (0,), (codigo,), [codigo, nombre])
    return codigo


def clave_cursada(config, legajo, materia, anio, periodo):
    texto_anio = str(anio)
    if not solo_digitos(texto_anio) or not 1900 <= int(texto_anio) <= 2100:
        raise ValueError("El año debe ser un entero entre 1900 y 2100.")
    if periodo not in config["periodos"]:
        raise ValueError("El período no es válido.")
    # La tupla identifica una cursada sin mezclar alumnos, materias o períodos.
    return (str(legajo), str(materia), str(int(texto_anio)), periodo)


def obtener_cursada(config, legajo, materia, anio, periodo):
    obtener_alumno(config, legajo)
    clave = clave_cursada(config, legajo, materia, anio, periodo)
    fila = archivos.buscar(config["cursadas"], 7, (0, 1, 2, 3), clave)
    if fila is None:
        raise ValueError("El alumno no está inscripto en esa materia, año y período.")
    return fila


def inscribir(config, legajo, materia, anio, periodo):
    obtener_alumno(config, legajo)
    obtener_materia(config, materia)
    clave = clave_cursada(config, legajo, materia, anio, periodo)
    if archivos.buscar(config["cursadas"], 7, (0, 1, 2, 3), clave) is not None:
        raise ValueError("El alumno ya está inscripto en esa materia, año y período.")
    archivos.guardar_registro(config["cursadas"], 7, (0, 1, 2, 3), clave, list(clave) + ["", "", ""])


def quitar_inscripcion(config, legajo, materia, anio, periodo):
    fila = obtener_cursada(config, legajo, materia, anio, periodo)
    if fila[4:] != ["", "", ""]:
        raise ValueError("No se puede quitar una inscripción que ya tiene notas.")
    clave = clave_cursada(config, legajo, materia, anio, periodo)
    archivos.guardar_registro(config["cursadas"], 7, (0, 1, 2, 3), clave, None)


def validar_nota(valor):
    try:
        numero = float(str(valor).replace(",", "."))
    except ValueError:
        raise ValueError("La nota debe ser un número entre 1 y 10.")
    if not 1 <= numero <= 10:
        raise ValueError("La nota debe estar entre 1 y 10.")
    return numero


def formatear_nota(valor):
    numero = validar_nota(valor)
    if numero == int(numero):
        texto = str(int(numero))
    else:
        texto = str(numero).replace(".", ",")
    return texto


def notas_de_cursada(config, fila):
    notas = {}
    for i in range(len(config["evaluaciones"])):
        if fila[i + 4] != "":
            notas[config["evaluaciones"][i]] = validar_nota(fila[i + 4])
    return notas


def registrar_nota(config, legajo, materia, anio, periodo, evaluacion, valor, modificar=False):
    fila = obtener_cursada(config, legajo, materia, anio, periodo)
    if evaluacion not in config["evaluaciones"]:
        raise ValueError("La evaluación no es válida.")
    posicion = config["evaluaciones"].index(evaluacion) + 4
    if fila[posicion] != "" and not modificar:
        raise ValueError("Esa evaluación ya tiene nota. Usá Modificar nota.")
    if fila[posicion] == "" and modificar:
        raise ValueError("No hay una nota cargada para esa evaluación.")
    fila[posicion] = str(validar_nota(valor))
    clave = clave_cursada(config, legajo, materia, anio, periodo)
    archivos.guardar_registro(config["cursadas"], 7, (0, 1, 2, 3), clave, fila)
