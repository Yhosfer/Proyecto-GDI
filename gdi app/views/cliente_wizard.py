# views/cliente_wizard.py  (o donde la tengas)

from tkinter import messagebox
from tkinter import ttk
from datetime import date

from ui.base import BaseModuleFrame   # mismo que usas para Estudiantes, etc.
from cliente.registro_service import RegistroClienteService


class ClienteWizard(BaseModuleFrame):
    def __init__(self, parent, on_exit_to_home):
        super().__init__(
            parent,
            "Registro rápido de estudiante",
            "Ingresa los datos mínimos del estudiante, apoderado y domicilio."
        )
        self.on_exit_to_home = on_exit_to_home
        self.service = RegistroClienteService()

        body = self.body

        # ----- BLOQUE ESTUDIANTE -----
        frame_est = ttk.LabelFrame(body, text="Datos del estudiante")
        frame_est.pack(fill="x", padx=10, pady=5)

        self.est_tipo_doc = ttk.Entry(frame_est, width=5)
        self.est_num_doc = ttk.Entry(frame_est, width=15)
        self.est_nombres = ttk.Entry(frame_est, width=30)
        self.est_apellidos = ttk.Entry(frame_est, width=30)
        self.est_fecha_nac = ttk.Entry(frame_est, width=10)  # yyyy-mm-dd
        self.est_ubigeo_nac = ttk.Entry(frame_est, width=5)
        self.est_pais_nac = ttk.Entry(frame_est, width=5)
        self.est_sexo = ttk.Entry(frame_est, width=2)  # M / F

        row = 0
        ttk.Label(frame_est, text="Tipo Doc (id):").grid(row=row, column=0, sticky="e")
        self.est_tipo_doc.grid(row=row, column=1, sticky="w", padx=3)
        ttk.Label(frame_est, text="N° Doc:").grid(row=row, column=2, sticky="e")
        self.est_num_doc.grid(row=row, column=3, sticky="w", padx=3)

        row += 1
        ttk.Label(frame_est, text="Nombres:").grid(row=row, column=0, sticky="e")
        self.est_nombres.grid(row=row, column=1, columnspan=3, sticky="we", padx=3)

        row += 1
        ttk.Label(frame_est, text="Apellidos:").grid(row=row, column=0, sticky="e")
        self.est_apellidos.grid(row=row, column=1, columnspan=3, sticky="we", padx=3)

        row += 1
        ttk.Label(frame_est, text="F. Nac (YYYY-MM-DD):").grid(row=row, column=0, sticky="e")
        self.est_fecha_nac.grid(row=row, column=1, sticky="w", padx=3)
        ttk.Label(frame_est, text="Ubigeo nac (id):").grid(row=row, column=2, sticky="e")
        self.est_ubigeo_nac.grid(row=row, column=3, sticky="w", padx=3)

        row += 1
        ttk.Label(frame_est, text="País nac (id):").grid(row=row, column=0, sticky="e")
        self.est_pais_nac.grid(row=row, column=1, sticky="w", padx=3)
        ttk.Label(frame_est, text="Sexo (M/F):").grid(row=row, column=2, sticky="e")
        self.est_sexo.grid(row=row, column=3, sticky="w", padx=3)

        for c in range(4):
            frame_est.columnconfigure(c, weight=1)

        # ----- BLOQUE APODERADO -----
        frame_apo = ttk.LabelFrame(body, text="Apoderado principal")
        frame_apo.pack(fill="x", padx=10, pady=5)

        self.apo_tipo_doc = ttk.Entry(frame_apo, width=5)
        self.apo_num_doc = ttk.Entry(frame_apo, width=15)
        self.apo_nombres = ttk.Entry(frame_apo, width=30)
        self.apo_apellidos = ttk.Entry(frame_apo, width=30)
        self.apo_sexo = ttk.Entry(frame_apo, width=2)
        self.apo_fecha_nac = ttk.Entry(frame_apo, width=10)
        self.apo_vive = ttk.Entry(frame_apo, width=2)  # 1/0
        self.apo_vive_con = ttk.Entry(frame_apo, width=2)  # 1/0
        self.apo_relacion = ttk.Entry(frame_apo, width=3)  # relacion_nna_id

        row = 0
        ttk.Label(frame_apo, text="Tipo Doc (id):").grid(row=row, column=0, sticky="e")
        self.apo_tipo_doc.grid(row=row, column=1, sticky="w", padx=3)
        ttk.Label(frame_apo, text="N° Doc:").grid(row=row, column=2, sticky="e")
        self.apo_num_doc.grid(row=row, column=3, sticky="w", padx=3)

        row += 1
        ttk.Label(frame_apo, text="Nombres:").grid(row=row, column=0, sticky="e")
        self.apo_nombres.grid(row=row, column=1, columnspan=3, sticky="we", padx=3)

        row += 1
        ttk.Label(frame_apo, text="Apellidos:").grid(row=row, column=0, sticky="e")
        self.apo_apellidos.grid(row=row, column=1, columnspan=3, sticky="we", padx=3)

        row += 1
        ttk.Label(frame_apo, text="Sexo (M/F):").grid(row=row, column=0, sticky="e")
        self.apo_sexo.grid(row=row, column=1, sticky="w", padx=3)
        ttk.Label(frame_apo, text="F. Nac:").grid(row=row, column=2, sticky="e")
        self.apo_fecha_nac.grid(row=row, column=3, sticky="w", padx=3)

        row += 1
        ttk.Label(frame_apo, text="Vive (1/0):").grid(row=row, column=0, sticky="e")
        self.apo_vive.grid(row=row, column=1, sticky="w", padx=3)
        ttk.Label(frame_apo, text="Vive con estudiante (1/0):").grid(row=row, column=2, sticky="e")
        self.apo_vive_con.grid(row=row, column=3, sticky="w", padx=3)

        row += 1
        ttk.Label(frame_apo, text="Relación (id relacion_nna):").grid(row=row, column=0, sticky="e")
        self.apo_relacion.grid(row=row, column=1, sticky="w", padx=3)

        for c in range(4):
            frame_apo.columnconfigure(c, weight=1)

        # ----- BLOQUE DOMICILIO -----
        frame_dom = ttk.LabelFrame(body, text="Domicilio actual")
        frame_dom.pack(fill="x", padx=10, pady=5)

        self.dom_ubigeo = ttk.Entry(frame_dom, width=5)
        self.dom_linea1 = ttk.Entry(frame_dom, width=40)
        self.dom_linea2 = ttk.Entry(frame_dom, width=40)
        self.dom_tel = ttk.Entry(frame_dom, width=15)

        row = 0
        ttk.Label(frame_dom, text="Ubigeo (id):").grid(row=row, column=0, sticky="e")
        self.dom_ubigeo.grid(row=row, column=1, sticky="w", padx=3)
        ttk.Label(frame_dom, text="Teléfono:").grid(row=row, column=2, sticky="e")
        self.dom_tel.grid(row=row, column=3, sticky="w", padx=3)

        row += 1
        ttk.Label(frame_dom, text="Dirección línea 1:").grid(row=row, column=0, sticky="e")
        self.dom_linea1.grid(row=row, column=1, columnspan=3, sticky="we", padx=3)

        row += 1
        ttk.Label(frame_dom, text="Dirección línea 2:").grid(row=row, column=0, sticky="e")
        self.dom_linea2.grid(row=row, column=1, columnspan=3, sticky="we", padx=3)

        for c in range(4):
            frame_dom.columnconfigure(c, weight=1)

        # ----- BLOQUE CONTROL SALUD (simple) -----
        frame_salud = ttk.LabelFrame(body, text="Control de salud inicial (opcional)")
        frame_salud.pack(fill="x", padx=10, pady=5)

        self.ctrl_tipo = ttk.Entry(frame_salud, width=5)   # tipo_control_id
        self.ctrl_fecha = ttk.Entry(frame_salud, width=10) # yyyy-mm-dd
        self.ctrl_resultado = ttk.Entry(frame_salud, width=20)
        self.ctrl_observ = ttk.Entry(frame_salud, width=30)

        row = 0
        ttk.Label(frame_salud, text="Tipo control (id):").grid(row=row, column=0, sticky="e")
        self.ctrl_tipo.grid(row=row, column=1, sticky="w", padx=3)
        ttk.Label(frame_salud, text="Fecha:").grid(row=row, column=2, sticky="e")
        self.ctrl_fecha.grid(row=row, column=3, sticky="w", padx=3)

        row += 1
        ttk.Label(frame_salud, text="Resultado:").grid(row=row, column=0, sticky="e")
        self.ctrl_resultado.grid(row=row, column=1, columnspan=3, sticky="we", padx=3)

        row += 1
        ttk.Label(frame_salud, text="Observaciones:").grid(row=row, column=0, sticky="e")
        self.ctrl_observ.grid(row=row, column=1, columnspan=3, sticky="we", padx=3)

        for c in range(4):
            frame_salud.columnconfigure(c, weight=1)

        # ----- BOTONES -----
        footer = ttk.Frame(body)
        footer.pack(fill="x", padx=10, pady=10)

        ttk.Button(footer, text="Cancelar", command=self._cancel).pack(side="right")
        ttk.Button(footer, text="Guardar", command=self._guardar).pack(side="right", padx=(0, 8))

    # ----------------- LÓGICA -----------------

    def _cancel(self):
        if messagebox.askyesno("Cancelar", "¿Deseas salir sin guardar?"):
            self.on_exit_to_home()

    def _guardar(self):
        try:
            datos = self._collect_data()
            est_id = self.service.registrar_estudiante_completo(datos)
            messagebox.showinfo("Éxito", f"Estudiante registrado con id {est_id}.")
            self.on_exit_to_home()
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))

    def _collect_data(self):
        # En producción convendría validar; aquí lo dejamos directo para que funcione ya.
        est = {
            "tipo_documento_id": int(self.est_tipo_doc.get()),
            "numero_documento": self.est_num_doc.get().strip(),
            "nombres": self.est_nombres.get().strip(),
            "apellidos": self.est_apellidos.get().strip(),
            "fecha_nacimiento": self.est_fecha_nac.get().strip(),
            "ubigeo_nacimiento_id": int(self.est_ubigeo_nac.get()),
            "pais_nacimiento_id": int(self.est_pais_nac.get()),
            "sexo": self.est_sexo.get().strip()[:1].upper(),
        }

        apo = {
            "tipo_documento_id": int(self.apo_tipo_doc.get()),
            "numero_documento": self.apo_num_doc.get().strip(),
            "nombres": self.apo_nombres.get().strip(),
            "apellidos": self.apo_apellidos.get().strip(),
            "sexo": self.apo_sexo.get().strip()[:1].upper(),
            "fecha_nacimiento": self.apo_fecha_nac.get().strip(),
            "vive": int(self.apo_vive.get() or "1"),
            "vive_con_estudiante": int(self.apo_vive_con.get() or "1"),
        }

        dom = {
            "ubigeo_id": int(self.dom_ubigeo.get()),
            "direccion_linea1": self.dom_linea1.get().strip(),
            "direccion_linea2": self.dom_linea2.get().strip() or None,
            "telefono": self.dom_tel.get().strip() or None,
        }

        relacion_id = int(self.apo_relacion.get())

        ctrl = {}
        if self.ctrl_tipo.get().strip():
            ctrl = {
                "tipo_control_id": int(self.ctrl_tipo.get()),
                "fecha": self.ctrl_fecha.get().strip() or date.today().isoformat(),
                "resultado": self.ctrl_resultado.get().strip() or "Sin registro",
                "observaciones": self.ctrl_observ.get().strip() or None,
            }

        return {
            "estudiante": est,
            "apoderado": apo,
            "domicilio": dom,
            "relacion_nna_id": relacion_id,
            "control_salud": ctrl,
            "estudiante_domicilio_desde": date.today(),
        }
