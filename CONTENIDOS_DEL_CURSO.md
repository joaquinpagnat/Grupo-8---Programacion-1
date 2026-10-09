# Cómo se relaciona el programa con las clases

Se tomaron como referencia los 12 PDF aportados por el grupo.
La restricción del trabajo permite importar random o módulos propios;
este programa solo necesita módulos propios.

## Recorrido recomendado para explicar el código

1. **main.py:** comienza con la configuración y la preparación de archivos.
   Un `while` repite el menú hasta elegir 12. Cada `if/elif` llama a la
   función correspondiente. No hay una función intermedia que ejecute opciones.
2. **Crear_Matriz.py:** pide datos y muestra resultados. Antes de cargar una
   nota se busca al alumno y se elige una de sus cursadas.
3. **gestion.py:** valida los datos y aplica las reglas: DNI único, materias
   individuales, años, períodos y tres evaluaciones.
4. **archivos.py:** busca o modifica registros recorriendo el archivo línea
   por línea. Usa `seek(0)` cuando debe volver al principio.
5. **Funciones_Reps.py:** repite una pregunta cuando la opción o nota
   ingresada no es válida.

## Contenidos utilizados

| Presentación | Aplicación |
| --- | --- |
| Clase 01 - Introducción | Variables, conversiones, condiciones, ciclos y menú. |
| Clase 02 - Funciones | Funciones con parámetros, valores de retorno y módulos propios. Los retornos están fuera de los ciclos. |
| Clase 03 - Listas 1 | Listas de campos de un registro y opciones de evaluación. |
| Clase 04 - Listas 2 | Índices y rebanadas para separar la clave y las notas de una cursada. |
| Clase 05 - Cadenas 1 | Recorridos de cadenas, concatenación, split, join y replace. |
| Clase 06 - Cadenas 2 | Validación con isalpha e isalnum, strip, lower y f-strings. |
| Clase 06b - Expresiones regulares | No se usa re; las validaciones se resuelven con cadenas. |
| Clase 07 - Tuplas, conjuntos y diccionarios | Opciones fijas, claves de cursadas, fichas y notas. |
| Clase 08 - Excepciones | try, except y raise para entradas inválidas y problemas de archivos. |
| Clase 09 - Archivos | open, close, lectura por línea, write y seek(0). |
| Clase 09b - JSON | No se importa json; el almacenamiento es texto con separadores. |
| Clase 10 - Recursividad | Las operaciones se resuelven con ciclos; no necesitan recursividad. |

## Tuplas y diccionarios

Las opciones de evaluación forman una tupla porque son fijas:

```python
("Parcial 1", "Parcial 2", "Final")
```

Una cursada se identifica por otra tupla:

```python
(legajo, materia, anio, periodo)
```

Así, las notas de una materia no se mezclan con otro alumno, año o período.

La ficha de un alumno es un diccionario con claves como `nombre`,
`apellido`, `dni`, `email` y `telefono`. Sus notas también se pueden
representar con un diccionario, por ejemplo:

```python
{"Parcial 1": 8.0, "Parcial 2": 7.0}
```

Se conserva solo el registro que se está usando, no el padrón completo.

## Cierre de archivos y simplificaciones

Aunque los PDF explican `assert` y `finally`, se retiraron por pedido del
grupo. No se reemplazaron por clases, decoradores ni bibliotecas.

La función `archivos.cerrar` recibe una lista de archivos abiertos y llama
a `close()` para cada uno. Si hubo un problema al procesarlos, el bloque
`except` los cierra y `raise` vuelve a comunicar el error al programa
principal. Si todo salió bien, se cierran al terminar la operación.
Los `except` sin tipo se usan únicamente para esa limpieza y siempre
vuelven a lanzar el error; no lo ocultan.

La función `ejecutar()` pertenecía al archivo de pruebas retirado. Sus
comprobaciones se conservaron fuera de la entrega para verificar los cambios.
El programa se inicia leyendo `main.py`.
