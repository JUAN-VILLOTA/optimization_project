# gui/newton_raphson_app.py
import tkinter as tk
from tkinter import messagebox, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from optimization_methods.utils import make_numeric_function
from optimization_methods.newton_raphson import newton_raphson

class NewtonRaphsonWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Método de Newton-Raphson")
        self.geometry("980x760")
        self.configure(bg="white")
        self.resizable(True, True)

        self._canvas = None
        self._last_result = None
        self._f_numeric = None
        self._expr_str = None

        self._build_ui()

    def _build_ui(self):
        # ==== Entradas ====
        top = tk.Frame(self, bg="white")
        top.pack(fill="x", padx=12, pady=10)

        tk.Label(top, text="f(x):", bg="white").grid(row=0, column=0, sticky="w")
        self.ent_fx = tk.Entry(top, width=50)
        self.ent_fx.grid(row=0, column=1, padx=8, pady=4, sticky="w")
        self.ent_fx.insert(0, "2*sin(x) - (x**2)/10")

        tk.Label(top, text="x0:", bg="white").grid(row=0, column=2, sticky="e")
        self.ent_x0 = tk.Entry(top, width=10)
        self.ent_x0.grid(row=0, column=3)
        self.ent_x0.insert(0, "2.5")

        tk.Label(top, text="iter máx:", bg="white").grid(row=1, column=0, sticky="w")
        self.ent_iter = tk.Entry(top, width=10)
        self.ent_iter.grid(row=1, column=1, sticky="w")
        self.ent_iter.insert(0, "50")

        tk.Label(top, text="tol:", bg="white").grid(row=1, column=2, sticky="e")
        self.ent_tol = tk.Entry(top, width=10)
        self.ent_tol.grid(row=1, column=3)
        self.ent_tol.insert(0, "1e-5")

        # ==== Botones ====
        btns = tk.Frame(self, bg="white")
        btns.pack(fill="x", padx=12, pady=8)
        tk.Button(btns, text="Calcular", command=self._on_calculate, bg="#16a34a", fg="white").pack(side="left", padx=4)
        tk.Button(btns, text="Graficar función", command=self._on_plot_function, bg="#2563eb", fg="white").pack(side="left", padx=4)
        tk.Button(btns, text="Ver tabla", command=self._on_show_table, bg="#f59e0b", fg="white").pack(side="left", padx=4)
        tk.Button(btns, text="Limpiar", command=self._on_clear, bg="#ef4444", fg="white").pack(side="left", padx=4)

        self.lbl_result = tk.Label(self, text="", bg="white", font=("Segoe UI", 10, "bold"))
        self.lbl_result.pack(fill="x", padx=12, pady=4)

        self.graph_area = tk.Frame(self, bg="white", height=500)
        self.graph_area.pack(fill="both", expand=True, padx=12, pady=8)

        # ==== Ayuda ====
        help_txt = (
            "Funciones soportadas:\n"
            "  sin(x), cos(x), tan(x), exp(x), log(x) [= ln(x)], sqrt(x), abs(x)\n"
            "Constantes: pi, E\n"
            "Operadores: +, -, *, /, ** (potencia)"
        )
        tk.Label(self, text=help_txt, fg="#555", bg="white", justify="left", anchor="w").pack(
            fill="x", padx=12, pady=(6, 12)
        )

    # ----------- Callbacks -----------
    def _on_calculate(self):
        try:
            fx = self.ent_fx.get().strip()
            x0 = float(self.ent_x0.get())
            itmax = int(self.ent_iter.get())
            tol = float(self.ent_tol.get())

            _, _, fnum = make_numeric_function(fx)
            self._f_numeric = fnum
            self._expr_str = fx

            root, table, errors = newton_raphson(fx, x0, tol=tol, max_iter=itmax)
            self._last_result = (root, table, errors)

            self.lbl_result.config(
                text=f"Raíz ≈ {root:.6f} | f(x) = {fnum(root):.6f} | iter = {len(table)}"
            )
            self._plot_errors(errors)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _on_plot_function(self):
        if self._f_numeric is None or not self._last_result:
            return
        x0 = float(self.ent_x0.get())
        xs = np.linspace(x0 - 10, x0 + 10, 600)
        ys = self._f_numeric(xs)

        root, _, _ = self._last_result

        fig = Figure(figsize=(7.8, 4.8), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(xs, ys, label=f"f(x) = {self._expr_str}")
        ax.scatter([root], [self._f_numeric(root)], color="red", label=f"Raíz ≈ {root:.6f}")
        ax.axhline(0, color="black", linewidth=0.6)
        ax.axvline(0, color="black", linewidth=0.6)
        ax.legend()
        ax.set_title("Gráfica de la función")
        fig.tight_layout()
        self._embed_figure(fig)

    def _on_show_table(self):
        if not self._last_result:
            return
        _, table, _ = self._last_result
        win = tk.Toplevel(self)
        win.title("Tabla de iteraciones — Newton-Raphson")
        win.geometry("800x420")

        txt = scrolledtext.ScrolledText(win, wrap="none")
        txt.pack(fill="both", expand=True)
        txt.insert("1.0", table.to_string(index=False))
        txt.configure(state="disabled")

    def _on_clear(self):
        self.lbl_result.config(text="")
        self._last_result = None
        self._f_numeric = None
        self._expr_str = None
        self._clear_canvas()

    # ----------- Helpers -----------
    def _plot_errors(self, errors):
        fig = Figure(figsize=(7.8, 4.8), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(range(1, len(errors)+1), errors, marker="o")
        ax.set_title("Convergencia del error")
        ax.set_xlabel("Iteración"); ax.set_ylabel("Error")
        ax.grid(True, linewidth=0.3)
        fig.tight_layout()
        self._embed_figure(fig)

    def _embed_figure(self, fig):
        self._clear_canvas()
        self._canvas = FigureCanvasTkAgg(fig, master=self.graph_area)
        self._canvas.draw()
        self._canvas.get_tk_widget().pack(fill="both", expand=True)

    def _clear_canvas(self):
        if self._canvas:
            self._canvas.get_tk_widget().destroy()
            self._canvas = None

def open_newton_raphson_window(master=None):
    NewtonRaphsonWindow(master)
