# optimization_methods/random_search.py
import numpy as np
import pandas as pd
import sympy as sp

def random_search(func_expr: str, xl: float, xu: float, max_iter: int = 50, seed: int = None):
    """
    Método de Búsqueda Aleatoria (Random Search) para optimización unidimensional.

    Parámetros:
        func_expr: str   -> expresión de la función, ej: "2*sin(x) - (x**2)/10"
        xl, xu: float    -> límites del intervalo de búsqueda
        max_iter: int    -> número de evaluaciones aleatorias
        seed: int        -> semilla opcional para reproducibilidad

    Retorna:
        x_best: float    -> punto óptimo encontrado
        f_best: float    -> valor óptimo
        table: DataFrame -> tabla con iteraciones
    """
    if seed is not None:
        np.random.seed(seed)

    x = sp.Symbol("x")
    try:
        f = sp.lambdify(x, sp.sympify(func_expr), modules=["numpy"])
    except Exception as e:
        raise ValueError(f"Función inválida: {e}")

    xs = np.random.uniform(xl, xu, max_iter)
    fs = f(xs)

    data = []
    best_idx = 0
    for i in range(max_iter):
        if fs[i] > fs[best_idx]:
            best_idx = i
        data.append([i + 1, xs[i], fs[i], xs[best_idx], fs[best_idx]])

    table = pd.DataFrame(data, columns=["Iter", "xi", "f(xi)", "x_best", "f(x_best)"])
    return xs[best_idx], fs[best_idx], table
