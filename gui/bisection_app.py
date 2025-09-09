# gui/bisection_app.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from optimization_methods.utils import make_numeric_function
from optimization_methods.bisection import bisection, BisectionResult

class BisectionWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Método de Bisección")
        self.geometry("980x760")
        self.configure(bg="white")
        self.resizable(True, True)

        self._canvas = None         # canvas matplotlib embebido
        self._last_result = None    # BisectionResult
        self._f_numeric = None      # función numérica
        self._expr_str = None

        self._build_ui()

    # ---------- UI ----------
    def _build_ui(self):
        # Frame superior: parámetros
        top = tk.Frame(self, bg="white")
        top.pack(fill="x", padx=12, pady=10)

        tk.Label(top, text="f(x):", bg="white").grid(row=0, column=0, sticky="w")
        self.ent_fx = tk.Entry(top, width=50)
        self.ent_fx.grid(row=0, column=1, padx=8, pady=4, sticky="w")
        self.ent_fx.insert(0, "x**3 - x - 2")  # ejemplo

        tk.Label(top, text="xl:", bg="white").grid(row=0, column=2, sticky="e")
        self.ent_xl = tk.Entry(top, width=10); self.ent_xl.grid(row=0, column=3, padx=4); self.ent_xl.insert(0, "1")

        tk.Label(top, text="xu:", bg="white").grid(row=0, column=4, sticky="e")
        self.ent_xu = tk.Entry(top, width=10); self.ent_xu.grid(row=0, column=5, padx=4); self.ent_xu.insert(0, "2")

        tk.Label(top, text="iter máx:", bg="white").grid(row=1, column=0, sticky="w", pady=(6,0))
        self.ent_iter = tk.Entry(top, width=10); self.ent_iter.grid(row=1, column=1, sticky="w", pady=(6,0)); self.ent_iter.insert(0, "50")

        tk.Label(top, text="tol:", bg="white").grid(row=1, column=2, sticky="e", pady=(6,0))
        self.ent_tol = tk.Entry(top, width=10); self.ent_tol.grid(row=1, column=3, pady=(6,0)); self.ent_tol.insert(0, "1e-6")

        # Botones
        btns = tk.Frame(self, bg="white")
        btns.pack(fill="x", padx=12, pady=8)
        tk.Button(btns, text="Calcular", command=self._on_calculate, bg="#16a34a", fg="white").pack(side="left", padx=4)
        tk.Button(btns, text="Graficar función", command=self._on_plot_function, bg="#2563eb", fg="white").pack(side="left", padx=4)
        tk.Button(btns, text="Ver tabla", command=self._on_show_table, bg="#f59e0b", fg="white").pack(side="left", padx=4)
        tk.Button(btns, text="Limpiar", command=self._on_clear, bg="#ef4444", fg="white").pack(side="left", padx=4)

        # Resultado
        self.lbl_result = tk.Label(self, text="", bg="white", font=("Segoe UI", 10, "bold"))
        self.lbl_result.pack(fill="x", padx=12, pady=4)

        # Área para gráficos (error o función)
        self.graph_area = tk.Frame(self, bg="white", height=500)
        self.graph_area.pack(fill="both", expand=True, padx=12, pady=8)

        # Ayuda
        help_txt = ("Operadores: ** (potencia), * (producto), /, +, -\n"
                    "Funciones: sin, cos, tan, exp, log(=ln), sqrt, abs, etc.")
        tk.Label(self, text=help_txt, fg="#555", bg="white").pack(padx=12, pady=(0,10), anchor="w")

    # ---------- Callbacks ----------
    def _on_calculate(self):
        try:
            fx = self.ent_fx.get().strip()
            xl = float(self.ent_xl.get())
            xu = float(self.ent_xu.get())
            itmax = int(self.ent_iter.get())
            tol = float(self.ent_tol.get())

            # función numérica segura
            _, _, fnum = make_numeric_function(fx)
            self._f_numeric = fnum
            self._expr_str = fx

            result: BisectionResult = bisection(fnum, xl, xu, max_iter=itmax, tol=tol)
            self._last_result = result

            # Mostrar resultado
            self.lbl_result.config(
                text=f"Raíz ≈ {result.root:.10f}  |  f(raíz) = {result.f_root:.3e}  |  iter = {result.iterations}"
            )

            # Graficar error
            self._plot_errors(result.errors)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _on_plot_function(self):
        try:
            if self._f_numeric is None:
                # Si aún no calculó, generamos función para graficar
                fx = self.ent_fx.get().strip()
                _, _, fnum = make_numeric_function(fx)
                self._f_numeric = fnum
                self._expr_str = fx

            xl = float(self.ent_xl.get())
            xu = float(self.ent_xu.get())
            xs = np.linspace(min(xl, xu), max(xl, xu), 600)
            ys = self._f_numeric(xs)

            fig = Figure(figsize=(7.8, 4.8), dpi=100)
            ax = fig.add_subplot(111)
            ax.plot(xs, ys, label=f"f(x) = {self._expr_str}")
            ax.axhline(0, linewidth=0.8)
            ax.axvline(0, linewidth=0.8)

            # Marcar raíz si existe
            if self._last_result is not None:
                xr = self._last_result.root
                ax.scatter([xr], [self._f_numeric(xr)], s=35, label=f"Raíz ≈ {xr:.6f}")

            ax.set_title("Gráfica de la función")
            ax.set_xlabel("x"); ax.set_ylabel("f(x)")
            ax.legend(loc="best")
            fig.tight_layout()

            self._embed_figure(fig)
        except Exception as e:
            messagebox.showerror("Error al graficar", str(e))

    def _on_show_table(self):
        if self._last_result is None:
            messagebox.showinfo("Información", "Primero ejecuta el cálculo.")
            return
        win = tk.Toplevel(self)
        win.title("Tabla de iteraciones — Bisección")
        win.geometry("800x420")

        txt = scrolledtext.ScrolledText(win, wrap="none")
        txt.pack(fill="both", expand=True)
        txt.insert("1.0", self._last_result.table.to_string(index=False))
        txt.configure(state="disabled")

    def _on_clear(self):
        self.lbl_result.config(text="")
        self._last_result = None
        self._f_numeric = None
        self._expr_str = None
        self._clear_canvas()

    # ---------- Helpers ----------
    def _plot_errors(self, errors):
        fig = Figure(figsize=(7.8, 4.8), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(range(1, len(errors)+1), errors, marker="o")
        ax.set_title(f"Convergencia del error (|xu - xl|/2)")
        ax.set_xlabel("Iteración")
        ax.set_ylabel("Error")
        ax.grid(True, linewidth=0.3)
        fig.tight_layout()
        self._embed_figure(fig)

    def _embed_figure(self, fig: Figure):
        self._clear_canvas()
        self._canvas = FigureCanvasTkAgg(fig, master=self.graph_area)
        self._canvas.draw()
        self._canvas.get_tk_widget().pack(fill="both", expand=True)

    def _clear_canvas(self):
        if self._canvas is not None:
            self._canvas.get_tk_widget().destroy()
            self._canvas = None

def open_bisection_window(master=None):
    BisectionWindow(master)
