import tkinter as tk
from tkinter import ttk, messagebox

from gui.bisection_app import open_bisection_window
from gui.false_position_app import open_false_position_window
from gui.golden_ratio_app import open_golden_ratio_window

METHODS = {
    "Bisección": open_bisection_window,
    "Falsa Posición": open_false_position_window,
    "Razón Dorada": open_golden_ratio_window,
    "Interpolación Cuadrática": None,
    "Newton": None,
    "Newton-Raphson": None,
    "Búsqueda Aleatoria": None,
}

def launch_selected(root, method_name: str):
    func = METHODS.get(method_name)
    if func:
        func(root)
    else:
        messagebox.showinfo("En construcción", f"El método '{method_name}' aún no está disponible.")

def main():
    root = tk.Tk()
    root.title("Optimización — Métodos")
    root.geometry("520x220")
    root.configure(bg="white")

    tk.Label(root, text="Selecciona un método de optimización:", bg="white").pack(pady=(18,6))
    cmb = ttk.Combobox(root, values=list(METHODS.keys()), state="readonly", width=38)
    cmb.current(0)
    cmb.pack(pady=6)

    tk.Button(root, text="Abrir", command=lambda: launch_selected(root, cmb.get()),
              bg="#2563eb", fg="white").pack(pady=10)

    tk.Label(root, text="GUI en Tkinter — Proyecto modular", bg="white", fg="#555").pack(pady=(14,0))

    root.mainloop()   # 👈 Esto mantiene la ventana abierta

if __name__ == "__main__":
    main()

