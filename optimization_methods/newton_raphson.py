# optimization_methods/newton_raphson.py
import sympy as sp
import pandas as pd

def newton_raphson(func_expr: str, x0: float, tol: float = 1e-5, max_iter: int = 50):
    """
    Método de Newton-Raphson para encontrar raíces de una función f(x) = 0.

    Parámetros:
        func_expr : str -> expresión de la función (ej: "2*sin(x) - x**2/10")
        x0        : float -> valor inicial
        tol       : float -> tolerancia
        max_iter  : int   -> máximo de iteraciones

    Retorna:
        root      : float -> raíz aproximada
        table     : DataFrame con las iteraciones
        errors    : lista con errores por iteración
    """
    x = sp.Symbol("x")
    f = sp.sympify(func_expr)
    fprime = sp.diff(f, x)

    f_lamb = sp.lambdify(x, f, modules=["numpy"])
    fprime_lamb = sp.lambdify(x, fprime, modules=["numpy"])

    xi = x0
    errors = []
    data = []

    for it in range(1, max_iter + 1):
        fxi = f_lamb(xi)
        fpxi = fprime_lamb(xi)

        if fpxi == 0:
            raise ZeroDivisionError("La derivada se anuló, no se puede continuar.")

        x_next = xi - fxi / fpxi
        error = abs(x_next - xi)

        data.append([it, xi, fxi, fpxi, x_next, error])
        errors.append(error)

        if error < tol:
            xi = x_next
            break
        xi = x_next

    columns = ["Iter", "xi", "f(xi)", "f'(xi)", "xi+1", "Error"]
    table = pd.DataFrame(data, columns=columns)

    return xi, table, errors
