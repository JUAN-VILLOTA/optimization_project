# optimization_methods/quadratic_interpolation.py
import numpy as np
import pandas as pd
import sympy as sp

def quadratic_interpolation_method(func_expr, x0, x1, x2, tol=1e-5, max_iter=50):
    """
    Método de interpolación cuadrática para optimización unidimensional.
    """

    x = sp.Symbol("x")
    try:
        f = sp.lambdify(x, sp.sympify(func_expr), modules=["numpy"])
    except Exception as e:
        raise ValueError(f"Función inválida: {e}")

    data = []
    prev_x = x1  # para calcular error inicial
    for it in range(1, max_iter + 1):
        f0, f1, f2 = f(x0), f(x1), f(x2)

        # Fórmula del nuevo punto x3
        num = f0 * (x1**2 - x2**2) + f1 * (x2**2 - x0**2) + f2 * (x0**2 - x1**2)
        den = 2 * (f0 * (x1 - x2) + f1 * (x2 - x0) + f2 * (x0 - x1))
        if den == 0:
            raise ZeroDivisionError("Denominador se volvió cero durante la interpolación.")
        x3 = num / den
        f3 = f(x3)

        # Calcular error relativo aproximado
        error = abs(x3 - prev_x)
        prev_x = x3

        data.append([it, x0, f0, x1, f1, x2, f2, x3, f3, error])

        # Criterio de parada
        if error < tol:
            break

        # Reemplazo de puntos
        if f3 > f1:
            if x3 > x1:
                x0 = x1
            else:
                x2 = x1
            x1 = x3
        else:
            if x3 > x1:
                x2 = x3
            else:
                x0 = x3

    columns = ["Iter", "x0", "f(x0)", "x1", "f(x1)", "x2", "f(x2)", "x3", "f(x3)", "Error"]
    table = pd.DataFrame(data, columns=columns)

    return x3, table
