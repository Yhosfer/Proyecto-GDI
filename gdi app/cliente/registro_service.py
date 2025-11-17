# cliente/registro_service.py
from datetime import date
from config.db import get_conn


class RegistroClienteService:
    """
    Se encarga de registrar estudiante + apoderado + domicilio
    en una sola transacción.
    """

    def registrar_estudiante_completo(self, datos: dict) -> int:
        """
        datos debe tener estas claves:
        - datos["estudiante"]: dict
        - datos["apoderado"]: dict
        - datos["domicilio"]: dict
        - datos["relacion_nna_id"]: int
        - datos["control_salud"]: dict (opcional)

        Devuelve el id del estudiante creado.
        """
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                # 1) DOMICILIO
                dom = datos["domicilio"]
                cur.execute(
                    """
                    INSERT INTO domicilio (ubigeo_id, direccion_linea1,
                                           direccion_linea2, telefono)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        dom["ubigeo_id"],
                        dom["direccion_linea1"],
                        dom.get("direccion_linea2"),
                        dom.get("telefono"),
                    ),
                )
                domicilio_id = cur.lastrowid

                # 2) APODERADO
                apo = datos["apoderado"]
                cur.execute(
                    """
                    INSERT INTO apoderado (
                        tipo_documento_id, numero_documento,
                        nombres, apellidos, sexo,
                        fecha_nacimiento, vive, vive_con_estudiante
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        apo["tipo_documento_id"],
                        apo["numero_documento"],
                        apo["nombres"],
                        apo["apellidos"],
                        apo["sexo"],
                        apo["fecha_nacimiento"],
                        apo["vive"],
                        apo["vive_con_estudiante"],
                    ),
                )
                apoderado_id = cur.lastrowid

                # 3) ESTUDIANTE
                est = datos["estudiante"]
                cur.execute(
                    """
                    INSERT INTO estudiante (
                        tipo_documento_id, numero_documento,
                        nombres, apellidos, fecha_nacimiento,
                        ubigeo_nacimiento_id, pais_nacimiento_id,
                        sexo
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        est["tipo_documento_id"],
                        est["numero_documento"],
                        est["nombres"],
                        est["apellidos"],
                        est["fecha_nacimiento"],
                        est["ubigeo_nacimiento_id"],
                        est["pais_nacimiento_id"],
                        est["sexo"],
                    ),
                )
                estudiante_id = cur.lastrowid

                # 4) ESTUDIANTE_DOMICILIO (actual)
                desde = datos.get("estudiante_domicilio_desde", date.today())
                cur.execute(
                    """
                    INSERT INTO estudiante_domicilio (
                        domicilio_id, estudiante_id, desde, hasta
                    ) VALUES (%s,%s,%s,NULL)
                    """,
                    (domicilio_id, estudiante_id, desde),
                )

                # 5) ESTUDIANTE_APODERADO
                cur.execute(
                    """
                    INSERT INTO estudiante_apoderado (
                        estudiante_id, apoderado_id, relacion_nna_id
                    )
                    VALUES (%s,%s,%s)
                    """,
                    (estudiante_id, apoderado_id, datos["relacion_nna_id"]),
                )

                # 6) CONTROL_SALUD (opcional)
                ctrl = datos.get("control_salud")
                if ctrl and ctrl.get("tipo_control_id"):
                    cur.execute(
                        """
                        INSERT INTO control_salud (
                            estudiante_id, tipo_control_id, fecha,
                            resultado, observaciones
                        )
                        VALUES (%s,%s,%s,%s,%s)
                        """,
                        (
                            estudiante_id,
                            ctrl["tipo_control_id"],
                            ctrl["fecha"],
                            ctrl["resultado"],
                            ctrl.get("observaciones"),
                        ),
                    )

                conn.commit()
                return estudiante_id

            except Exception:
                conn.rollback()
                raise
            finally:
                cur.close()
