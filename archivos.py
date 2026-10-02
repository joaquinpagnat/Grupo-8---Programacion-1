"""Archivos de texto procesados registro por registro (clase 09)."""


def existe(ruta):
    encontrado = True
    archivo = None
    try:
        archivo = open(ruta, "rt", encoding="utf-8")
    except FileNotFoundError:
        encontrado = False
    finally:
        if archivo is not None:
            archivo.close()
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
            raise ValueError("Los campos no pueden contener punto y coma ni saltos de línea.")
        textos.append(texto)
    return ";".join(textos) + "\n"


def obtener_clave(campos, posiciones):
    valores = []
    for posicion in posiciones:
        valores.append(campos[posicion])
    return tuple(valores)


def buscar_en_archivo(archivo, cantidad, posiciones, clave):
    """Busca una fila sin almacenar el archivo completo."""
    archivo.seek(0)
    resultado = None
    for linea in archivo:
        campos = separar(linea, cantidad)
        if obtener_clave(campos, posiciones) == clave:
            if resultado is not None:
                raise ValueError("El archivo contiene un identificador duplicado.")
            resultado = campos
    return resultado


def buscar(ruta, cantidad, posiciones, clave):
    archivo = None
    try:
        archivo = open(ruta, "rt", encoding="utf-8")
        resultado = buscar_en_archivo(archivo, cantidad, posiciones, clave)
    finally:
        if archivo is not None:
            archivo.close()
    return resultado


def siguiente_codigo(ruta, cantidad):
    mayor = 0
    archivo = None
    try:
        archivo = open(ruta, "rt", encoding="utf-8")
        for linea in archivo:
            campos = separar(linea, cantidad)
            mayor = max(mayor, int(campos[0]))
    finally:
        if archivo is not None:
            archivo.close()
    return str(mayor + 1)


def copiar(origen, destino):
    """Copia un archivo de texto leyendo y escribiendo una línea por vez."""
    entrada = None
    salida = None
    try:
        entrada = open(origen, "rt", encoding="utf-8")
        salida = open(destino, "wt", encoding="utf-8")
        for linea in entrada:
            salida.write(linea)
    finally:
        try:
            if salida is not None:
                salida.close()
        finally:
            if entrada is not None:
                entrada.close()


def guardar_registro(ruta, cantidad, posiciones, clave, nuevo):
    """Agrega, reemplaza o quita una fila; conserva la versión previa en .bak."""
    linea_nueva = ""
    if nuevo is not None:
        linea_nueva = formar_linea(nuevo)
    entrada = None
    salida = None
    encontrado = False
    try:
        entrada = open(ruta, "rt", encoding="utf-8")
        salida = open(ruta + ".nuevo", "wt", encoding="utf-8")
        for linea in entrada:
            campos = separar(linea, cantidad)
            if obtener_clave(campos, posiciones) == clave:
                if encontrado:
                    raise ValueError("El archivo contiene un identificador duplicado.")
                encontrado = True
                if nuevo is not None:
                    salida.write(linea_nueva)
            else:
                salida.write(linea)
        if not encontrado:
            if nuevo is None:
                raise ValueError("No existe el registro que se quiere quitar.")
            salida.write(linea_nueva)
    finally:
        try:
            if salida is not None:
                salida.close()
        finally:
            if entrada is not None:
                entrada.close()

    # Primero se termina la nueva versión; después se conserva la anterior.
    copiar(ruta, ruta + ".bak")
    try:
        copiar(ruta + ".nuevo", ruta)
    except (OSError, KeyboardInterrupt):
        try:
            copiar(ruta + ".bak", ruta)
        except OSError:
            raise OSError("No se pudo restaurar el archivo. Conservá su copia .bak.")
        raise


def crear(ruta, registros):
    """Escribe los ejemplos definidos en el código, sin leer otros archivos."""
    archivo = None
    try:
        archivo = open(ruta, "wt", encoding="utf-8")
        for registro in registros:
            archivo.write(formar_linea(registro))
    finally:
        if archivo is not None:
            archivo.close()
