"""Lectura y escritura de archivos de texto, un registro por vez."""


def cerrar(abiertos):
    # Intenta cerrar todos los archivos, incluso si uno no puede cerrarse.
    error = None
    for archivo in abiertos:
        if archivo is not None:
            try:
                archivo.close()
            except OSError as problema:
                error = problema
    if error is not None:
        raise error


def existe(ruta):
    encontrado = True
    try:
        archivo = open(ruta, "rt", encoding="utf-8")
        archivo.close()
    except FileNotFoundError:
        encontrado = False
    return encontrado


def separar(linea, cantidad):
    campos = linea.rstrip("\n\r").split(";")
    if len(campos) != cantidad:
        raise ValueError("Registro inválido: cantidad de campos incorrecta.")
    return campos


def formar_linea(campos):
    textos = []
    for campo in campos:
        texto = str(campo)
        if ";" in texto or "\n" in texto or "\r" in texto:
            raise ValueError("Los datos no pueden contener punto y coma ni saltos de línea.")
        textos.append(texto)
    return ";".join(textos) + "\n"


def buscar_en_archivo(archivo, cantidad, clave):
    # La clave ocupa los primeros campos: el código o los 4 datos de la cursada.
    archivo.seek(0)
    resultado = None
    for linea in archivo:
        campos = separar(linea, cantidad)
        if tuple(campos[:len(clave)]) == clave:
            if resultado is not None:
                raise ValueError("El archivo contiene un identificador duplicado.")
            resultado = campos
    return resultado


def buscar(ruta, cantidad, clave):
    archivo = None
    try:
        archivo = open(ruta, "rt", encoding="utf-8")
        resultado = buscar_en_archivo(archivo, cantidad, clave)
    except:
        cerrar([archivo])
        raise
    cerrar([archivo])
    return resultado


def siguiente_codigo(ruta, cantidad):
    mayor = 0
    archivo = None
    try:
        archivo = open(ruta, "rt", encoding="utf-8")
        for linea in archivo:
            campos = separar(linea, cantidad)
            mayor = max(mayor, int(campos[0]))
    except:
        cerrar([archivo])
        raise
    cerrar([archivo])
    return str(mayor + 1)


def copiar(origen, destino):
    entrada = None
    salida = None
    try:
        entrada = open(origen, "rt", encoding="utf-8")
        salida = open(destino, "wt", encoding="utf-8")
        for linea in entrada:
            salida.write(linea)
    except:
        cerrar([entrada, salida])
        raise
    cerrar([entrada, salida])


def guardar_registro(ruta, cantidad, clave, nuevo):
    """Agrega o reemplaza un registro. Si nuevo es None, lo quita."""
    entrada = None
    salida = None
    encontrado = False
    try:
        entrada = open(ruta, "rt", encoding="utf-8")
        salida = open(ruta + ".nuevo", "wt", encoding="utf-8")
        for linea in entrada:
            campos = separar(linea, cantidad)
            if tuple(campos[:len(clave)]) == clave:
                if encontrado:
                    raise ValueError("El archivo contiene un identificador duplicado.")
                encontrado = True
                if nuevo is not None:
                    salida.write(formar_linea(nuevo))
            else:
                salida.write(linea)
        if not encontrado:
            if nuevo is None:
                raise ValueError("No existe el registro que se quiere quitar.")
            salida.write(formar_linea(nuevo))
    except:
        cerrar([entrada, salida])
        raise
    cerrar([entrada, salida])

    # Se conserva la versión anterior antes de reemplazar el archivo.
    copiar(ruta, ruta + ".bak")
    try:
        copiar(ruta + ".nuevo", ruta)
    except (OSError, KeyboardInterrupt):
        copiar(ruta + ".bak", ruta)
        raise


def crear(ruta, registros):
    archivo = None
    try:
        archivo = open(ruta, "wt", encoding="utf-8")
        for registro in registros:
            archivo.write(formar_linea(registro))
    except:
        cerrar([archivo])
        raise
    cerrar([archivo])
