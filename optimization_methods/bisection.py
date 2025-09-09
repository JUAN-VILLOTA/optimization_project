# optimization_methods/bisection.py
from dataclasses import dataclass
from typing import Callable, List, Dict, Any
import pandas as pd
import numpy as np

@dataclass
class BisectionResult:
    root: float
    f_root: float
    iterations: int
    table: pd.DataFrame
    errors: List[float]

def bisection(f: Callable[[float], float],
              xl: float,
              xu: float,
              max_iter: int = 50,
              tol: float = 1e-6) -> BisectionResult:
    """
    Método de Bisección para encontrar una raíz en [xl, xu].
    Requiere cambio de signo: f(xl)*f(xu) < 0
    Error usado: |xu - xl|/2 (típico en bisección).
    """
    fl = float(f(xl))
    fu = float(f(xu))
    if np.isnan(fl) or np.isnan(fu):
        raise ValueError("La función devolvió NaN en los límites.")
    if fl * fu > 0:
        raise ValueError("No hay cambio de signo en [xl, xu]. Asegura f(xl)*f(xu) < 0.")

    rows: List[Dict[str, Any]] = []
    errors: List[float] = []
    xr = xl  # inicialización

    for it in range(1, max_iter + 1):
        xr = (xl + xu) / 2.0
        fr = float(f(xr))

        err = abs(xu - xl) / 2.0
        errors.append(err)

        rows.append({
            "iter": it,
            "xl": xl, "xu": xu, "xr": xr,
            "f(xl)": fl, "f(xu)": fu, "f(xr)": fr,
            "error": err
        })

        if fr == 0.0 or err < tol:
            break

        # Selección de subintervalo
        if fl * fr < 0:
            xu = xr
            fu = fr
        else:
            xl = xr
            fl = fr

    df = pd.DataFrame(rows, columns=["iter", "xl", "xu", "xr", "f(xl)", "f(xu)", "f(xr)", "error"])
    return BisectionResult(root=xr, f_root=float(f(xr)), iterations=len(df), table=df, errors=errors)
