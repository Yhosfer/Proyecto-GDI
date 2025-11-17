# dao/apoderado_dao.py
from typing import List, Dict
from config.db import get_conn

class ApoderadoDAO:
    """Acceso a datos para la tabla apoderado."""

    def listar(self, filtro: str = "") -> List[Dict]:
        """
        Lista apoderados.

        Si 'filtro' tiene texto:
          - Busca por DNI exacto (numero_documento)
          - O por apellidos que contengan ese texto.
        """
        sql = """
            SELECT apoderado_id,
                   tipo_documento_id,
                   numero_documento,
                   apellidos,
                   nombres,
                   fecha_nacimiento,
                   sexo,
                   vive,
                   vive_con_estudiante
            FROM apoderado
            WHERE (%s = '' OR numero_documento = %s OR apellidos LIKE CONCAT('%', %s, '%'))
            ORDER BY apellidos, nombres
        """
        params = (filtro, filtro, filtro)

        with get_conn() as cnx:
            cur = cnx.cursor(dictionary=True)
            cur.execute(sql, params)
            filas = cur.fetchall()
            cur.close()
        return filas
