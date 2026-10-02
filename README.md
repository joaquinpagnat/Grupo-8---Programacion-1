# Grupo 8 - Gestión de alumnos y notas

Versión adaptada a las 12 presentaciones de Programación 1 entregadas por el
grupo. Todos los archivos Python importan únicamente módulos propios.
No hace falta instalar bibliotecas adicionales.

## Iniciar

1. Descargá el proyecto completo y extraé el ZIP.
2. En Windows, abrí **Iniciar.bat**.
3. También podés abrir una terminal **en la carpeta del programa** y ejecutar
   `python main.py` con Python 3.9 o posterior.

El iniciador coloca la terminal en la carpeta correcta y busca Python instalado
en el equipo o el que incluye Codex. El `.bat` necesita los demás archivos.

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

## Demostración para el profesor

El primer inicio crea **15 alumnos ficticios**, **11 materias** y **45
inscripciones**: tres materias diferentes por alumno, dos en el primer
cuatrimestre y una en el segundo. Las cursadas de ejemplo son del año **2026**.
Las notas están vacías para cargarlas durante la presentación.

Alumnos: Matías López, Carlos Gómez, Daniela Fernández, Juan Pérez, Sofía
Rodríguez, Lucía González, Pedro Martínez, Florencia Sánchez, Valentina Romero,
Diego Díaz, Martina Álvarez, Alejandro Ruiz, Camila Alonso, Gabriel Torres y
Julieta Silva. Los DNI de ejemplo van del 90000001 al 90000015 y los correos
usan `example.com`.

Materias: Matemática, Literatura, Electrotecnia, Inglés, Física, Química,
Historia, Geografía, Biología, Informática y Educación Física.

Recorrido sugerido:

1. Opción **11**: ver el listado precargado.
2. Opción **7**: buscar `matias`. Escribí **el legajo que aparece en el resultado**.
3. Opción **2**: buscá al mismo alumno, seleccioná Matemática y cargá Parcial 1.
4. Opción **4**: consultar las notas, impresas una por línea y sin corchetes.
5. Opción **3**: corregir la nota; opción **6**: modificar los datos personales.
6. Opción **12**: salir. Al abrir otra vez, los cambios siguen guardados.

## Reglas

- El alumno tiene legajo automático, nombre, apellido, DNI, correo y teléfono.
  Correo y teléfono son opcionales. Los nombres admiten espacios y tildes.
- El DNI debe tener 7 u 8 dígitos; se aceptan puntos y espacios al ingresarlo.
  No puede repetirse entre alumnos activos. Se permiten personas con el mismo
  nombre si sus DNI son diferentes.
- La búsqueda funciona por nombre, apellido, DNI completo o `#legajo`.
  Ignora mayúsculas y tildes. Luego se ingresa el legajo del resultado elegido.
- Cada alumno se inscribe en sus propias materias, con año y período.
  El año se ingresa por teclado; no se consulta el reloj con `datetime`.
- Por cursada se admite una nota de **Parcial 1**, una de **Parcial 2** y una de
  **Final**. Las notas van de 1 a 10 y admiten decimales con coma o punto.
  Las evaluaciones ya cargadas se corrigen mediante Modificar nota.
- Se conservan períodos distintos: primer cuatrimestre, segundo cuatrimestre
  y anual. El final se asocia a la cursada seleccionada.
- Enter mantiene los datos al modificar una ficha. Un guion borra correo o
  teléfono. `/cancelar` o Ctrl+C cancela la operación y vuelve al menú.
- La eliminación requiere confirmación y se implementa como **baja lógica**:
  el alumno desaparece de las búsquedas y sus inscripciones y notas quedan
  fuera del uso normal. El registro se conserva en el archivo para no perder
  historial ni reutilizar legajos. No se borran materias ni otros alumnos.
- Solo se puede quitar una inscripción si no tiene notas.

## Archivos y guardado

- `main.py`: inicio y ciclo principal.
- `Crear_Matriz.py`: menú, búsquedas y pantallas. Se conserva el nombre original.
- `Funciones_Reps.py`: entrada por teclado y validación de opciones.
- `gestion.py`: validaciones, alumnos, materias, inscripciones y notas.
- `archivos.py`: lectura y escritura secuencial de registros de texto.
- `pruebas.py`: 52 comprobaciones con `assert` y módulos propios.
- `CONTENIDOS_DEL_CURSO.md`: relación entre las presentaciones y el código.

Se generan automáticamente `alumnos.txt`, `materias.txt` y `cursadas.txt`.
Cada línea contiene un registro y sus campos se separan con punto y coma.
Los archivos se leen con `for linea in archivo`, se cierran en `finally` y
**no se cargan completos en listas o diccionarios**. Las búsquedas conservan
solo la ficha seleccionada. Cada diccionario de notas tiene como máximo tres
elementos.

Al modificar datos se prepara una nueva versión línea por línea. Antes de
reemplazar el archivo se conserva una copia `.bak`. Si falla el reemplazo,
se intenta recuperar esa copia. Los archivos `.nuevo` son auxiliares.
Este mecanismo no garantiza recuperación automática ante un corte de energía
durante la escritura; la copia `.bak` permite recuperar la versión anterior.

Los archivos de datos y sus copias se excluyen de GitHub y del ZIP. Para
trasladar tus propios datos, copiá los **tres archivos `.txt` juntos**, con
el programa cerrado. Los ejemplos solo se crean si faltan los tres archivos;
si falta uno solo se informa el problema para evitar mezclar versiones.

### Datos de la versión anterior

El nuevo programa no usa `json`. Si encuentra únicamente un `datos.json`
anterior, avisa y lo conserva en lugar de comenzar con ejemplos. La conversión
de ese archivo debe hacerse antes de usar esta versión; no se incluyó un
importador JSON porque incumpliría la restricción de importaciones.

El ZIP y GitHub contienen solo el código: en una carpeta nueva se generan
los 15 alumnos de demostración.

## Pruebas

Desde la carpeta del proyecto, ejecutá `python pruebas.py`.
Se utilizan únicamente archivos llamados `prueba_alumnos.txt`,
`prueba_materias.txt` y `prueba_cursadas.txt`, junto a sus auxiliares. Las pruebas
recrean esos archivos en cada ejecución y no modifican los datos de uso normal.
Verifican duplicados, búsquedas, edición, notas, períodos, bajas y persistencia.
