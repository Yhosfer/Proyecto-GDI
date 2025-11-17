# dao/domicilio_dao.py
from typing import List, Dict
from config.db import get_conn

class DomicilioDAO:
    """Acceso a datos para domicilio + historial estudiante_domicilio."""

    def listar(self, filtro: str = "") -> List[Dict]:
        """
        Lista domicilios de estudiantes (historial).

        Si 'filtro' tiene texto:
          - Busca por DNI del estudiante
          - O por apellidos del estudiante.
        """
        sql = """
            SELECT
                ed.estudiante_domicilio_id,
                e.estudiante_id,
                e.numero_documento,
                e.apellidos,
                e.nombres,
                d.domicilio_id,
                d.direccion_linea1,
                d.direccion_linea2,
                d.ubigeo_id,
                d.telefono,
                ed.desde,
                ed.hasta
            FROM estudiante_domicilio ed
            JOIN estudiante e   ON e.estudiante_id = ed.estudiante_id
            JOIN domicilio d    ON d.domicilio_id = ed.domicilio_id
            WHERE (%s = '' OR e.numero_documento = %s OR e.apellidos LIKE CONCAT('%', %s, '%'))
            ORDER BY e.apellidos, e.nombres, ed.desde DESC
        """
        params = (filtro, filtro, filtro)

        with get_conn() as cnx:
            cur = cnx.cursor(dictionary=True)
            cur.execute(sql, params)
            filas = cur.fetchall()
            cur.close()
        return filas
