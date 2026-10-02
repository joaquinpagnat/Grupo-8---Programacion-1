# Relación con el material de Programación 1

Se revisaron los **12 PDF proporcionados, con 283 páginas en total**. Algunas
páginas contienen más de una diapositiva. La tabla utiliza números de página
del PDF, no números de diapositiva.

La restricción del grupo es más estricta que los ejemplos de las presentaciones:
solo se permite importar `random` y módulos propios. Esta versión utiliza
solamente módulos propios; no necesita azar para funcionar.

| Material revisado | Páginas | Contenido y aplicación |
| --- | ---: | --- |
| P1_Clase01 - Introduccion.pdf | 31 | Variables, conversiones, operadores, condiciones, `while`, `for` y `range`. Se usan en el menú y las validaciones. |
| P1_Clase02 - Funciones.pdf | 23 | Funciones, parámetros, retornos, valores por omisión y módulos. Separación entre interfaz, reglas y archivos. Se mantienen los retornos fuera de los ciclos. |
| P1_Clase03 - Listas1.pdf | 29 | Listas, índices, `append`, pertenencia y funciones incorporadas. Opciones de evaluación y campos de un registro. `random` está explicado en las páginas 25 a 28, pero no es necesario en este programa. |
| P1_Clase04 - Listas2 (1).pdf | 26 | Rebanadas, copias, `enumerate`, comprensión y matrices. Se usan rebanadas de un registro y `enumerate` para preparar las inscripciones de ejemplo. |
| P1_Clase05 - Cadenas1.pdf | 22 | Cadenas, concatenación, recorrido, `split`, `join` y `replace`. El procedimiento de quitar tildes se basa en la página 15; los registros de texto usan las páginas 16 a 18. |
| P1_Clase06 - Cadenas2.pdf | 21 | `isalpha`, `isdigit`, `isalnum`, mayúsculas/minúsculas, `strip` y f-strings. Validación de nombres, limpieza de entradas y salida legible. |
| P1_Clase06b - Expresiones Regulares.pdf | 10 | Patrones y módulo `re`. Revisado, pero no se usa `re` por la restricción del grupo; la validación se hace recorriendo cadenas. |
| P1_Clase07 - TuplasConjuntosDiccionarios.pdf | 29 | Tuplas en las páginas 1 a 8 y diccionarios en las páginas 16 a 27. Se usan en opciones, fichas, notas y claves de inscripciones. No hace falta incorporar conjuntos sin una función concreta. |
| P1_Clase08 - Excepciones.pdf | 22 | `try`, `except`, `raise`, `finally` y `assert`. Errores de entrada, cancelación, cierre de archivos y comprobaciones del programa. No se definen clases de excepciones propias. |
| P1_Clase09 - Archivos.pdf | 34 | Texto plano, registros, `open`, escritura, lectura por línea, `seek(0)` y cierre. Las páginas 23 y 33 rechazan cargar archivos completos en memoria; la página 25 explica que CSV no requiere importar un módulo. |
| P1_Clase09b - JSON.pdf | 9 | JSON y serialización. Revisado, pero no se importa `json`. La página 8 también advierte sobre usar JSON como almacenamiento principal y presenta JSONL. |
| P1_Clase10 - Recursividad.pdf | 27 | Caso base, caso recursivo, factorial, Fibonacci, listas y Hanoi. Revisado; las operaciones de este programa se resuelven con ciclos y no necesitan recursividad. |

## Tuplas y diccionarios que se pueden mostrar al profesor

En `gestion.configuracion`, el diccionario relaciona nombres con rutas y
opciones. Los valores `periodos` y `evaluaciones` son tuplas:

```python
"periodos": ("1.er cuatrimestre", "2.º cuatrimestre", "Anual")
"evaluaciones": ("Parcial 1", "Parcial 2", "Final")
```

`gestion.clave_cursada` forma una tupla de cuatro elementos:

```python
(legajo, materia, anio, periodo)
```

Esta clave evita repetir una inscripción y separa las notas de materias,
alumnos, años y períodos distintos.

`gestion.ficha_desde_fila` convierte los campos de **un registro** en un
diccionario con nombres claros: `legajo`, `nombre`, `apellido`, `dni`, etc.
`gestion.notas_de_cursada` hace lo mismo con las tres evaluaciones de una
cursada. No se guarda el padrón completo en un diccionario.

## Cambios respecto de la primera versión mejorada

- Se eliminaron `json`, `math`, `re`, `unicodedata`, `datetime`, `pathlib`,
  `copy`, `unittest` y las demás importaciones ajenas al proyecto.
- Se eliminaron la clase de cancelación, expresiones generadoras y mecanismos
  de pruebas con bibliotecas. Las pruebas entregadas usan `assert`.
- Se conservan el alta, la modificación y la búsqueda de alumnos, el control
  de duplicados, las materias individuales, los años y períodos y las tres
  evaluaciones elegidas por el grupo.
- El guardado procesa archivos de texto una línea por vez. Los campos de un
  registro se separan con `split`; no se utiliza `eval`, `exec`, importación
  dinámica ni un lector JSON oculto.
- La baja lógica se guarda cambiando el campo `activo` de `1` a `0` y evita
  reutilizar legajos. Las notas de alumnos dados de baja no son accesibles
  desde el programa.
- Los ejemplos tienen año fijo 2026. Para una inscripción nueva el usuario
  ingresa el año desde el menú, sin recurrir a `datetime`.

La guía relaciona las decisiones con el contenido revisado; la evaluación
final del trabajo corresponde al profesor.
