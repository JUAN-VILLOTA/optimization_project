# optimization_methods/utils.py
from sympy import symbols, sympify, lambdify
import numpy as np

# Permitimos funciones matemáticas comunes de SymPy (evitamos eval inseguro)
ALLOWED = {
    # constantes
    "E": np.e, "PI": np.pi, "pi": np.pi,
    # funciones
    "sin": __import__("sympy").sin,
    "cos": __import__("sympy").cos,
    "tan": __import__("sympy").tan,
    "asin": __import__("sympy").asin,
    "acos": __import__("sympy").acos,
    "atan": __import__("sympy").atan,
    "exp": __import__("sympy").exp,
    "log": __import__("sympy").log,   # log natural
    "ln": __import__("sympy").log,
    "sqrt": __import__("sympy").sqrt,
    "sinh": __import__("sympy").sinh,
    "cosh": __import__("sympy").cosh,
    "tanh": __import__("sympy").tanh,
    "abs": __import__("sympy").Abs,
}

def make_numeric_function(func_str):
    """
    Convierte una cadena como 'x**3 - x - 2' en:
      - expr (Sympy)
      - f(x) numérica (Numpy) para evaluar en arrays o escalares
    Lanza ValueError si la expresión no es válida.
    """
    x = symbols("x")
    try:
        expr = sympify(func_str, locals=ALLOWED)
    except Exception as e:
        raise ValueError(f"Función inválida: {e}")

    f_numeric = lambdify(x, expr, modules="numpy")
    return x, expr, f_numeric
