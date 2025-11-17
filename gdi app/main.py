#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
San Benito - Aplicativo (Interfaz principal con 2 apartados)

Apartados:
- Cliente: asistente paso a paso para capturar datos y poblar tablas del estudiante.
- Administrador: vistas de mantenimiento/consultas.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from dao.estudiante_dao import EstudianteDAO
from dao.apoderado_dao import ApoderadoDAO
from dao.domicilio_dao import DomicilioDAO
from dao.salud_dao import SaludDAO
from dao.procedimientos_dao import ProcedimientosDAO

from ui.base import BaseModuleFrame          # ← clases base comunes
from views.cliente_wizard import ClienteWizard  # ← wizard del cliente

APP_TITLE = "San Benito - Gestión Escolar"
APP_SIZE = "1620x760"

# --------- Estilos (ttk) ---------
def setup_styles():
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("Sidebar.TFrame", background="#0f172a")
    style.configure("Content.TFrame", background="#f8fafc")
    style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
    style.configure("SubHeader.TLabel", font=("Segoe UI", 12, "bold"), foreground="#334155")
    style.configure("Nav.TButton", anchor="w", padding=(12, 10), font=("Segoe UI", 10, "bold"))
    style.map(
        "Nav.TButton",
        foreground=[("active", "#e2e8f0"), ("!active", "#e2e8f0")],
        background=[("active", "#1e293b"), ("!active", "#0f172a")],
    )
    style.configure("Status.TLabel", background="#e2e8f0", foreground="#111827")


# --------- VISTAS ADMIN ---------
class EstudiantesView(BaseModuleFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            "Estudiantes",
            "Visualización y búsqueda por DNI/Apellido de los estudiantes registrados.",
        )
        self.dao = EstudianteDAO()

        actions = ttk.Frame(self.body, padding=(0, 0, 0, 10), style="Content.TFrame")
        actions.pack(side="top", fill="x")

        ttk.Button(actions, text="🔄 Actualizar", command=self._cargar_estudiantes).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(actions, text="🔍 Buscar", command=self._buscar).pack(
            side="left", padx=(0, 8)
        )

        self.tree = ttk.Treeview(
            self.body,
            columns=(
                "id",
                "tipo_doc",
                "dni",
                "apellidos",
                "nombres",
                "fecha_nac",
                "sexo",
                "ubigeo_nac",
                "pais_nac",
            ),
            show="headings",
            height=16,
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("tipo_doc", text="Tipo Doc")
        self.tree.heading("dni", text="Nro Doc")
        self.tree.heading("apellidos", text="Apellidos")
        self.tree.heading("nombres", text="Nombres")
        self.tree.heading("fecha_nac", text="Fec. Nac.")
        self.tree.heading("sexo", text="Sexo")
        self.tree.heading("ubigeo_nac", text="Ubigeo Nac.")
        self.tree.heading("pais_nac", text="País Nac.")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("tipo_doc", width=80, anchor="center")
        self.tree.column("dni", width=110, anchor="w")
        self.tree.column("apellidos", width=160, anchor="w")
        self.tree.column("nombres", width=160, anchor="w")
        self.tree.column("fecha_nac", width=100, anchor="center")
        self.tree.column("sexo", width=60, anchor="center")
        self.tree.column("ubigeo_nac", width=110, anchor="center")
        self.tree.column("pais_nac", width=90, anchor="center")

        self.tree.pack(expand=True, fill="both")
        self._cargar_estudiantes()

    def _limpiar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def _cargar_estudiantes(self, filtro: str = ""):
        self._limpiar_tabla()
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
                    est["tipo_documento_id"],
                    est["numero_documento"],
                    est["apellidos"],
                    est["nombres"],
                    est["fecha_nacimiento"],
                    est["sexo"],
                    est["ubigeo_nacimiento_id"],
                    est["pais_nacimiento_id"],
                ),
            )

    def _buscar(self):
        texto = simpledialog.askstring("Buscar", "DNI o Apellido:")
        if texto is None:
            return
        self._cargar_estudiantes(texto.strip())


class ApoderadosView(BaseModuleFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            "Apoderados",
            "Visualización y búsqueda por DNI/Apellido de los apoderados registrados.",
        )
        self.dao = ApoderadoDAO()

        actions = ttk.Frame(self.body, padding=(0, 0, 0, 10), style="Content.TFrame")
        actions.pack(side="top", fill="x")

        ttk.Button(actions, text="🔄 Actualizar", command=self._cargar_apoderados).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(actions, text="🔍 Buscar", command=self._buscar).pack(
            side="left", padx=(0, 8)
        )

        self.tree = ttk.Treeview(
            self.body,
            columns=(
                "id",
                "tipo_doc",
                "dni",
                "apellidos",
                "nombres",
                "fecha_nac",
                "sexo",
                "vive",
                "vive_con",
            ),
            show="headings",
            height=16,
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("tipo_doc", text="Tipo Doc")
        self.tree.heading("dni", text="Nro Doc")
        self.tree.heading("apellidos", text="Apellidos")
        self.tree.heading("nombres", text="Nombres")
        self.tree.heading("fecha_nac", text="Fec. Nac.")
        self.tree.heading("sexo", text="Sexo")
        self.tree.heading("vive", text="Vive")
        self.tree.heading("vive_con", text="Vive con est.")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("tipo_doc", width=80, anchor="center")
        self.tree.column("dni", width=110, anchor="w")
        self.tree.column("apellidos", width=160, anchor="w")
        self.tree.column("nombres", width=160, anchor="w")
        self.tree.column("fecha_nac", width=100, anchor="center")
        self.tree.column("sexo", width=60, anchor="center")
        self.tree.column("vive", width=80, anchor="center")
        self.tree.column("vive_con", width=110, anchor="center")

        self.tree.pack(expand=True, fill="both")
        self._cargar_apoderados()

    def _limpiar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def _cargar_apoderados(self, filtro: str = ""):
        self._limpiar_tabla()
        try:
            filas = self.dao.listar(filtro)
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer apoderados:\n{e}")
            return

        for apo in filas:
            self.tree.insert(
                "",
                "end",
                values=(
                    apo["apoderado_id"],
                    apo["tipo_documento_id"],
                    apo["numero_documento"],
                    apo["apellidos"],
                    apo["nombres"],
                    apo["fecha_nacimiento"],
                    apo["sexo"],
                    apo["vive"],
                    apo["vive_con_estudiante"],
                ),
            )

    def _buscar(self):
        texto = simpledialog.askstring("Buscar", "DNI o Apellido:")
        if texto is None:
            return
        self._cargar_apoderados(texto.strip())


class DomiciliosView(BaseModuleFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            "Domicilios e Historial",
            "Historial de domicilios por estudiante (incluye domicilio vigente y anteriores).",
        )
        self.dao = DomicilioDAO()

        actions = ttk.Frame(self.body, padding=(0, 0, 0, 10), style="Content.TFrame")
        actions.pack(side="top", fill="x")

        ttk.Button(actions, text="🔄 Actualizar", command=self._cargar_domicilios).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(
            actions,
            text="🔍 Buscar por estudiante",
            command=self._buscar,
        ).pack(side="left", padx=(0, 8))

        self.tree = ttk.Treeview(
            self.body,
            columns=(
                "ed_id",
                "est_id",
                "dni",
                "estudiante",
                "dom_id",
                "direccion",
                "ubigeo",
                "telefono",
                "desde",
                "hasta",
            ),
            show="headings",
            height=16,
        )

        self.tree.heading("ed_id", text="ID Hist.")
        self.tree.heading("est_id", text="ID Est.")
        self.tree.heading("dni", text="DNI Est.")
        self.tree.heading("estudiante", text="Estudiante")
        self.tree.heading("dom_id", text="ID Dom.")
        self.tree.heading("direccion", text="Dirección")
        self.tree.heading("ubigeo", text="Ubigeo")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("desde", text="Desde")
        self.tree.heading("hasta", text="Hasta")

        self.tree.column("ed_id", width=70, anchor="center")
        self.tree.column("est_id", width=70, anchor="center")
        self.tree.column("dni", width=110, anchor="w")
        self.tree.column("estudiante", width=200, anchor="w")
        self.tree.column("dom_id", width=70, anchor="center")
        self.tree.column("direccion", width=220, anchor="w")
        self.tree.column("ubigeo", width=90, anchor="center")
        self.tree.column("telefono", width=110, anchor="center")
        self.tree.column("desde", width=90, anchor="center")
        self.tree.column("hasta", width=90, anchor="center")

        self.tree.pack(expand=True, fill="both")
        self._cargar_domicilios()

    def _limpiar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def _cargar_domicilios(self, filtro: str = ""):
        self._limpiar_tabla()
        try:
            filas = self.dao.listar(filtro)
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer domicilios:\n{e}")
            return

        for row in filas:
            nombre_est = f"{row['apellidos']}, {row['nombres']}"
            direccion = f"{row['direccion_linea1']} {row['direccion_linea2'] or ''}".strip()
            self.tree.insert(
                "",
                "end",
                values=(
                    row["estudiante_domicilio_id"],
                    row["estudiante_id"],
                    row["numero_documento"],
                    nombre_est,
                    row["domicilio_id"],
                    direccion,
                    row["ubigeo_id"],
                    row["telefono"],
                    row["desde"],
                    row["hasta"],
                ),
            )

    def _buscar(self):
        texto = simpledialog.askstring("Buscar", "DNI o Apellido del estudiante:")
        if texto is None:
            return
        self._cargar_domicilios(texto.strip())


class SaludView(BaseModuleFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            "Controles de Salud",
            "Ingresa DNI o apellido del estudiante para ver sus controles de salud.",
        )
        self.dao = SaludDAO()

        search_bar = ttk.Frame(self.body, padding=(0, 0, 0, 10), style="Content.TFrame")
        search_bar.pack(side="top", fill="x")

        ttk.Label(search_bar, text="DNI o Apellido del estudiante:").pack(side="left")
        self.txt_query = ttk.Entry(search_bar, width=30)
        self.txt_query.pack(side="left", padx=8)
        ttk.Button(search_bar, text="🔍 Buscar", command=self._buscar).pack(side="left")

        self.tree = ttk.Treeview(
            self.body,
            columns=("ctrl_id", "dni", "estudiante", "tipo_ctrl", "fecha", "resultado", "obs"),
            show="headings",
            height=16,
        )
        for c, t in zip(
            ("ctrl_id", "dni", "estudiante", "tipo_ctrl", "fecha", "resultado", "obs"),
            ("ID Ctrl", "DNI", "Estudiante", "Tipo Control", "Fecha", "Resultado", "Observaciones"),
        ):
            self.tree.heading(c, text=t)

        self.tree.column("ctrl_id", width=70, anchor="center")
        self.tree.column("dni", width=110, anchor="w")
        self.tree.column("estudiante", width=220, anchor="w")
        self.tree.column("tipo_ctrl", width=120, anchor="center")
        self.tree.column("fecha", width=100, anchor="center")
        self.tree.column("resultado", width=220, anchor="w")
        self.tree.column("obs", width=260, anchor="w")
        self.tree.pack(expand=True, fill="both")

    def _limpiar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def _buscar(self):
        q = self.txt_query.get().strip()
        if not q:
            messagebox.showwarning("Salud", "Ingresa un DNI o Apellido.")
            return
        self._limpiar()
        try:
            filas = self.dao.listar_por_estudiante(q)
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar controles:\n{e}")
            return
        if not filas:
            messagebox.showinfo("Salud", "No se encontraron controles para ese estudiante.")
            return
        for row in filas:
            nombre = f"{row['apellidos']}, {row['nombres']}"
            self.tree.insert(
                "",
                "end",
                values=(
                    row["control_salud_id"],
                    row["numero_documento"],
                    nombre,
                    row["tipo_control_id"],
                    row["fecha"],
                    row["resultado"],
                    row["observaciones"],
                ),
            )


# --------- NUEVA VISTA: PROCEDIMIENTOS (SPs) ---------
class ProcedimientosView(BaseModuleFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            "Procedimientos Almacenados",
            "Ejecuta procedimientos avanzados del sistema usando el DNI o apellido del estudiante.",
        )
        self.dao = ProcedimientosDAO()

        top = ttk.Frame(self.body, style="Content.TFrame")
        top.pack(fill="x", pady=10)

        ttk.Label(top, text="DNI o Apellido:").pack(side="left")
        self.txt_query = ttk.Entry(top, width=30)
        self.txt_query.pack(side="left", padx=8)

        btns = ttk.Frame(self.body, style="Content.TFrame")
        btns.pack(fill="x", pady=10)

        botones = [
            ("🕒 Último Control", self._ultimo_control),
            ("🌎 Estudiantes por País", self._por_pais),
            ("👨‍👩‍👧 Apoderados por Sexo", self._apoderados),
            ("📋 Historial Controles", self._historial_controles),
            ("🏠 Domicilio Actual", self._domicilio_actual),
            ("🗃️ Historial Domicilios", self._historial_domicilios),
            ("📑 Ficha Completa", self._info_completa),
            ("🔎 Buscar por Apellido", self._buscar_apellido),
            ("♂♀ Estudiantes por Sexo", self._estudiantes_sexo),
        ]

        for (txt, cmd) in botones:
            ttk.Button(btns, text=txt, command=cmd).pack(side="left", padx=5)

        table_frame = ttk.Frame(self.body, style="Content.TFrame")
        table_frame.pack(expand=True, fill="both", pady=10)

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(table_frame, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")

        yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        yscroll.grid(row=0, column=1, sticky="ns")

        xscroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        xscroll.grid(row=1, column=0, sticky="ew")

        self.tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

    # Utilidad: obtener ID de estudiante
    def _get_est_id(self):
        q = self.txt_query.get().strip()
        if not q:
            messagebox.showwarning("Atención", "Ingrese DNI o apellido.")
            return None

        est_id = self.dao.obtener_estudiante_id(q)
        if est_id is None:
            messagebox.showinfo("Sin resultados", "No se encontró estudiante.")
            return None
        return est_id

    # Mostrar resultados en el tree
    def _mostrar(self, filas):
        for c in self.tree.get_children():
            self.tree.delete(c)
        self.tree["columns"] = []

        if not filas:
            messagebox.showinfo("Resultado", "Sin datos.")
            return

        filas = [{k.lower(): v for k, v in row.items()} for row in filas]
        columnas = list(filas[0].keys())
        self.tree["columns"] = columnas

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140, anchor="center")

        for row in filas:
            self.tree.insert("", "end", values=[row[col] for col in columnas])

    # Botones
    def _ultimo_control(self):
        est_id = self._get_est_id()
        if est_id:
            self._mostrar(self.dao.ultimo_control(est_id))

    def _por_pais(self):
        self._mostrar(self.dao.estudiantes_por_pais())

    def _domicilio_actual(self):
        est_id = self._get_est_id()
        if est_id:
            self._mostrar(self.dao.domicilio_actual(est_id))

    def _apoderados(self):
        self._mostrar(self.dao.apoderados_por_sexo())

    def _historial_controles(self):
        est_id = self._get_est_id()
        if est_id:
            self._mostrar(self.dao.historial_controles(est_id))

    def _historial_domicilios(self):
        est_id = self._get_est_id()
        if est_id:
            self._mostrar(self.dao.historial_domicilios(est_id))

    def _info_completa(self):
        est_id = self._get_est_id()
        if est_id:
            self._mostrar(self.dao.info_completa(est_id))

    def _buscar_apellido(self):
        q = self.txt_query.get().strip()
        if not q:
            messagebox.showwarning("Atención", "Ingrese un apellido.")
            return
        self._mostrar(self.dao.buscar_por_apellido(q))

    def _estudiantes_sexo(self):
        self._mostrar(self.dao.estudiantes_por_sexo())


class ConsultasView(BaseModuleFrame):
    def __init__(self, parent):
        super().__init__(parent, "Consultas", "Búsquedas rápidas por DNI/Apellido y estadísticas básicas.")
        search_bar = ttk.Frame(self.body, padding=(0, 0, 0, 10), style="Content.TFrame")
        search_bar.pack(side="top", fill="x")
        ttk.Label(search_bar, text="DNI o Apellido:").pack(side="left")
        ttk.Entry(search_bar, width=32).pack(side="left", padx=8)
        ttk.Button(search_bar, text="🔎 Buscar").pack(side="left")
        self.results = tk.Text(self.body, height=20, wrap="word")
        self.results.pack(expand=True, fill="both")
        self.results.insert("end", "Resultados (por implementar con DAO)…")


# --------- Pantalla de inicio ---------
class StartScreen(ttk.Frame):
    def __init__(self, parent, on_select):
        super().__init__(parent, style="Content.TFrame")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        wrap = ttk.Frame(self, style="Content.TFrame", padding=40)
        wrap.grid(column=0, row=0, sticky="nsew")
        wrap.columnconfigure(0, weight=1)

        ttk.Label(wrap, text="Bienvenido", style="Header.TLabel").grid(column=0, row=0, sticky="w")
        ttk.Label(
            wrap,
            text="Selecciona un modo de trabajo:",
            style="SubHeader.TLabel",
        ).grid(column=0, row=1, sticky="w", pady=(6, 16))

        cards = ttk.Frame(wrap, style="Content.TFrame")
        cards.grid(column=0, row=2, sticky="nsew")
        for i in range(2):
            cards.columnconfigure(i, weight=1)

        cliente = ttk.Frame(cards, padding=20, style="Content.TFrame")
        cliente.grid(column=0, row=0, sticky="nsew", padx=(0, 10))
        ttk.Label(cliente, text="👤  Cliente", style="SubHeader.TLabel").grid(column=0, row=0, sticky="w")
        ttk.Label(
            cliente,
            text="Asistente paso a paso para registrar un estudiante con su apoderado y domicilio.",
        ).grid(column=0, row=1, sticky="w", pady=(6, 10))
        ttk.Button(
            cliente,
            text="Entrar a Cliente",
            command=lambda: on_select("cliente"),
        ).grid(column=0, row=2, sticky="w")

        admin = ttk.Frame(cards, padding=20, style="Content.TFrame")
        admin.grid(column=1, row=0, sticky="nsew", padx=(10, 0))
        ttk.Label(admin, text="🛠️  Administrador", style="SubHeader.TLabel").grid(column=0, row=0, sticky="w")
        ttk.Label(
            admin,
            text="Gestiona datos: ver, actualizar, eliminar y consultas del sistema.",
        ).grid(column=0, row=1, sticky="w", pady=(6, 10))
        ttk.Button(
            admin,
            text="Entrar a Administrador",
            command=lambda: on_select("admin"),
        ).grid(column=0, row=2, sticky="w")


# --------- Shell Administrador ---------
class AdminShell(ttk.Frame):
    def __init__(self, parent, on_exit_to_home):
        super().__init__(parent)
        root = ttk.Frame(self, style="Content.TFrame")
        root.pack(expand=True, fill="both")
        root.columnconfigure(0, minsize=240)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, minsize=26)

        sidebar = ttk.Frame(root, style="Sidebar.TFrame")
        sidebar.grid(column=0, row=0, sticky="nsew")

        for idx, (text, key) in enumerate(
            [
                ("🏫  Estudiantes", "Estudiantes"),
                ("👨‍👩‍👧  Apoderados", "Apoderados"),
                ("🏠  Domicilios", "Domicilios"),
                ("🩺  Salud", "Salud"),
                ("📚  Procedimientos", "Procedimientos"),
            ]
        ):
            ttk.Button(
                sidebar,
                text=text,
                style="Nav.TButton",
                command=lambda k=key: self._show_view(k),
            ).pack(fill="x", padx=6, pady=(6 if idx == 0 else 2, 2))

        self.content = ttk.Frame(root, style="Content.TFrame")
        self.content.grid(column=1, row=0, sticky="nsew")
        self.content.rowconfigure(0, weight=1)
        self.content.columnconfigure(0, weight=1)

        self.status = ttk.Label(root, text="Admin listo", style="Status.TLabel", anchor="w")
        self.status.grid(column=0, row=1, columnspan=2, sticky="ew")

        topbar = ttk.Frame(self.content, style="Content.TFrame")
        topbar.grid(column=0, row=0, sticky="ew")
        ttk.Button(topbar, text="⟵ Volver al inicio", command=on_exit_to_home).pack(
            side="right", padx=10, pady=8
        )

        self._show_view("Estudiantes")

    def _show_view(self, name: str):
        for child in self.content.grid_slaves():
            info = child.grid_info()
            if info.get("row") != 0:
                child.destroy()

        view_parent = ttk.Frame(self.content, style="Content.TFrame")
        view_parent.grid(column=0, row=1, sticky="nsew")
        self.content.rowconfigure(1, weight=1)

        if name == "Estudiantes":
            view = EstudiantesView(view_parent)
        elif name == "Apoderados":
            view = ApoderadosView(view_parent)
        elif name == "Domicilios":
            view = DomiciliosView(view_parent)
        elif name == "Salud":
            view = SaludView(view_parent)
        elif name == "Procedimientos":
            view = ProcedimientosView(view_parent)
        else:
            view = BaseModuleFrame(view_parent, "Módulo", "Vista no implementada.")
        view.grid(column=0, row=0, sticky="nsew")


# --------- Aplicación ---------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_SIZE)
        self.minsize(1024, 680)

        setup_styles()
        self._build_menu()

        self.container = ttk.Frame(self, style="Content.TFrame")
        self.container.pack(expand=True, fill="both")

        self._go_home()

    def _build_menu(self):
        menubar = tk.Menu(self)

        m_archivo = tk.Menu(menubar, tearoff=0)
        m_archivo.add_command(label="Inicio", command=self._go_home)
        m_archivo.add_separator()
        m_archivo.add_command(label="Salir", command=self.destroy)
        menubar.add_cascade(label="Archivo", menu=m_archivo)

        m_modos = tk.Menu(menubar, tearoff=0)
        m_modos.add_command(label="Cliente", command=lambda: self._show_mode("cliente"))
        m_modos.add_command(label="Administrador", command=lambda: self._show_mode("admin"))
        menubar.add_cascade(label="Modos", menu=m_modos)

        self.config(menu=menubar)

    def _clear_container(self):
        for w in self.container.winfo_children():
            w.destroy()

    def _go_home(self):
        self._clear_container()
        StartScreen(self.container, on_select=self._show_mode).pack(expand=True, fill="both")

    def _show_mode(self, mode: str):
        self._clear_container()
        if mode == "cliente":
            ClienteWizard(self.container, on_exit_to_home=self._go_home).pack(
                expand=True, fill="both"
            )
        elif mode == "admin":
            AdminShell(self.container, on_exit_to_home=self._go_home).pack(
                expand=True, fill="both"
            )
        else:
            ttk.Label(self.container, text="Modo no reconocido").pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
