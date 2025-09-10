# gui/random_search_app.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

from optimization_methods.utils import make_numeric_function
from optimization_methods.random_search import random_search

class RandomSearchWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Método de Búsqueda Aleatoria")
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

        tk.Label(top, text="xl:", bg="white").grid(row=0, column=2, sticky="e")
        self.ent_xl = tk.Entry(top, width=10); self.ent_xl.grid(row=0, column=3); self.ent_xl.insert(0, "-5")

        tk.Label(top, text="xu:", bg="white").grid(row=0, column=4, sticky="e")
        self.ent_xu = tk.Entry(top, width=10); self.ent_xu.grid(row=0, column=5); self.ent_xu.insert(0, "5")

        tk.Label(top, text="iter máx:", bg="white").grid(row=1, column=0, sticky="w")
        self.ent_iter = tk.Entry(top, width=10); self.ent_iter.grid(row=1, column=1, sticky="w"); self.ent_iter.insert(0, "50")

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
            "Operadores: +, -, *, /, ** (potencia)\n\n"
            "Nota: La búsqueda aleatoria prueba puntos al azar en [xl, xu] y guarda el mejor."
        )
        tk.Label(self, text=help_txt, fg="#555", bg="white", justify="left", anchor="w").pack(
            fill="x", padx=12, pady=(6, 12)
        )

    # ==== Callbacks ====
    def _on_calculate(self):
        try:
            fx = self.ent_fx.get().strip()
            xl = float(self.ent_xl.get())
            xu = float(self.ent_xu.get())
            itmax = int(self.ent_iter.get())

            _, _, fnum = make_numeric_function(fx)
            self._f_numeric = fnum
            self._expr_str = fx

            x_best, f_best, table = random_search(fx, xl, xu, max_iter=itmax)
            self._last_result = (x_best, f_best, table)

            self.lbl_result.config(
                text=f"Mejor x ≈ {x_best:.6f} | f(x) = {f_best:.6f} | iter = {len(table)}"
            )
            self._plot_progress(table)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _on_plot_function(self):
        if self._f_numeric is None or not self._last_result:
            return
        xl = float(self.ent_xl.get())
        xu = float(self.ent_xu.get())
        xs = np.linspace(xl, xu, 600)
        ys = self._f_numeric(xs)

        x_best, f_best, _ = self._last_result

        fig = Figure(figsize=(7.8, 4.8), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(xs, ys, label=f"f(x) = {self._expr_str}")
        ax.scatter([x_best], [f_best], color="red", label=f"Mejor punto ≈ {x_best:.6f}")
        ax.axhline(0, color="black", linewidth=0.6)
        ax.axvline(0, color="black", linewidth=0.6)
        ax.legend()
        ax.set_title("Gráfica de la función")
        fig.tight_layout()
        self._embed_figure(fig)

    def _on_show_table(self):
        if not self._last_result:
            return
        _, _, table = self._last_result
        win = tk.Toplevel(self)
        win.title("Tabla de iteraciones — Búsqueda Aleatoria")
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

    # ==== Helpers ====
    def _plot_progress(self, table):
        fig = Figure(figsize=(7.8, 4.8), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(table["Iter"], table["f(x_best)"], marker="o")
        ax.set_title("Progreso del mejor valor encontrado")
        ax.set_xlabel("Iteración")
        ax.set_ylabel("f(x_best)")
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

def open_random_search_window(master=None):
    RandomSearchWindow(master)
