"""Reglas del sistema. Solo utiliza la biblioteca estándar de Python."""

import json
import math
import re
import unicodedata
from datetime import date
from pathlib import Path


# Tuplas: opciones fijas que no se modifican durante la ejecución.
PERIODOS = ("1.er cuatrimestre", "2.º cuatrimestre", "Anual")
EVALUACIONES = ("Parcial 1", "Parcial 2", "Final")
MATERIAS_INICIALES = (
    "Matemática", "Literatura", "Electrotecnia", "Inglés", "Física",
    "Química", "Historia", "Geografía", "Biología", "Informática",
    "Educación Física",
)
# Datos ficticios para presentar el programa al profesor.
ALUMNOS_EJEMPLO = (
    ("Matías", "López"), ("Carlos", "Gómez"), ("Daniela", "Fernández"),
    ("Juan", "Pérez"), ("Sofía", "Rodríguez"), ("Lucía", "González"),
    ("Pedro", "Martínez"), ("Florencia", "Sánchez"), ("Valentina", "Romero"),
    ("Diego", "Díaz"), ("Martina", "Álvarez"), ("Alejandro", "Ruiz"),
    ("Camila", "Alonso"), ("Gabriel", "Torres"), ("Julieta", "Silva"),
)


def normalizar(texto):
    """Permite buscar sin distinguir mayúsculas, tildes o espacios extra."""
    texto = unicodedata.normalize("NFD", texto.casefold())
    return " ".join("".join(c for c in texto if not unicodedata.combining(c)).split())


def datos_nuevos():
    # Diccionarios: los alumnos y las materias se identifican por claves estables.
    return {
        "version": 1,
        "proximo_legajo": 1,
        "alumnos": {},
        "materias": {str(i): nombre for i, nombre in enumerate(MATERIAS_INICIALES, 1)},
    }


def precargar_demostracion(datos, anio=None):
    """Agrega ejemplos sin reemplazar alumnos existentes ni repetir sus DNI."""
    anio = date.today().year if anio is None else anio
    validar_periodo(anio, PERIODOS[0])
    codigos = []
    for nombre_materia in MATERIAS_INICIALES:
        codigo = next((c for c, nombre in datos["materias"].items()
                       if normalizar(nombre) == normalizar(nombre_materia)), None)
        if codigo is None:
            codigo = alta_materia(datos, nombre_materia)
        codigos.append(codigo)

    agregados = 0
    for numero, (nombre, apellido) in enumerate(ALUMNOS_EJEMPLO, 1):
        dni = str(90000000 + numero)
        if any(int(alumno["dni"]) == int(dni) for alumno in datos["alumnos"].values()):
            continue
        legajo = alta_alumno(datos, nombre, apellido, dni, f"alumno{numero}@example.com")
        # Cada alumno cursa tres materias diferentes: dos en el primer
        # cuatrimestre y otra en el segundo. Las notas quedan listas para cargar.
        for posicion, desplazamiento in enumerate((0, 3, 6)):
            materia = codigos[(numero - 1 + desplazamiento) % len(codigos)]
            periodo = PERIODOS[0] if posicion < 2 else PERIODOS[1]
            inscribir(datos, legajo, materia, anio, periodo)
        agregados += 1
    return agregados


def datos_demostracion():
    datos = datos_nuevos()
    precargar_demostracion(datos)
    return datos


def validar_nombre(valor, campo):
    valor = " ".join(valor.split())
    if not valor or len(valor) > 80 or not any(c.isalpha() for c in valor):
        raise ValueError(f"{campo}: ingresá entre 1 y 80 caracteres.")
    if not all(c.isalpha() or c in " '-’" for c in valor):
        raise ValueError(f"{campo}: usá letras, espacios, apóstrofes o guiones.")
    return valor


def validar_ficha(datos, nombre, apellido, dni, email="", telefono="", excluir=None):
    nombre = validar_nombre(nombre, "Nombre")
    apellido = validar_nombre(apellido, "Apellido")
    dni = dni.strip().replace(".", "").replace(" ", "")
    if not re.fullmatch(r"[0-9]{7,8}", dni):
        raise ValueError("El DNI debe tener 7 u 8 dígitos, sin letras.")
    # También considera iguales 1234567 y 01234567.
    for legajo, alumno in datos["alumnos"].items():
        if legajo != excluir and int(alumno["dni"]) == int(dni):
            raise ValueError(f"Ya existe un alumno con ese DNI (legajo {legajo}).")
    email = email.strip()
    if email and (len(email) > 254 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email)):
        raise ValueError("El correo debe tener un formato como nombre@dominio.com.")
    telefono = telefono.strip()
    if telefono and (not re.fullmatch(r"\+?[0-9() -]{6,25}", telefono)
                     or not 6 <= sum(c.isdigit() for c in telefono) <= 15):
        raise ValueError("El teléfono debe contener entre 6 y 15 dígitos.")
    return {"nombre": nombre, "apellido": apellido, "dni": dni,
            "email": email, "telefono": telefono}


def alta_alumno(datos, nombre, apellido, dni, email="", telefono=""):
    ficha = validar_ficha(datos, nombre, apellido, dni, email, telefono)
    legajo = str(datos["proximo_legajo"])
    ficha["inscripciones"] = []
    datos["alumnos"][legajo] = ficha
    datos["proximo_legajo"] += 1
    return legajo


def modificar_alumno(datos, legajo, nombre, apellido, dni, email="", telefono=""):
    alumno = obtener_alumno(datos, legajo)
    ficha = validar_ficha(datos, nombre, apellido, dni, email, telefono, excluir=legajo)
    alumno.update(ficha)  # Conserva el legajo, las inscripciones y las notas.


def obtener_alumno(datos, legajo):
    if legajo not in datos["alumnos"]:
        raise ValueError("No existe ese legajo.")
    return datos["alumnos"][legajo]


def eliminar_alumno(datos, legajo):
    obtener_alumno(datos, legajo)
    del datos["alumnos"][legajo]


def buscar_alumnos(datos, consulta):
    consulta = normalizar(consulta)
    if not consulta:
        return []
    if consulta.startswith("#"):
        legajo = consulta[1:]
        return [(legajo, datos["alumnos"][legajo])] if legajo in datos["alumnos"] else []
    resultados = []
    for legajo, alumno in datos["alumnos"].items():
        texto = normalizar(f"{alumno['nombre']} {alumno['apellido']}")
        dni_consulta = consulta.replace(".", "").replace(" ", "")
        coincide_dni = dni_consulta.isascii() and dni_consulta.isdigit() and int(dni_consulta) == int(alumno["dni"])
        if coincide_dni or all(palabra in texto for palabra in consulta.split()):
            resultados.append((legajo, alumno))
    return sorted(resultados, key=lambda par: (normalizar(par[1]["apellido"]), normalizar(par[1]["nombre"])))


def alta_materia(datos, nombre):
    nombre = " ".join(nombre.split())
    if not nombre or len(nombre) > 80 or not any(c.isalnum() for c in nombre):
        raise ValueError("La materia debe tener un nombre de 1 a 80 caracteres.")
    if any(normalizar(m) == normalizar(nombre) for m in datos["materias"].values()):
        raise ValueError("Ya existe una materia con ese nombre.")
    codigo = str(max((int(c) for c in datos["materias"]), default=0) + 1)
    datos["materias"][codigo] = nombre
    return codigo


def validar_periodo(anio, periodo):
    if type(anio) is not int or not 1900 <= anio <= 2100:
        raise ValueError("El año debe ser un entero entre 1900 y 2100.")
    if periodo not in PERIODOS:
        raise ValueError("Seleccioná un período válido.")


def buscar_inscripcion(datos, legajo, materia, anio, periodo):
    alumno = obtener_alumno(datos, legajo)
    # Tupla compuesta: distingue la misma materia en distintos años o períodos.
    clave = (materia, anio, periodo)
    for inscripcion in alumno["inscripciones"]:
        if (inscripcion["materia"], inscripcion["anio"], inscripcion["periodo"]) == clave:
            return inscripcion
    return None


def inscribir(datos, legajo, materia, anio, periodo):
    alumno = obtener_alumno(datos, legajo)
    validar_periodo(anio, periodo)
    if materia not in datos["materias"]:
        raise ValueError("La materia no existe.")
    if buscar_inscripcion(datos, legajo, materia, anio, periodo):
        raise ValueError("El alumno ya está inscripto en esa materia, año y período.")
    alumno["inscripciones"].append({
        "materia": materia, "anio": anio, "periodo": periodo, "notas": {},
    })


def obtener_inscripcion(datos, legajo, materia, anio, periodo):
    inscripcion = buscar_inscripcion(datos, legajo, materia, anio, periodo)
    if inscripcion is None:
        raise ValueError("El alumno no está inscripto en esa materia, año y período.")
    return inscripcion


def quitar_inscripcion(datos, legajo, materia, anio, periodo):
    inscripcion = obtener_inscripcion(datos, legajo, materia, anio, periodo)
    if inscripcion["notas"]:
        raise ValueError("No se puede quitar una inscripción que ya tiene notas.")
    datos["alumnos"][legajo]["inscripciones"].remove(inscripcion)


def validar_nota(valor):
    if isinstance(valor, bool):
        raise ValueError("La nota debe ser un número entre 1 y 10.")
    try:
        numero = float(str(valor).replace(",", "."))
    except (ValueError, TypeError):
        raise ValueError("La nota debe ser un número entre 1 y 10.") from None
    if not math.isfinite(numero) or not 1 <= numero <= 10:
        raise ValueError("La nota debe estar entre 1 y 10.")
    return numero


def registrar_nota(datos, legajo, materia, anio, periodo, evaluacion, valor, modificar=False):
    inscripcion = obtener_inscripcion(datos, legajo, materia, anio, periodo)
    if evaluacion not in EVALUACIONES:
        raise ValueError("El tipo de evaluación no es válido.")
    existe = evaluacion in inscripcion["notas"]
    if existe and not modificar:
        raise ValueError("Esa evaluación ya tiene nota. Usá Modificar nota para corregirla.")
    if modificar and not existe:
        raise ValueError("No hay una nota cargada para esa evaluación.")
    inscripcion["notas"][evaluacion] = validar_nota(valor)


def informe_alumno(datos, legajo):
    alumno = obtener_alumno(datos, legajo)
    lineas = [
        f"Legajo {legajo} — {alumno['apellido']}, {alumno['nombre']}",
        f"DNI: {alumno['dni']}",
        f"Correo: {alumno['email'] or 'Sin informar'} | Teléfono: {alumno['telefono'] or 'Sin informar'}",
    ]
    if not alumno["inscripciones"]:
        lineas.append("Sin materias asignadas. Usá la opción 8 para inscribir al alumno.")
    ordenadas = sorted(alumno["inscripciones"], key=lambda i: (
        i["anio"], PERIODOS.index(i["periodo"]), datos["materias"][i["materia"]]))
    for inscripcion in ordenadas:
        lineas.append(f"\n{datos['materias'][inscripcion['materia']]} | {inscripcion['anio']} | {inscripcion['periodo']}")
        if not inscripcion["notas"]:
            lineas.append("  Sin notas cargadas.")
        for evaluacion in EVALUACIONES:
            if evaluacion in inscripcion["notas"]:
                nota = format(inscripcion["notas"][evaluacion], "g").replace(".", ",")
                lineas.append(f"  {evaluacion}: {nota}")
    return "\n".join(lineas)


def validar_archivo(datos):
    """Comprueba referencias y duplicados antes de aceptar un archivo guardado."""
    try:
        if type(datos) is not dict or type(datos["version"]) is not int or datos["version"] != 1:
            raise ValueError("Versión desconocida.")
        if type(datos["alumnos"]) is not dict or type(datos["materias"]) is not dict:
            raise ValueError("Alumnos y materias deben ser diccionarios.")
        control = datos_nuevos()
        control["materias"] = {}
        for codigo, nombre in datos["materias"].items():
            if not codigo.isascii() or not codigo.isdigit() or str(int(codigo)) != codigo or int(codigo) < 1:
                raise ValueError("Código de materia inválido.")
            alta_materia(control, nombre)
        control["materias"] = datos["materias"].copy()
        for legajo, alumno in datos["alumnos"].items():
            if not legajo.isascii() or not legajo.isdigit() or str(int(legajo)) != legajo or int(legajo) < 1:
                raise ValueError("Legajo inválido.")
            ficha = validar_ficha(control, *(alumno[c] for c in ("nombre", "apellido", "dni", "email", "telefono")))
            ficha["inscripciones"] = []
            control["alumnos"][legajo] = ficha
            if type(alumno["inscripciones"]) is not list:
                raise ValueError("Inscripciones inválidas.")
            for inscripcion in alumno["inscripciones"]:
                materia, anio, periodo = (inscripcion[c] for c in ("materia", "anio", "periodo"))
                inscribir(control, legajo, materia, anio, periodo)
                if type(inscripcion["notas"]) is not dict:
                    raise ValueError("Notas inválidas.")
                for evaluacion, valor in inscripcion["notas"].items():
                    if type(valor) not in (int, float):
                        raise ValueError("Las notas guardadas deben ser numéricas.")
                    registrar_nota(control, legajo, materia, anio, periodo, evaluacion, valor)
        proximo = datos["proximo_legajo"]
        if type(proximo) is not int or proximo <= max((int(c) for c in datos["alumnos"]), default=0):
            raise ValueError("El próximo legajo no es válido.")
        control["proximo_legajo"] = proximo
        return control
    except (KeyError, TypeError, AttributeError, ValueError, OverflowError) as error:
        raise ValueError(f"El archivo de datos no es válido: {error}") from None


def cargar_datos(ruta):
    ruta = Path(ruta)
    if not ruta.exists():
        return datos_demostracion()
    try:
        with ruta.open(encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except (json.JSONDecodeError, UnicodeError) as error:
        raise ValueError(f"No se puede leer el archivo de datos: {error}") from None
    return validar_archivo(datos)


def guardar_datos(datos, ruta):
    ruta = Path(ruta)
    comprobados = validar_archivo(datos)
    temporal = ruta.with_suffix(".tmp")
    try:
        with temporal.open("w", encoding="utf-8") as archivo:
            json.dump(comprobados, archivo, ensure_ascii=False, indent=2, allow_nan=False)
        temporal.replace(ruta)  # El archivo anterior se reemplaza solo al terminar.
    finally:
        if temporal.exists():
            temporal.unlink()

