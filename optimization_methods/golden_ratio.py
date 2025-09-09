# optimization_methods/golden_ratio.py
from dataclasses import dataclass
from typing import Callable, List, Dict, Any
import pandas as pd
import numpy as np

@dataclass
class GoldenRatioResult:
    point: float
    f_point: float
    iterations: int
    table: pd.DataFrame
    errors: List[float]

def golden_ratio(f: Callable[[float], float],
                 xl: float,
                 xu: float,
                 max_iter: int = 50,
                 tol: float = 1e-5) -> GoldenRatioResult:
    """
    Método de la Razón Dorada para optimización en una variable.
    Busca un máximo en el intervalo [xl, xu].
    """

    phi = (1 + np.sqrt(5)) / 2  # número áureo
    rows: List[Dict[str, Any]] = []
    errors: List[float] = []

    for it in range(1, max_iter + 1):
        # Cálculo de los puntos interiores
        x1 = xu - (xu - xl) / phi
        x2 = xl + (xu - xl) / phi

        f1 = float(f(x1))
        f2 = float(f(x2))

        error = abs(xu - xl)
        errors.append(error)

        rows.append({
            "iter": it,
            "xl": xl, "xu": xu,
            "x1": x1, "x2": x2,
            "f(x1)": f1, "f(x2)": f2,
            "error": error
        })

        # Actualización del intervalo
        if f1 < f2:
            xl = x1
        else:
            xu = x2

        if error < tol:
            break

    point = (xl + xu) / 2
    return GoldenRatioResult(
        point=point,
        f_point=float(f(point)),
        iterations=len(rows),
        table=pd.DataFrame(rows),
        errors=errors
    )
