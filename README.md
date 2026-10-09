# Grupo 8 - Gestión de alumnos y notas

Programa de consola para Programación 1. Usa solamente módulos propios.
No requiere instalar bibliotecas adicionales.

## Cómo abrirlo

1. Descargá el proyecto completo y descomprimí el ZIP.
2. En Windows, abrí **Iniciar.bat**. Necesitás Python 3.9 o posterior.
3. También podés ejecutar `python main.py` desde la carpeta del programa.

El archivo BAT necesita los demás archivos del proyecto para funcionar.

## Menú

| Opción | Operación |
| --- | --- |
| 1 | Alta de alumno |
| 2 | Agregar nota |
| 3 | Modificar nota |
| 4 | Ver notas de un alumno |
| 5 | Eliminar alumno |
| 6 | Modificar datos de un alumno |
| 7 | Buscar alumno y ver su ficha |
| 8 | Inscribir alumno en una materia |
| 9 | Quitar inscripción sin notas |
| 10 | Agregar materia al catálogo |
| 11 | Listar alumnos |
| 12 | Salir |

## Datos de ejemplo

En una carpeta nueva, el primer inicio crea 15 alumnos ficticios, 11 materias
y 45 inscripciones del año 2026. Cada alumno tiene tres materias asignadas,
repartidas entre los dos cuatrimestres. Las notas comienzan vacías.

Para una demostración: listá los alumnos con la opción 11, buscá `matias`
con la opción 2, ingresá su legajo `1`, elegí una cursada y cargá una nota.
Después consultala con la opción 4 o corregila con la opción 3.

## Reglas de uso

- Cada alumno tiene legajo automático, nombre, apellido y DNI. Correo y
  teléfono son opcionales. El DNI no puede repetirse entre alumnos activos.
- La búsqueda admite nombre, apellido, DNI completo o `#legajo`, sin
  distinguir mayúsculas ni tildes. Se elige escribiendo el legajo mostrado.
  Si no hay coincidencias o el legajo no corresponde, vuelve al menú.
- Cada inscripción relaciona un alumno, una materia, un año y un período:
  primer cuatrimestre, segundo cuatrimestre o anual.
- Cada cursada admite solamente **Parcial 1, Parcial 2 y Final**.
  Las notas van de 1 a 10 y admiten coma o punto decimal.
- Al modificar un alumno, Enter conserva el valor y un guion borra correo
  o teléfono. `/cancelar` o Ctrl+C vuelve al menú durante una operación.
- Eliminar un alumno requiere confirmación. Se marca como inactivo para
  conservar su historial y evitar reutilizar su legajo; deja de aparecer
  en las búsquedas y sus notas quedan fuera del uso normal.
- Una inscripción con notas no puede quitarse.

## Organización del código

| Archivo | Responsabilidad |
| --- | --- |
| `main.py` | Ciclo principal con `while` y opciones con `if/elif`. |
| `Crear_Matriz.py` | Menú, búsquedas, entrada de fichas y presentación de notas. |
| `Funciones_Reps.py` | Lectura y validación de opciones, notas y confirmaciones. |
| `gestion.py` | Reglas de alumnos, materias, inscripciones y notas; ejemplos iniciales. |
| `archivos.py` | Lectura, escritura y cierre de archivos de texto. |

Se mantienen tuplas para las opciones y claves de cursadas, y diccionarios
para las fichas y las notas. La explicación está en `CONTENIDOS_DEL_CURSO.md`.

## Guardado

Los cambios se guardan automáticamente en `alumnos.txt`, `materias.txt`
y `cursadas.txt`. Cada línea es un registro separado por punto y coma.
Se procesan línea por línea; no se carga el archivo completo en una lista.

Los archivos se cierran con `close()`, también si hay un error o se cancela.
Al modificar datos se prepara un archivo `.nuevo` y se conserva la versión
anterior en `.bak`. Si falla el reemplazo se intenta restaurar esa copia.
Esto no garantiza recuperación automática ante un corte de energía.

Esta versión conserva el formato de los tres archivos de texto anteriores.
Para trasladar tus datos, copiá los tres juntos con el programa cerrado.
Si falta solo uno, el programa avisa en lugar de mezclar datos con ejemplos.
Si encuentra únicamente un antiguo `datos.json`, solicita su conversión.

El ZIP y GitHub contienen el código y la documentación. Los datos personales,
las copias y los archivos temporales se excluyen mediante `.gitignore`.

## Simplificación del 9 de octubre de 2026

Se retiró `pruebas.py`: su función `ejecutar()` creaba datos temporales
para comprobar el programa y no formaba parte del uso normal.
También se quitó `ejecutar_opcion()`; ahora las llamadas están directamente
en `main.py`, como en el programa original.

El código entregado no utiliza `assert` ni `finally`. Se simplificaron las
búsquedas, las validaciones y los parámetros de las funciones de archivos.
La verificación se realizó por separado: 52 comprobaciones de las reglas,
recorridos del menú, persistencia, cancelación y cierre de archivos.

El programa principal distingue errores de archivos inexistentes, permisos,
lectura o escritura, codificación y datos inválidos mediante varios `except`.
Un `except:` final informa los errores no previstos y vuelve al menú.
Si el error ocurre durante la preparación inicial, informa el problema y sale.
