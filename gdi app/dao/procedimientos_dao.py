# dao/procedimientos_dao.py
import mysql.connector
from config.db import get_conn


class ProcedimientosDAO:
    """
    DAO para ejecutar los procedimientos almacenados del módulo de consultas.
    """

    # ---------- Utilidad interna: ejecutar un SP y devolver lista de dicts ----------
    def _fetch_sp(self, nombre_sp: str, params=()):
        """
        Ejecuta un procedimiento almacenado y devuelve una lista de diccionarios.
        """
        with get_conn() as conn:
            cur = conn.cursor(dictionary=True)
            cur.callproc(nombre_sp, params)

            rows = []
            for r in cur.stored_results():
                rows = r.fetchall()

            cur.close()
        return rows

    # ---------- Búsqueda de estudiante por DNI / apellido ----------
    def obtener_estudiante_id(self, dni_o_apellido: str):
        """
        Devuelve el estudiante_id buscando por:
        - DNI exacto si es todo dígitos
        - o por apellido (LIKE) en otro caso.
        Si no encuentra nada, devuelve None.
        """
        with get_conn() as conn:
            cur = conn.cursor(dictionary=True)

            if dni_o_apellido.isdigit():
                # Prioriza coincidencia exacta de DNI
                sql = """
                    SELECT estudiante_id
                    FROM estudiante
                    WHERE numero_documento = %s
                       OR apellidos LIKE %s
                    ORDER BY (numero_documento = %s) DESC,
                             apellidos,
                             nombres
                    LIMIT 1;
                """
                cur.execute(sql, (dni_o_apellido,
                                  f"%{dni_o_apellido}%",
                                  dni_o_apellido))
            else:
                sql = """
                    SELECT estudiante_id
                    FROM estudiante
                    WHERE apellidos LIKE %s
                    ORDER BY apellidos, nombres
                    LIMIT 1;
                """
                cur.execute(sql, (f"%{dni_o_apellido}%",))

            row = cur.fetchone()
            cur.close()

        return row["estudiante_id"] if row else None

    # ---------- 1) Último control ----------
    def ultimo_control(self, est_id: int):
        return self._fetch_sp("sp_ultimo_control_estudiante", (est_id,))

    # ---------- 2) Estudiantes por país ----------
    def estudiantes_por_pais(self):
        return self._fetch_sp("sp_estudiantes_por_pais")

    # ---------- 3) Domicilio actual ----------
    def domicilio_actual(self, est_id: int):
        return self._fetch_sp("sp_domicilio_actual_estudiante", (est_id,))

    # ---------- 4) Apoderados por sexo ----------
    def apoderados_por_sexo(self):
        return self._fetch_sp("sp_apoderados_por_sexo")

    # ---------- 5) Historial controles ----------
    def historial_controles(self, est_id: int):
        return self._fetch_sp("sp_historial_controles_estudiante", (est_id,))

    # ---------- 6) Historial domicilios ----------
    def historial_domicilios(self, est_id: int):
        return self._fetch_sp("sp_historial_domicilios_estudiante", (est_id,))

    # ---------- 7) Info completa de estudiante ----------
    def info_completa(self, est_id: int):
        return self._fetch_sp("sp_info_completa_estudiante", (est_id,))

    # ---------- 8) Buscar estudiantes por apellido ----------
    def buscar_por_apellido(self, apellido: str):
        return self._fetch_sp("sp_buscar_estudiantes_apellido", (apellido,))

    # ---------- 9) Estudiantes por sexo ----------
    def estudiantes_por_sexo(self):
        return self._fetch_sp("sp_estudiantes_por_sexo")
