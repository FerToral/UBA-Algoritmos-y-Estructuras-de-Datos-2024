from fractions import Fraction as F
from itertools import product
import unittest
import modelo as m


class FondoComun(unittest.TestCase):
    def ejemplo(self):
        return [1, 1], [[F(1, 2), F(1, 2)]] * 2, [[3, F(6, 5)]] * 2, [[0, 1], [1, 0]]

    def test_redistribucion_conserva_recursos(self):
        for recursos in product((0, 1, 2), repeat=3):
            for cooperan in product((False, True), repeat=3):
                resultado = m.redistribuir(recursos, cooperan)
                self.assertEqual(sum(resultado), sum(recursos))
                self.assertEqual(len(resultado), len(recursos))
                self.assertTrue(all(x >= 0 for x in resultado))
        self.assertEqual(m.redistribuir([], []), [])

    def test_tabla_de_la_consigna_sin_redondear(self):
        r, a, p, e = self.ejemplo()
        sin = m.historial(r, [False, False], a, p, e)
        mixto = m.historial(r, [True, False], a, p, e)
        ambos = m.historial(r, [True, True], a, p, e)
        self.assertEqual(sin, [[1, F(3, 2), F(9, 10)], [1, F(3, 5), F(9, 10)]])
        self.assertEqual(mixto, [[1, F(3, 4), F(9, 40)], [1, F(27, 20), F(9, 4)]])
        self.assertEqual(ambos, [[1, F(21, 20), F(441, 400)]] * 2)

    def test_ceros_y_horizonte_vacio(self):
        self.assertEqual(
            m.historial([1], [False], [[1, 0]], [[3, 1]], [[1, 0]]), [[1, 0, 0]]
        )
        self.assertEqual(m.historial([2], [True], [[1, 0]], [[3, 1]], [[]]), [[2]])
        self.assertEqual(
            m.decidir_cooperacion(0, [2], [True], [[1, 0]], [[3, 1]], [[]]), [True]
        )

    def test_maximos_con_vecinos_protegidos(self):
        for s, esperado in [
            ([], False),
            ([1], True),
            ([1, 1], False),
            ([1, 2], True),
            ([2, 1], True),
            ([2, 1, 2], False),
            ([1, 3, 2], True),
            ([1, 2, 2, 1], False),
        ]:
            self.assertEqual(m.maxima_local_unica(s), esperado)

    def test_decision_conserva_otros_y_compara_finales(self):
        r, a, p, e = self.ejemplo()
        anterior = [True, True]
        elegido = m.decidir_cooperacion(0, r, anterior, a, p, e)
        self.assertEqual(elegido[1], anterior[1])
        self.assertEqual(anterior, [True, True])
        final = m.historial(r, elegido, a, p, e)[0][-1]
        for alternativa in (False, True):
            self.assertGreaterEqual(
                final, m.historial(r, [alternativa, True], a, p, e)[0][-1]
            )

    def test_malla_incluye_frontera_y_no_cambia_otros(self):
        apuesta = m.apuesta_en_malla(
            0, [1], [False], [[F(1, 2), F(1, 2)]], [[3, 1]], [[0]]
        )
        self.assertEqual(apuesta, [[1, 0]])
        r, a, p, e = self.ejemplo()
        respuesta = m.apuesta_en_malla(0, r, [False, False], a, p, e, 10)
        self.assertEqual(respuesta[0], [F(1, 2), F(1, 2)])
        self.assertEqual(respuesta[1], a[1])

    def test_wp_formula_y_cada_prefijo_del_invariante(self):
        apuesta = m.DosEventos(s=F(2, 5), c=F(3, 5))
        pago = m.DosEventos(s=F(6, 5), c=3)
        for n in range(6):
            for eventos in product((False, True), repeat=n):
                for k in range(n + 1):
                    prefijo = list(eventos[:k])
                    self.assertEqual(
                        m.fruto_individual(7, apuesta, pago, prefijo),
                        m.formula_individual(7, apuesta, pago, prefijo),
                    )
        self.assertEqual(m.fruto_individual(7, apuesta, pago, []), 7)

    def test_configuracion_rechaza_inconsistencias(self):
        for argumentos in [
            ([1], [False], [[1, 1]], [[3, 1]], [[0]]),
            ([1], [False], [[1, 0]], [[3, 1]], [[2]]),
            ([1, 1], [False, True], [[1], [1]], [[3], [3]], [[0], []]),
            ([1], [False], [[-1, 2]], [[3, 1]], [[0]]),
        ]:
            with self.assertRaises(ValueError):
                m.historial(*argumentos)
        with self.assertRaises(TypeError):
            m.redistribuir([0.5], [True])
