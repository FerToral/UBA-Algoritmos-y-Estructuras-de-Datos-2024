"""Modelo racional de apoyo al TP1 Fondo Monetario Común,1C2024."""

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import comb


def racional(x):
    if isinstance(x, float) or isinstance(x, bool):
        raise TypeError("Usar enteros, Fraction o texto decimal, no float/bool")
    return Fraction(x)


def redistribuir(recursos, cooperan):
    r = [racional(x) for x in recursos]
    if (
        len(r) != len(cooperan)
        or any(type(x) is not bool for x in cooperan)
        or any(x < 0 for x in r)
    ):
        raise ValueError("Recursos/cooperación inválidos")
    if not r:
        return []
    fondo = sum((x for x, coop in zip(r, cooperan) if coop), Fraction()) / len(r)
    return [fondo if coop else x + fondo for x, coop in zip(r, cooperan)]


def configurar(recursos, cooperan, apuestas, pagos, eventos):
    r = [racional(x) for x in recursos]
    a = [[racional(x) for x in fila] for fila in apuestas]
    p = [[racional(x) for x in fila] for fila in pagos]
    n = len(r)
    if n == 0 or not (len(cooperan) == len(a) == len(p) == len(eventos) == n):
        raise ValueError("Dimensiones de individuos incompatibles")
    if any(x <= 0 for x in r) or any(type(x) is not bool for x in cooperan):
        raise ValueError("Estado inicial inválido")
    h = len(eventos[0])
    for i in range(n):
        m = len(a[i])
        if m == 0 or len(p[i]) != m or len(eventos[i]) != h:
            raise ValueError("Dimensiones de eventos incompatibles")
        if any(x < 0 for x in a[i]) or sum(a[i]) != 1 or any(x <= 0 for x in p[i]):
            raise ValueError("Apuestas/pagos inválidos")
        if any(type(x) is not int or not 0 <= x < m for x in eventos[i]):
            raise ValueError("Evento fuera del dominio")
    return r, a, p, h


def historial(recursos, cooperan, apuestas, pagos, eventos):
    r, a, p, h = configurar(recursos, cooperan, apuestas, pagos, eventos)
    historia = [[x] for x in r]
    for t in range(h):
        antes_fondo = [
            historia[i][-1] * a[i][eventos[i][t]] * p[i][eventos[i][t]]
            for i in range(len(r))
        ]
        nuevos = redistribuir(antes_fondo, cooperan)
        for fila, x in zip(historia, nuevos):
            fila.append(x)
    return historia


def maxima_local_unica(trayectoria):
    return (
        sum(
            (i == 0 or x > trayectoria[i - 1])
            and (i == len(trayectoria) - 1 or x > trayectoria[i + 1])
            for i, x in enumerate(trayectoria)
        )
        == 1
    )


def indice(individuo, n):
    if type(individuo) is not int or not 0 <= individuo < n:
        raise ValueError("Individuo fuera del dominio")


def decidir_cooperacion(individuo, recursos, cooperan, apuestas, pagos, eventos):
    configurar(recursos, cooperan, apuestas, pagos, eventos)
    indice(individuo, len(recursos))
    actual = list(cooperan)
    alternativa = list(cooperan)
    alternativa[individuo] = not alternativa[individuo]
    final_actual = historial(recursos, actual, apuestas, pagos, eventos)[individuo][-1]
    final_alternativo = historial(recursos, alternativa, apuestas, pagos, eventos)[
        individuo
    ][-1]
    return alternativa if final_alternativo > final_actual else actual


def _composiciones(total, longitud):
    if longitud == 1:
        yield (total,)
    else:
        for x in range(total + 1):
            for resto in _composiciones(total - x, longitud - 1):
                yield (x, *resto)


def apuesta_en_malla(
    individuo, recursos, cooperan, apuestas, pagos, eventos, denominador=10
):
    """Máximo de una malla FINITA; no certifica el máximo sobre todos los reales."""
    _, a, _, _ = configurar(recursos, cooperan, apuestas, pagos, eventos)
    indice(individuo, len(recursos))
    if type(denominador) is not int or denominador < 1:
        raise ValueError("Denominador entero positivo")
    m = len(a[individuo])
    if comb(denominador + m - 1, m - 1) > 100000:
        raise ValueError("Malla demasiado grande para este verificador")
    mejor, valor = None, None
    for coordenadas in _composiciones(denominador, m):
        candidato = [fila[:] for fila in a]
        candidato[individuo] = [Fraction(x, denominador) for x in coordenadas]
        final = historial(recursos, cooperan, candidato, pagos, eventos)[individuo][-1]
        if valor is None or final > valor:
            mejor, valor = candidato, final
    return mejor


@dataclass(frozen=True)
class DosEventos:
    s: object
    c: object


def fruto_individual(recurso, apuesta, pago, eventos):
    r = racional(recurso)
    ac, a_s, pc, ps = map(racional, (apuesta.c, apuesta.s, pago.c, pago.s))
    if (
        min(r, ac, a_s, pc, ps) <= 0
        or ac + a_s != 1
        or any(type(x) is not bool for x in eventos)
    ):
        raise ValueError("Precondición individual incumplida")
    res, i = r, 0
    while i < len(eventos):
        res = (res * ac) * pc if eventos[i] else (res * a_s) * ps
        i += 1
    return res


def formula_individual(recurso, apuesta, pago, eventos):
    caras = eventos.count(True)
    sellos = eventos.count(False)
    return (
        racional(recurso)
        * (racional(apuesta.c) * racional(pago.c)) ** caras
        * (racional(apuesta.s) * racional(pago.s)) ** sellos
    )
