# dao/salud_dao.py
from typing import List, Dict
from config.db import get_conn

class SaludDAO:
    """Acceso a datos para controles de salud."""

    def listar_por_estudiante(self, filtro: str) -> List[Dict]:
        """
        Devuelve todos los controles de salud de los estudiantes cuyo
        DNI coincide o cuyos apellidos contienen el texto del filtro.
        """
        sql = """
            SELECT
                cs.control_salud_id,
                e.estudiante_id,
                e.numero_documento,
                e.apellidos,
                e.nombres,
                cs.tipo_control_id,
                cs.fecha,
                cs.resultado,
                cs.observaciones
            FROM control_salud cs
            JOIN estudiante e ON e.estudiante_id = cs.estudiante_id
            WHERE (e.numero_documento = %s OR e.apellidos LIKE CONCAT('%', %s, '%'))
            ORDER BY e.apellidos, e.nombres, cs.fecha DESC
        """
        params = (filtro, filtro)

        with get_conn() as cnx:
            cur = cnx.cursor(dictionary=True)
            cur.execute(sql, params)
            filas = cur.fetchall()
            cur.close()
        return filas
