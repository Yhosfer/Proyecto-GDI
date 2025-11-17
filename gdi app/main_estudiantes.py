# main_estudiantes.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from dao.estudiante_dao import EstudianteDAO


class EstudiantesView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.dao = EstudianteDAO()

        # Título
        ttk.Label(self, text="Listado de Estudiantes",
                  font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 10))

        # Barra de botones
        bar = ttk.Frame(self)
        bar.pack(fill="x", pady=(0, 10))

        ttk.Button(bar, text="🔄 Actualizar",
                   command=self.cargar_estudiantes).pack(side="left", padx=(0, 5))
        ttk.Button(bar, text="🔍 Buscar DNI/Apellido",
                   command=self.buscar).pack(side="left", padx=5)

        # Tabla
        self.tree = ttk.Treeview(
            self,
            columns=("id", "dni", "apellidos", "nombres"),
            show="headings",
            height=18
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("dni", text="Nro Documento")
        self.tree.heading("apellidos", text="Apellidos")
        self.tree.heading("nombres", text="Nombres")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("dni", width=140, anchor="w")
        self.tree.column("apellidos", width=220, anchor="w")
        self.tree.column("nombres", width=220, anchor="w")

        self.tree.pack(expand=True, fill="both")

        # Cargar datos al iniciar
        self.cargar_estudiantes()

    def limpiar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def cargar_estudiantes(self, filtro: str = ""):
        """Lee desde la BD y llena el Treeview."""
        self.limpiar_tabla()
        try:
            filas = self.dao.listar(filtro)
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer estudiantes:\n{e}")
            return

        for est in filas:
            self.tree.insert(
                "",
                "end",
                values=(
                    est["estudiante_id"],
                    est["numero_documento"],
                    est["apellidos"],
                    est["nombres"],
                ),
            )

    def buscar(self):
        texto = simpledialog.askstring("Buscar", "DNI o Apellido:")
        if texto is None:
            return
        texto = texto.strip()
        self.cargar_estudiantes(texto)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("San Benito - Estudiantes")
        self.geometry("800x500")
        self.minsize(700, 400)

        EstudiantesView(self).pack(expand=True, fill="both")


if __name__ == "__main__":
    app = App()
    app.mainloop()
