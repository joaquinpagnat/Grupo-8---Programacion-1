import archivos


def configuracion(prefijo=""):
    """Devuelve el diccionario con las rutas de archivos y opciones fijas del sistema."""
    return {
        "alumnos": prefijo + "alumnos.txt",
        "materias": prefijo + "materias.txt",
        "cursadas": prefijo + "cursadas.txt",
        "periodos": ("1.er cuatrimestre", "2.º cuatrimestre", "Anual"),
        "evaluaciones": ("Parcial 1", "Parcial 2", "Final"),
        "anio_demo": 2026,
    }


def preparar_archivos(config):
    """Verifica la existencia de los archivos de datos o crea los de demostración."""
    presentes = 0
    for nombre in ("alumnos", "materias", "cursadas"):
        if archivos.existe(config[nombre]):
            presentes = presentes + 1
    if presentes == 0:
        crear_demostracion(config)
    elif presentes != 3:
        raise ValueError("Falta alguno de los archivos de datos (alumnos.txt, materias.txt o cursadas.txt).")


def crear_demostracion(config):
    """Genera los archivos iniciales con alumnos, materias y cursadas de prueba."""
    nombres = (
        ("Matías", "López"), ("Carlos", "Gómez"), ("Daniela", "Fernández"),
        ("Juan", "Pérez"), ("Sofía", "Rodríguez"), ("Lucía", "González"),
        ("Pedro", "Martínez"), ("Florencia", "Sánchez"), ("Valentina", "Romero"),
        ("Diego", "Díaz"), ("Martina", "Álvarez"), ("Alejandro", "Ruiz"),
        ("Camila", "Alonso"), ("Gabriel", "Torres"), ("Julieta", "Silva"),
    )
    materias = (
        "Matemática", "Literatura", "Electrotecnia", "Inglés", "Física",
        "Química", "Historia", "Geografía", "Biología", "Informática", "Educación Física",
    )
    catalogo = [[str(i + 1), materias[i]] for i in range(len(materias))]
    archivos.crear(config["materias"], catalogo)

    try:
        arch_alumnos = open(config["alumnos"], "wt", encoding="UTF8")
        arch_cursadas = open(config["cursadas"], "wt", encoding="UTF8")
        for i, (nombre, apellido) in enumerate(nombres):
            legajo = str(i + 1)
            dni = str(90000001 + i)
            fila_alumno = [legajo, "1", nombre, apellido, dni, f"alumno{legajo}@example.com", ""]
            arch_alumnos.write(archivos.formar_linea(fila_alumno))
            for posicion, desplazamiento in enumerate((0, 3, 6)):
                materia = str((i + desplazamiento) % len(materias) + 1)
                periodo = config["periodos"][0] if posicion < 2 else config["periodos"][1]
                fila_cursada = [legajo, materia, str(config["anio_demo"]), periodo, "", "", ""]
                arch_cursadas.write(archivos.formar_linea(fila_cursada))
    finally:
        try:
            arch_alumnos.close()
        except NameError:
            pass
        try:
            arch_cursadas.close()
        except NameError:
            pass



def normalizar(texto):
    """Convierte una cadena a minúsculas y reemplaza las vocales con tilde."""
    contilde = "áéíóúü"
    sintilde = "aeiouu"
    resultado = ""
    for caracter in texto.lower():
        if caracter in contilde:
            pos = contilde.index(caracter)
            resultado = resultado + sintilde[pos]
        else:
            resultado = resultado + caracter
    return " ".join(resultado.split())


def solo_digitos(texto):
    """Verifica si una cadena no vacía contiene únicamente dígitos numéricos."""
    return texto.isdigit()


def validar_nombre(texto, campo):
    """Valida que un nombre o apellido contenga únicamente letras y espacios."""
    texto = " ".join(texto.split())
    limpio = texto.replace(" ", "").replace("-", "").replace("'", "")
    if len(texto) == 0 or not limpio.isalpha():
        raise ValueError(f"{campo}: ingresá solo letras y espacios.")
    return texto


def validar_ficha(nombre, apellido, dni, email="", telefono=""):
    """Valida los datos personales de un alumno y los devuelve en un diccionario."""
    nombre = validar_nombre(nombre, "Nombre")
    apellido = validar_nombre(apellido, "Apellido")
    dni = dni.strip().replace(".", "").replace(" ", "")
    if not solo_digitos(dni) or len(dni) not in (7, 8):
        raise ValueError("El DNI debe tener 7 u 8 dígitos numéricos.")
    email = email.strip()
    if email != "":
        if email.count("@") != 1 or "." not in email or " " in email:
            raise ValueError("Correo inválido. Ejemplo: nombre@dominio.com.")
    telefono = telefono.strip()
    if telefono != "":
        limpio = telefono.replace(" ", "").replace("-", "").replace("+", "")
        if not limpio.isdigit() or len(limpio) < 6:
            raise ValueError("El teléfono debe tener al menos 6 dígitos.")
    return {
        "nombre": nombre,
        "apellido": apellido,
        "dni": dni,
        "email": email,
        "telefono": telefono,
    }


def ficha_desde_fila(fila):
    """Construye un diccionario de alumno a partir de los campos de una línea."""
    claves = ("legajo", "activo", "nombre", "apellido", "dni", "email", "telefono")
    return {claves[i]: fila[i] for i in range(len(claves))}


def fila_desde_ficha(ficha):
    """Convierte el diccionario de un alumno en una lista ordenada de campos."""
    claves = ("legajo", "activo", "nombre", "apellido", "dni", "email", "telefono")
    return [ficha[clave] for clave in claves]


def obtener_alumno(config, legajo):
    """Busca un alumno activo por su número de legajo."""
    fila = archivos.buscar(config["alumnos"], 7, (0,), (str(legajo),))
    if fila is None or fila[1] != "1":
        raise ValueError("No existe un alumno activo con ese legajo.")
    return ficha_desde_fila(fila)


def verificar_dni(config, dni, excluir=""):
    """Comprueba que el DNI no pertenezca a otro alumno activo en el padrón."""
    duplicado = None
    try:
        arch = open(config["alumnos"], "rt", encoding="UTF8")
        for linea in arch:
            fila = archivos.separar(linea, 7)
            if fila[1] == "1" and fila[0] != str(excluir) and int(fila[4]) == int(dni):
                duplicado = fila[0]
    finally:
        try:
            arch.close()
        except NameError:
            pass
    if duplicado is not None:
        raise ValueError(f"Ya existe un alumno con ese DNI (legajo {duplicado}).")


def alta_alumno(config, nombre, apellido, dni, email="", telefono=""):
    """Registra un nuevo alumno en el archivo y devuelve el legajo asignado."""
    ficha = validar_ficha(nombre, apellido, dni, email, telefono)
    verificar_dni(config, ficha["dni"])
    ficha["legajo"] = archivos.siguiente_codigo(config["alumnos"], 7)
    ficha["activo"] = "1"
    archivos.guardar_registro(config["alumnos"], 7, (0,), (ficha["legajo"],), fila_desde_ficha(ficha))
    return ficha["legajo"]


def modificar_alumno(config, legajo, nombre, apellido, dni, email="", telefono=""):
    """Actualiza los datos personales de un alumno existente."""
    anterior = obtener_alumno(config, legajo)
    ficha = validar_ficha(nombre, apellido, dni, email, telefono)
    verificar_dni(config, ficha["dni"], anterior["legajo"])
    ficha["legajo"] = anterior["legajo"]
    ficha["activo"] = "1"
    archivos.guardar_registro(config["alumnos"], 7, (0,), (ficha["legajo"],), fila_desde_ficha(ficha))


def eliminar_alumno(config, legajo):
    """Realiza la baja lógica de un alumno cambiando su estado activo a cero."""
    ficha = obtener_alumno(config, legajo)
    ficha["activo"] = "0"
    archivos.guardar_registro(config["alumnos"], 7, (0,), (ficha["legajo"],), fila_desde_ficha(ficha))


def coincide_alumno(ficha, consulta):
    """Evalúa si los datos de un alumno activo coinciden con el texto buscado."""
    consulta = normalizar(consulta)
    coincide = False
    if ficha["activo"] == "1" and consulta != "":
        if consulta[0] == "#":
            coincide = consulta[1:] == ficha["legajo"]
        else:
            posible_dni = consulta.replace(".", "").replace(" ", "")
            if solo_digitos(posible_dni):
                coincide = int(posible_dni) == int(ficha["dni"]) or posible_dni == ficha["legajo"]
            else:
                texto = normalizar(ficha["nombre"] + " " + ficha["apellido"])
                coincide = True
                for palabra in consulta.split():
                    if palabra not in texto:
                        coincide = False
    return coincide


def obtener_materia(config, codigo):
    """Devuelve el nombre de una materia a partir de su código."""
    fila = archivos.buscar(config["materias"], 2, (0,), (str(codigo),))
    if fila is None:
        raise ValueError("La materia no existe.")
    return fila[1]


def alta_materia(config, nombre):
    """Agrega una nueva materia al catálogo verificando que no esté repetida."""
    nombre = " ".join(nombre.split())
    limpio = nombre.replace(" ", "").replace("-", "")
    if not (1 <= len(nombre) <= 80) or not limpio.isalnum():
        raise ValueError("La materia debe contener solo letras, números, espacios o guiones.")
    mayor = 0
    repetida = False
    try:
        arch = open(config["materias"], "rt", encoding="UTF8")
        for linea in arch:
            fila = archivos.separar(linea, 2)
            if int(fila[0]) > mayor:
                mayor = int(fila[0])
            if normalizar(fila[1]) == normalizar(nombre):
                repetida = True
    finally:
        try:
            arch.close()
        except NameError:
            pass
    if repetida:
        raise ValueError("Ya existe una materia con ese nombre.")
    codigo = str(mayor + 1)
    archivos.guardar_registro(config["materias"], 2, (0,), (codigo,), [codigo, nombre])
    return codigo


def clave_cursada(config, legajo, materia, anio, periodo):
    """Valida y construye la tupla que identifica a una cursada."""
    texto_anio = str(anio).strip()
    if not solo_digitos(texto_anio) or not (1900 <= int(texto_anio) <= 2100):
        raise ValueError("El año debe ser un entero entre 1900 y 2100.")
    if periodo not in config["periodos"]:
        raise ValueError("El período no es válido.")
    return (str(legajo), str(materia), str(int(texto_anio)), periodo)


def obtener_cursada(config, legajo, materia, anio, periodo):
    """Busca y devuelve el registro de una cursada existente."""
    obtener_alumno(config, legajo)
    clave = clave_cursada(config, legajo, materia, anio, periodo)
    fila = archivos.buscar(config["cursadas"], 7, (0, 1, 2, 3), clave)
    if fila is None:
        raise ValueError("El alumno no está inscripto en esa materia, año y período.")
    return fila


def inscribir(config, legajo, materia, anio, periodo):
    """Inscribe a un alumno activo en una materia, año y período."""
    obtener_alumno(config, legajo)
    obtener_materia(config, materia)
    clave = clave_cursada(config, legajo, materia, anio, periodo)
    if archivos.buscar(config["cursadas"], 7, (0, 1, 2, 3), clave) is not None:
        raise ValueError("El alumno ya está inscripto en esa materia, año y período.")
    archivos.guardar_registro(config["cursadas"], 7, (0, 1, 2, 3), clave, list(clave) + ["", "", ""])


def quitar_inscripcion(config, legajo, materia, anio, periodo):
    """Elimina una inscripción de cursada que aún no posee calificaciones."""
    fila = obtener_cursada(config, legajo, materia, anio, periodo)
    if fila[4:] != ["", "", ""]:
        raise ValueError("No se puede quitar una inscripción que ya tiene notas.")
    clave = clave_cursada(config, legajo, materia, anio, periodo)
    archivos.guardar_registro(config["cursadas"], 7, (0, 1, 2, 3), clave, None)


def validar_nota(valor):
    """Convierte y valida que una nota se encuentre en el rango de 1 a 10."""
    try:
        numero = float(str(valor).replace(",", "."))
    except ValueError:
        raise ValueError("La nota debe ser un número entre 1 y 10.")
    if not (1 <= numero <= 10):
        raise ValueError("La nota debe estar entre 1 y 10.")
    return numero


def formatear_nota(valor):
    """Formatea una nota numérica para su visualización por pantalla."""
    numero = validar_nota(valor)
    if numero == int(numero):
        texto = str(int(numero))
    else:
        texto = str(round(numero, 2)).replace(".", ",")
    return texto


def notas_de_cursada(config, fila):
    """Extrae un diccionario con las evaluaciones calificadas de una cursada."""
    notas = {}
    for i, evaluacion in enumerate(config["evaluaciones"]):
        if fila[i + 4] != "":
            notas[evaluacion] = validar_nota(fila[i + 4])
    return notas


def sumar_notas(lista, inicio=0):
    """Suma recursivamente las calificaciones de una lista."""
    if inicio == len(lista):
        return 0
    else:
        return lista[inicio] + sumar_notas(lista, inicio + 1)


def calcular_promedio(lista):
    """Calcula el promedio de una lista de notas utilizando recursividad."""
    promedio = 0.0
    if len(lista) > 0:
        promedio = sumar_notas(lista) / len(lista)
    return promedio


def registrar_nota(config, legajo, materia, anio, periodo, evaluacion, valor, modificar=False):
    """Carga o modifica la calificación de una evaluación en una cursada."""
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


