# dao/catalogos_dao.py

from typing import Optional

class PaisDAO:
    @staticmethod
    def get_or_create_by_nombre(conn, nombre_pais: str, iso3: str = "UNK") -> int:
        """
        Busca un país por nombre (case-insensitive).
        Si no existe, lo crea con el iso3 dado (por defecto 'UNK').
        Devuelve pais_nacimiento_id.
        """
        nombre_pais = nombre_pais.strip()
        if not nombre_pais:
            raise ValueError("El nombre de país no puede estar vacío")

        cur = conn.cursor()
        cur.execute("""
            SELECT pais_nacimiento_id
            FROM pais
            WHERE LOWER(nombre) = LOWER(%s)
        """, (nombre_pais,))
        row = cur.fetchone()
        if row:
            cur.close()
            return row[0]

        # crear país nuevo
        cur.execute("""
            INSERT INTO pais(nombre, iso3)
            VALUES (%s, %s)
        """, (nombre_pais, iso3))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        return new_id


class UbigeoDAO:
    @staticmethod
    def get_or_create_by_codigo(conn, codigo: str,
                                departamento: str = "",
                                provincia: str = "",
                                distrito: str = "") -> int:
        """
        Trabaja con el código de ubigeo (lo que escribe el usuario).
        Si el código existe, devuelve su id (codigo_ubigeo).
        Si no existe, lo crea con nombres genéricos o los que mandes.
        """
        codigo = codigo.strip()
        if not codigo:
            raise ValueError("El código de ubigeo no puede estar vacío")

        cur = conn.cursor()
        cur.execute("""
            SELECT codigo_ubigeo
            FROM ubigeo
            WHERE codigo_ubigeo = %s
        """, (codigo,))
        row = cur.fetchone()
        if row:
            cur.close()
            return row[0]

        # Si no existe, lo creamos. Aquí puedes ajustar departamento/provincia/distrito.
        if not departamento:
            departamento = "SIN-DEPARTAMENTO"
        if not provincia:
            provincia = "SIN-PROVINCIA"
        if not distrito:
            distrito = "SIN-DISTRITO"

        cur.execute("""
            INSERT INTO ubigeo(codigo_ubigeo, departamento, provincia, distrito)
            VALUES (%s, %s, %s, %s)
        """, (codigo, departamento, provincia, distrito))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        return new_id


class TipoDocumentoDAO:
    @staticmethod
    def get_id_by_nombre(conn, nombre_doc: str) -> int:
        """
        Devuelve tipo_documento_id a partir del nombre ('DNI','CE','PASAPORTE').
        """
        nombre_doc = nombre_doc.strip()
        cur = conn.cursor()
        cur.execute("""
            SELECT tipo_documento_id
            FROM tipo_documento
            WHERE nombre = %s
        """, (nombre_doc,))
        row = cur.fetchone()
        cur.close()
        if not row:
            raise ValueError(f"Tipo de documento no válido: {nombre_doc}")
        return row[0]


class RelacionNNADAO:
    @staticmethod
    def get_id_by_nombre(conn, nombre_rel: str) -> int:
        """
        Devuelve relacion_id (relación NNA) a partir de 'Padre','Madre','Tutor'.
        """
        nombre_rel = nombre_rel.strip()
        cur = conn.cursor()
        cur.execute("""
            SELECT relacion_id
            FROM relacion_nna
            WHERE nombre = %s
        """, (nombre_rel,))
        row = cur.fetchone()
        cur.close()
        if not row:
            raise ValueError(f"Relación NNA no válida: {nombre_rel}")
        return row[0]


class TipoControlSaludDAO:
    @staticmethod
    def get_or_create_by_nombre(conn, nombre: str) -> int:
        """
        Busca un tipo de control por nombre. Si no existe, lo crea.
        Devuelve tipo_control_id.
        """
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre de tipo de control no puede estar vacío")

        cur = conn.cursor()
        cur.execute("""
            SELECT tipo_control_id
            FROM tipo_control_salud
            WHERE LOWER(nombre) = LOWER(%s)
        """, (nombre,))
        row = cur.fetchone()
        if row:
            cur.close()
            return row[0]

        # crear si no existe
        cur.execute("""
            INSERT INTO tipo_control_salud(nombre)
            VALUES (%s)
        """, (nombre,))
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        return new_id
