# optimization_methods/false_position.py
from dataclasses import dataclass
from typing import Callable, List, Dict, Any
import pandas as pd
import numpy as np

@dataclass
class FalsePositionResult:
    root: float
    f_root: float
    iterations: int
    table: pd.DataFrame
    errors: List[float]

def false_position(f: Callable[[float], float],
                   xl: float,
                   xu: float,
                   max_iter: int = 50,
                   tol: float = 1e-6) -> FalsePositionResult:
    """
    Método de Falsa Posición (Interpolación Lineal).
    Requiere que f(xl) * f(xu) < 0.
    """

    fl = float(f(xl))
    fu = float(f(xu))
    if fl * fu > 0:
        raise ValueError("No hay cambio de signo en [xl, xu]. Asegura f(xl)*f(xu) < 0.")

    rows: List[Dict[str, Any]] = []
    errors: List[float] = []
    xr = xl

    for it in range(1, max_iter + 1):
        # Fórmula de Falsa Posición
        xr = xu - (fu * (xl - xu)) / (fl - fu)
        fr = float(f(xr))

        # Error: diferencia entre xr y el anterior xl o xu (aprox)
        err = abs(fr)
        errors.append(err)

        rows.append({
            "iter": it,
            "xl": xl, "xu": xu, "xr": xr,
            "f(xl)": fl, "f(xu)": fu, "f(xr)": fr,
            "error": err
        })

        if abs(fr) < tol:
            break

        # Actualizar intervalo
        if fl * fr < 0:
            xu = xr
            fu = fr
        else:
            xl = xr
            fl = fr

    df = pd.DataFrame(rows, columns=["iter", "xl", "xu", "xr", "f(xl)", "f(xu)", "f(xr)", "error"])
    return FalsePositionResult(root=xr, f_root=float(f(xr)), iterations=len(df), table=df, errors=errors)
