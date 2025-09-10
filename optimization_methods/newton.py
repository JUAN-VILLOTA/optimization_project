# optimization_methods/newton.py
import sympy as sp
import pandas as pd
from typing import Tuple, List

def newton_optimize(func_expr: str, x0: float, tol: float = 1e-5, max_iter: int = 50) -> Tuple[float, pd.DataFrame, List[float]]:
    """
    Método de Newton para optimización (buscar mínimo/máximo usando f' y f'').
    Devuelve (x_opt, table_df, errors_list).

    Parametros:
      - func_expr: str, expresión en x (ej. "2*sin(x) - x**2/10")
      - x0: float, valor inicial
      - tol: tolerancia para |x_{n+1} - x_n|
      - max_iter: iteraciones máximas
    """
    x = sp.Symbol("x")
    try:
        f = sp.sympify(func_expr)
    except Exception as e:
        raise ValueError(f"Expresión inválida: {e}")

    f1 = sp.diff(f, x)
    f2 = sp.diff(f1, x)

    f1_num = sp.lambdify(x, f1, modules=["numpy"])
    f2_num = sp.lambdify(x, f2, modules=["numpy"])
    f_num = sp.lambdify(x, f, modules=["numpy"])

    xi = float(x0)
    rows = []
    errors = []

    for it in range(1, max_iter + 1):
        f1xi = float(f1_num(xi))
        f2xi = float(f2_num(xi))

        if f2xi == 0:
            raise ZeroDivisionError("La segunda derivada se anuló en la iteración; no es posible continuar.")

        x_next = xi - f1xi / f2xi
        err = abs(x_next - xi)
        errors.append(err)

        rows.append({
            "Iter": it,
            "xi": xi,
            "f'(xi)": f1xi,
            "f''(xi)": f2xi,
            "xi+1": x_next,
            "Error": err
        })

        xi = x_next
        if err < tol:
            break

    import pandas as pd
    table = pd.DataFrame(rows, columns=["Iter", "xi", "f'(xi)", "f''(xi)", "xi+1", "Error"])
    return float(xi), table, errors
