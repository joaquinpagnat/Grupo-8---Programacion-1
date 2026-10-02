# Gestión de alumnos y notas — Grupo 8

Programa de consola en Python con alumnos, materias, inscripciones y notas.
No requiere instalar bibliotecas externas.

## Cómo abrirlo

1. Extraé todo el ZIP en una carpeta.
2. En Windows, hacé doble clic en **Iniciar.bat**.
3. También podés abrir una terminal en esa carpeta y ejecutar:

```text
python main.py
```

Requiere Python 3.9 o posterior. El iniciador puede usar el Python incluido con
Codex en esta computadora o una instalación de Python del sistema.

## Primer uso

1. Elegí **1 - Alta de alumno** y completá nombre, apellido y DNI. El correo y
   el teléfono son opcionales. El sistema asigna un legajo que no cambia.
2. Elegí **8 - Inscribir alumno en una materia**. Buscá al alumno, seleccioná
   una materia, el año y el período de cursada.
3. Elegí **2 - Agregar nota**. Buscá al alumno, seleccioná una de sus
   inscripciones y elegí **Parcial 1**, **Parcial 2** o **Final**.
4. Consultá sus notas con la opción **4** y corregilas con la opción **3**.
5. Salí con la opción **12**, al final del menú. Cada cambio ya queda guardado automáticamente.

## Demostración para el profesor

Al abrirlo por primera vez, el programa precarga **15 alumnos de ejemplo** y
las **11 materias originales**. Cada alumno ya tiene tres materias asignadas:
dos en el primer cuatrimestre y una en el segundo, con el año de inicio de la
demostración. Las notas están vacías para poder cargarlas durante la presentación.

Los nombres provienen del listado de ejemplo del programa original. Los DNI
del 90000001 al 90000015 y los correos `alumno1@example.com`, etc., son ficticios.

| Legajo inicial | Alumno | DNI de ejemplo |
| --- | --- | --- |
| 1 | Matías López | 90000001 |
| 2 | Carlos Gómez | 90000002 |
| 3 | Daniela Fernández | 90000003 |
| 4 | Juan Pérez | 90000004 |
| 5 | Sofía Rodríguez | 90000005 |
| 6 | Lucía González | 90000006 |
| 7 | Pedro Martínez | 90000007 |
| 8 | Florencia Sánchez | 90000008 |
| 9 | Valentina Romero | 90000009 |
| 10 | Diego Díaz | 90000010 |
| 11 | Martina Álvarez | 90000011 |
| 12 | Alejandro Ruiz | 90000012 |
| 13 | Camila Alonso | 90000013 |
| 14 | Gabriel Torres | 90000014 |
| 15 | Julieta Silva | 90000015 |

Materias: Matemática, Literatura, Electrotecnia, Inglés, Física, Química,
Historia, Geografía, Biología, Informática y Educación Física.

Recorrido breve para presentar:

1. **11 - Listar alumnos** muestra el padrón precargado.
2. **7 - Buscar alumno y ver su ficha**: buscá `matias` y seleccioná a Matías López.
3. **2 - Agregar nota**: buscá `matias`, elegí Matemática y cargá Parcial 1.
4. **4 - Ver notas de un alumno** muestra la nota sin corchetes.
5. **3 - Modificar nota** permite corregirla y **6** modifica los datos del alumno.
6. **12 - Salir** cierra el programa.

Si ya existe `datos.json`, se conservan sus datos al iniciar. La precarga
automática solo se usa cuando no hay archivo guardado; no vuelve a agregar
alumnos que se hayan eliminado. `datos.json` no se sube a GitHub porque puede
contener información personal de los alumnos.

## Qué se agregó y corrigió

| Pedido | Funcionamiento |
| --- | --- |
| Duplicados | No permite repetir DNI al crear ni modificar alumnos. También controla materias e inscripciones repetidas. |
| Más datos del alumno | Legajo automático, nombre, apellido, DNI, correo y teléfono. |
| Búsqueda al cargar notas | Busca por nombre, apellido, DNI completo o `#legajo`. Solo muestra coincidencias. |
| Modificación de alumnos | Opción 6; conserva el legajo, las materias asignadas y las notas. |
| Períodos | Cada inscripción tiene año y período: 1.er cuatrimestre, 2.º cuatrimestre o Anual. |
| Tipos y cantidad de notas | Dos parciales y un final por alumno, materia, año y período. |
| Materias por alumno | Se asignan expresamente mediante inscripciones; agregar una materia al catálogo no inscribe a todos. |
| Impresión de notas | Muestra una evaluación por línea, con su nombre y valor, sin corchetes. |
| Errores del original | Acepta nombres compuestos, valida entradas no numéricas y evita borrar materias al eliminar un alumno. |
| Persistencia | Guarda los cambios en `datos.json` y los recupera al iniciar. |

## Reglas de uso

- El DNI admite 7 u 8 dígitos. Se pueden ingresar puntos o espacios.
  Dos alumnos pueden llamarse igual si tienen DNI distintos.
- La búsqueda ignora mayúsculas y tildes: `ana lopez` encuentra a Ana López.
  Para el legajo 12 escribí `#12`; el DNI se busca completo.
- Las notas van de **1 a 10** y admiten decimales con coma o punto.
- Hay **como máximo tres notas por inscripción**: Parcial 1, Parcial 2 y Final.
  No es obligatorio cargar las tres juntas ni en un orden determinado.
  Si ya existe una nota, se corrige desde **Modificar nota**; no se duplica.
- El período corresponde a la cursada. El final pertenece a esa inscripción;
  no se modelan fechas o turnos de mesa de examen.
- La misma materia puede cursarse en otro año o período y sus notas quedan
  separadas. Los años admitidos van de 1900 a 2100.
- En la modificación de alumnos, Enter mantiene un dato; un guion (`-`)
  permite borrar el correo o el teléfono.
- `/cancelar` vuelve al menú sin aplicar cambios. Los selectores también
  ofrecen `0 - Volver` y una búsqueda vacía permite regresar.
- Eliminar un alumno requiere confirmación y elimina sus inscripciones y
  notas. Las materias del catálogo y los demás alumnos se conservan.
- Solo se puede quitar una inscripción si aún no tiene notas.
- La opción 11 muestra el listado completo cuando se lo solicita expresamente.

## Ejemplo de impresión

```text
Legajo 1 — López, Ana María
DNI: 12345678
Correo: ana@example.com | Teléfono: Sin informar

Matemática | 2026 | 1.er cuatrimestre
  Parcial 1: 8,5
  Parcial 2: 7
  Final: 9
```

## Tuplas y diccionarios en el código

En `gestion.py`, las opciones fijas son tuplas:

```python
PERIODOS = ("1.er cuatrimestre", "2.º cuatrimestre", "Anual")
EVALUACIONES = ("Parcial 1", "Parcial 2", "Final")
```

También se utiliza una tupla `(materia, anio, periodo)` para reconocer una
inscripción y evitar duplicarla.

Los alumnos son diccionarios indexados por legajo. Cada ficha contiene datos
personales y una lista de inscripciones. Las notas de cada inscripción son
otro diccionario, por ejemplo:

```python
{"Parcial 1": 8.5, "Parcial 2": 7.0, "Final": 9.0}
```

El diccionario `ACCIONES` de `Crear_Matriz.py` relaciona cada opción del menú
con su función. Estas estructuras se usan en el funcionamiento del programa.

## Archivos

- `main.py`: inicio, menú principal y guardado de cambios.
- `Crear_Matriz.py`: pantallas y operaciones de consola. Mantiene el nombre
  del módulo original; la matriz fue reemplazada por registros relacionados.
- `Funciones_Reps.py`: lectura de entradas, validaciones y cancelación.
- `gestion.py`: reglas, búsqueda, datos, tuplas, diccionarios y archivo JSON.
- `tests/test_gestion.py`: 28 pruebas automáticas de reglas y recorridos de uso.
- `Iniciar.bat`: iniciador para Windows.
- `datos.json`: se crea después del primer cambio guardado, junto a `main.py`.

Para trasladar los datos a otra carpeta, copiá también `datos.json`.
Si el guardado falla, la operación se revierte. Si un archivo de datos está
dañado, el programa lo informa y lo conserva sin sobrescribirlo.

## Ejecutar las pruebas

Desde la carpeta del programa:

```text
python -m unittest discover -s tests -v
```

Las pruebas usan datos temporales y no modifican el archivo de uso normal.

