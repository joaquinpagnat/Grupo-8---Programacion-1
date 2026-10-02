import contextlib
from copy import deepcopy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import Crear_Matriz
import Funciones_Reps
import gestion
import main


class GestionTests(unittest.TestCase):
    def setUp(self):
        self.datos = gestion.datos_nuevos()
        self.legajo = gestion.alta_alumno(self.datos, "Ana María", "López García", "12.345.678")
        self.periodo = gestion.PERIODOS[0]

    def inscribir(self, legajo=None, materia="1", anio=2026, periodo=None):
        gestion.inscribir(self.datos, legajo or self.legajo, materia, anio, periodo or self.periodo)

    def nota(self, evaluacion="Parcial 1", valor=8, **kwargs):
        gestion.registrar_nota(self.datos, self.legajo, "1", 2026, self.periodo, evaluacion, valor, **kwargs)

    def test_nombre_compuesto_y_datos_adicionales(self):
        gestion.modificar_alumno(self.datos, self.legajo, "Ana María", "O'Connor-López",
                                "12345678", "ana@example.com", "+54 11 1234-5678")
        alumno = self.datos["alumnos"][self.legajo]
        self.assertEqual(alumno["nombre"], "Ana María")
        self.assertEqual(alumno["email"], "ana@example.com")
        self.assertEqual(alumno["telefono"], "+54 11 1234-5678")

    def test_dni_duplicado_y_homonimos(self):
        with self.assertRaisesRegex(ValueError, "Ya existe"):
            gestion.alta_alumno(self.datos, "Otra", "Persona", "12 345 678")
        otro = gestion.alta_alumno(self.datos, "Ana María", "López García", "23456789")
        self.assertNotEqual(otro, self.legajo)
        self.assertEqual(len(gestion.buscar_alumnos(self.datos, "ana lopez")), 2)

    def test_dni_con_cero_inicial_no_elude_duplicados(self):
        gestion.alta_alumno(self.datos, "Luis", "Pérez", "1234567")
        with self.assertRaisesRegex(ValueError, "Ya existe"):
            gestion.alta_alumno(self.datos, "Lucas", "Gómez", "01234567")

    def test_ficha_invalida_no_altera_datos(self):
        for campo, valor in (("nombre", "123"), ("apellido", ""), ("dni", "abc"),
                             ("email", "sin-arroba"), ("telefono", "abc123")):
            with self.subTest(campo=campo):
                ficha = dict(nombre="Ana", apellido="Pérez", dni="22345678", email="", telefono="")
                ficha[campo] = valor
                antes = deepcopy(self.datos)
                with self.assertRaises(ValueError):
                    gestion.alta_alumno(self.datos, **ficha)
                self.assertEqual(self.datos, antes)

    def test_busquedas_sin_tildes_dni_legajo_y_vacia(self):
        for consulta in ("ANA MARIA", "lopez garcia", "garcia ana", "12.345.678", "#1"):
            with self.subTest(consulta=consulta):
                self.assertEqual(gestion.buscar_alumnos(self.datos, consulta)[0][0], self.legajo)
        self.assertEqual(gestion.buscar_alumnos(self.datos, ""), [])
        self.assertEqual(gestion.buscar_alumnos(self.datos, "no existe"), [])
        self.assertEqual(gestion.buscar_alumnos(self.datos, "#99"), [])

    def test_modificar_alumno_conserva_notas_y_legajo(self):
        self.inscribir()
        self.nota()
        gestion.modificar_alumno(self.datos, self.legajo, "Ana", "Pérez", "34567890")
        self.assertEqual(self.datos["alumnos"][self.legajo]["inscripciones"][0]["notas"], {"Parcial 1": 8})
        self.assertEqual(gestion.buscar_alumnos(self.datos, "34567890")[0][0], self.legajo)

    def test_modificar_no_admite_dni_de_otro(self):
        otro = gestion.alta_alumno(self.datos, "Juan", "Pérez", "23456789")
        antes = deepcopy(self.datos)
        with self.assertRaises(ValueError):
            gestion.modificar_alumno(self.datos, otro, "Juan", "Pérez", "12345678")
        self.assertEqual(self.datos, antes)

    def test_materias_individuales_y_no_inscripto(self):
        otro = gestion.alta_alumno(self.datos, "Juan", "Pérez", "23456789")
        self.inscribir()
        self.inscribir(otro, "2")
        self.nota()
        self.assertEqual(self.datos["alumnos"][otro]["inscripciones"][0]["notas"], {})
        with self.assertRaisesRegex(ValueError, "no está inscripto"):
            gestion.registrar_nota(self.datos, otro, "1", 2026, self.periodo, "Final", 6)

    def test_inscripciones_y_notas_separadas_por_anio_y_periodo(self):
        for anio, periodo in ((2026, self.periodo), (2026, gestion.PERIODOS[1]), (2027, self.periodo)):
            self.inscribir(anio=anio, periodo=periodo)
            gestion.registrar_nota(self.datos, self.legajo, "1", anio, periodo, "Parcial 1", 7)
        self.assertEqual(len(self.datos["alumnos"][self.legajo]["inscripciones"]), 3)
        with self.assertRaisesRegex(ValueError, "ya está inscripto"):
            self.inscribir()

    def test_anio_periodo_materia_invalidos(self):
        for materia, anio, periodo in (("99", 2026, self.periodo), ("1", 0, self.periodo),
                                       ("1", 2026, "Inexistente"), ("1", True, self.periodo)):
            with self.subTest(materia=materia, anio=anio, periodo=periodo):
                with self.assertRaises(ValueError):
                    gestion.inscribir(self.datos, self.legajo, materia, anio, periodo)

    def test_tres_evaluaciones_y_sin_duplicados(self):
        self.inscribir()
        self.assertEqual(gestion.EVALUACIONES, ("Parcial 1", "Parcial 2", "Final"))
        for evaluacion in gestion.EVALUACIONES:
            self.nota(evaluacion)
        with self.assertRaisesRegex(ValueError, "ya tiene nota"):
            self.nota()
        with self.assertRaises(ValueError):
            self.nota("Parcial 3")
        self.assertEqual(len(self.datos["alumnos"][self.legajo]["inscripciones"][0]["notas"]), 3)

    def test_notas_invalidas_y_decimales(self):
        self.inscribir()
        for nota in ("abc", "", 0, 11, "nan", "inf", True):
            with self.subTest(nota=nota):
                with self.assertRaises(ValueError):
                    self.nota(valor=nota)
        self.nota(valor="8,5")
        self.nota(valor=9, modificar=True)
        self.assertEqual(self.datos["alumnos"][self.legajo]["inscripciones"][0]["notas"]["Parcial 1"], 9)
        with self.assertRaisesRegex(ValueError, "No hay una nota"):
            self.nota("Final", modificar=True)

    def test_informe_legible_sin_corchetes(self):
        self.inscribir()
        self.nota(valor="8,5")
        texto = gestion.informe_alumno(self.datos, self.legajo)
        self.assertIn("Parcial 1: 8,5", texto)
        self.assertIn("Matemática | 2026 | 1.er cuatrimestre", texto)
        self.assertNotIn("[", texto)
        self.assertNotIn("]", texto)
        self.assertNotIn("Literatura", texto)

    def test_eliminar_alumno_no_borra_materias_ni_otros_alumnos(self):
        otros = [gestion.alta_alumno(self.datos, "Alumno", "Prueba", str(30000000 + i)) for i in range(15)]
        self.inscribir(otros[-1])
        catalogo = deepcopy(self.datos["materias"])
        gestion.eliminar_alumno(self.datos, otros[12])
        self.assertEqual(self.datos["materias"], catalogo)
        self.assertEqual(len(self.datos["alumnos"][otros[-1]]["inscripciones"]), 1)
        for legajo in list(self.datos["alumnos"]):
            gestion.eliminar_alumno(self.datos, legajo)
        self.assertEqual(self.datos["alumnos"], {})
        nuevo = gestion.alta_alumno(self.datos, "Nuevo", "Alumno", "45678901")
        self.assertEqual(nuevo, "17")

    def test_quitar_inscripcion_solo_sin_notas(self):
        self.inscribir()
        gestion.quitar_inscripcion(self.datos, self.legajo, "1", 2026, self.periodo)
        self.assertEqual(self.datos["alumnos"][self.legajo]["inscripciones"], [])
        self.inscribir()
        self.nota()
        with self.assertRaisesRegex(ValueError, "ya tiene notas"):
            gestion.quitar_inscripcion(self.datos, self.legajo, "1", 2026, self.periodo)

    def test_materias_duplicadas_y_alta_sin_asignacion_automatica(self):
        with self.assertRaisesRegex(ValueError, "Ya existe"):
            gestion.alta_materia(self.datos, "  MATEMATICA  ")
        gestion.alta_materia(self.datos, "Programación 1")
        self.assertEqual(self.datos["alumnos"][self.legajo]["inscripciones"], [])

    def test_guardar_y_recuperar(self):
        self.inscribir()
        self.nota()
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "datos.json"
            self.assertEqual(gestion.cargar_datos(ruta), gestion.datos_demostracion())
            gestion.guardar_datos(self.datos, ruta)
            self.assertEqual(gestion.cargar_datos(ruta), self.datos)
            self.assertFalse(ruta.with_suffix(".tmp").exists())

    def test_archivo_roto_no_se_sobrescribe(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "datos.json"
            ruta.write_text("archivo roto", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main.main(ruta), 1)
            self.assertEqual(ruta.read_text(encoding="utf-8"), "archivo roto")

    def test_rechaza_archivo_con_referencias_o_notas_invalidas(self):
        self.inscribir()
        for cambio in ("materia", "nota", "legajo", "dni", "inscripcion"):
            with self.subTest(cambio=cambio):
                roto = deepcopy(self.datos)
                alumno = roto["alumnos"][self.legajo]
                if cambio == "materia":
                    alumno["inscripciones"][0]["materia"] = "999"
                elif cambio == "nota":
                    alumno["inscripciones"][0]["notas"]["Parcial 1"] = float("nan")
                elif cambio == "legajo":
                    roto["proximo_legajo"] = 1
                elif cambio == "dni":
                    roto["alumnos"]["2"] = deepcopy(alumno)
                else:
                    alumno["inscripciones"].append(deepcopy(alumno["inscripciones"][0]))
                with self.assertRaises(ValueError):
                    gestion.validar_archivo(roto)

    def test_demostracion_lista_para_cargar_notas(self):
        datos = gestion.datos_demostracion()
        self.assertEqual(len(datos["alumnos"]), 15)
        self.assertEqual(len(datos["materias"]), 11)
        self.assertEqual(datos["proximo_legajo"], 16)
        self.assertEqual(gestion.validar_archivo(datos), datos)
        materias_utilizadas = set()
        for alumno in datos["alumnos"].values():
            self.assertEqual(len(alumno["inscripciones"]), 3)
            self.assertEqual(len({i["materia"] for i in alumno["inscripciones"]}), 3)
            self.assertTrue(all(not i["notas"] for i in alumno["inscripciones"]))
            materias_utilizadas.update(i["materia"] for i in alumno["inscripciones"])
        self.assertEqual(materias_utilizadas, set(datos["materias"]))

    def test_precargar_conserva_alumnos_y_no_duplica_ejemplos(self):
        self.inscribir()
        self.nota()
        ficha_original = deepcopy(self.datos["alumnos"][self.legajo])
        self.assertEqual(gestion.precargar_demostracion(self.datos, 2026), 15)
        self.assertEqual(self.datos["alumnos"][self.legajo], ficha_original)
        antes = deepcopy(self.datos)
        self.assertEqual(gestion.precargar_demostracion(self.datos, 2026), 0)
        self.assertEqual(self.datos, antes)

    def test_reabrir_no_restaura_ejemplos_eliminados(self):
        datos = gestion.datos_demostracion()
        gestion.eliminar_alumno(datos, "1")
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "datos.json"
            gestion.guardar_datos(datos, ruta)
            self.assertEqual(gestion.cargar_datos(ruta), datos)


class ConsolaTests(unittest.TestCase):
    def ejecutar(self, entradas, ruta):
        salida = io.StringIO()
        with patch("builtins.input", side_effect=entradas), contextlib.redirect_stdout(salida):
            estado = main.main(ruta)
        self.assertEqual(estado, 0)
        return salida.getvalue()

    def test_recorrido_completo_y_reapertura(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "datos.json"
            gestion.guardar_datos(gestion.datos_nuevos(), ruta)
            salida = self.ejecutar([
                "abc", "99", "1", "Ana María", "López", "12345678", "ana@example.com", "",
                "1", "Juan", "Gómez", "23456789", "", "",
                "8", "ana", "1", "1", "2026", "1",
                "2", "ana", "1", "1", "1", "texto", "11", "8,5",
                "3", "#1", "1", "1", "1", "9",
                "6", "#1", "1", "Ana María", "Pérez", "", "", "",
                "4", "perez", "1", "12",
            ], ruta)
            datos = gestion.cargar_datos(ruta)
            alumno = datos["alumnos"]["1"]
            self.assertEqual(alumno["apellido"], "Pérez")
            self.assertEqual(alumno["inscripciones"][0]["notas"], {"Parcial 1": 9})
            self.assertIn("Parcial 1: 9", salida)
            self.assertNotIn("Gómez, Juan", salida)  # La carga no imprime el padrón completo.
            reabierto = self.ejecutar(["7", "#1", "1", "12"], ruta)
            self.assertIn("Parcial 1: 9", reabierto)

    def test_sin_alumnos_y_cancelaciones(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "datos.json"
            gestion.guardar_datos(gestion.datos_nuevos(), ruta)
            salida = self.ejecutar(["2", "3", "4", "5", "6", "8", "9", "11",
                                   "1", "/cancelar", "12"], ruta)
            self.assertIn("No hay alumnos", salida)
            self.assertIn("Operación cancelada", salida)
            self.assertEqual(gestion.cargar_datos(ruta), gestion.datos_nuevos())

    def test_sin_materias_sin_notas_y_tres_evaluaciones_completas(self):
        datos = gestion.datos_nuevos()
        gestion.alta_alumno(datos, "Ana", "Pérez", "12345678")
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "datos.json"
            gestion.guardar_datos(datos, ruta)
            salida = self.ejecutar(["2", "#1", "1", "8", "#1", "1", "1", "2026", "1",
                                   "3", "#1", "1", "1",
                                   "2", "#1", "1", "1", "1", "6",
                                   "2", "#1", "1", "1", "1", "7",
                                   "2", "#1", "1", "1", "1", "8",
                                   "2", "#1", "1", "1", "12"], ruta)
            self.assertIn("no tiene materias asignadas", salida)
            self.assertIn("todavía no tienen notas", salida)
            self.assertIn("Ya están cargadas las tres evaluaciones", salida)

    def test_eliminacion_requiere_confirmacion(self):
        datos = gestion.datos_nuevos()
        gestion.alta_alumno(datos, "Ana", "Pérez", "12345678")
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "datos.json"
            gestion.guardar_datos(datos, ruta)
            self.ejecutar(["5", "#1", "1", "n", "12"], ruta)
            self.assertIn("1", gestion.cargar_datos(ruta)["alumnos"])
            self.ejecutar(["5", "#1", "1", "s", "12"], ruta)
            self.assertEqual(gestion.cargar_datos(ruta)["alumnos"], {})

    def test_guardado_fallido_revierte_operacion(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "datos.json"
            gestion.guardar_datos(gestion.datos_nuevos(), ruta)
            with patch("gestion.guardar_datos", side_effect=OSError("Sin permiso")):
                salida = self.ejecutar(["1", "Ana", "Pérez", "12345678", "", "", "11", "12"], ruta)
            self.assertIn("No se pudo guardar", salida)
            self.assertIn("No hay alumnos cargados", salida)
            self.assertNotIn("Cambios guardados correctamente", salida)

    def test_fin_de_entrada_cierra_sin_error(self):
        with tempfile.TemporaryDirectory() as carpeta:
            with patch("builtins.input", side_effect=EOFError), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main.main(Path(carpeta) / "datos.json"), 0)


if __name__ == "__main__":
    unittest.main()

