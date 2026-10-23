def existe(ruta):
    """Verifica si un archivo de texto existe intentando abrirlo en modo lectura."""
    encontrado = True
    try:
        arch = open(ruta, "rt", encoding="UTF8")
    except FileNotFoundError:
        encontrado = False
    finally:
        try:
            arch.close()
        except NameError:
            pass
    return encontrado


def separar(linea, cantidad):
    """Separa los campos de un registro delimitado por punto y coma."""
    campos = linea.rstrip("\n").split(";")
    assert len(campos) == cantidad, "Registro inválido en el archivo."
    return campos


def formar_linea(campos):
    """Arma una línea de texto separada por punto y coma a partir de una lista de campos."""
    textos = [str(campo).replace(";", ",") for campo in campos]
    return ";".join(textos) + "\n"


def obtener_clave(campos, posiciones):
    """Extrae una tupla con los campos que identifican al registro."""
    lista = [campos[pos] for pos in posiciones]
    return tuple(lista)


def buscar_en_archivo(arch, cantidad, posiciones, clave):
    """Busca un registro por su clave leyendo línea por línea con readline."""
    arch.seek(0)
    resultado = None
    linea = arch.readline()
    while linea != "" and resultado is None:
        campos = separar(linea, cantidad)
        if obtener_clave(campos, posiciones) == clave:
            resultado = campos
        linea = arch.readline()
    return resultado


def buscar(ruta, cantidad, posiciones, clave):
    """Abre un archivo de texto y busca un registro según su clave."""
    resultado = None
    try:
        arch = open(ruta, "rt", encoding="UTF8")
        resultado = buscar_en_archivo(arch, cantidad, posiciones, clave)
    finally:
        try:
            arch.close()
        except NameError:
            pass
    return resultado


def siguiente_codigo(ruta, cantidad):
    """Determina el próximo número de código secuencial en un archivo."""
    mayor = 0
    try:
        arch = open(ruta, "rt", encoding="UTF8")
        for linea in arch:
            campos = separar(linea, cantidad)
            codigo = int(campos[0])
            if codigo > mayor:
                mayor = codigo
    finally:
        try:
            arch.close()
        except NameError:
            pass
    return str(mayor + 1)


def copiar(origen, destino):
    """Copia un archivo de texto en otro procesando un registro por vez."""
    try:
        entrada = open(origen, "rt", encoding="UTF8")
        salida = open(destino, "wt", encoding="UTF8")
        for linea in entrada:
            salida.write(linea)
    finally:
        try:
            entrada.close()
            salida.close()
        except NameError:
            pass


def guardar_registro(ruta, cantidad, posiciones, clave, nuevo):
    """Agrega, modifica o elimina un registro copiando hacia un archivo auxiliar."""
    ruta_aux = ruta + ".tmp"
    encontrado = False
    try:
        entrada = open(ruta, "rt", encoding="UTF8")
        salida = open(ruta_aux, "wt", encoding="UTF8")
        for linea in entrada:
            campos = separar(linea, cantidad)
            if obtener_clave(campos, posiciones) == clave:
                encontrado = True
                if nuevo is not None:
                    salida.write(formar_linea(nuevo))
            else:
                salida.write(linea)

        if not encontrado and nuevo is not None:
            salida.write(formar_linea(nuevo))
    finally:
        try:
            entrada.close()
            salida.close()
        except NameError:
            pass

    copiar(ruta_aux, ruta)


def crear(ruta, registros):
    """Graba los registros iniciales en un archivo de texto nuevo."""
    try:
        arch = open(ruta, "wt", encoding="UTF8")
        for registro in registros:
            arch.write(formar_linea(registro))
    finally:
        try:
            arch.close()
        except NameError:
            pass


