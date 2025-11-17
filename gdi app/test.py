import mysql.connector

def probar_conexion():
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="sasasa2006",
        database="colegiopalermo",
        charset="utf8mb4"
    )
    cur = cnx.cursor()
    cur.execute("SELECT COUNT(*) FROM estudiante")
    total = cur.fetchone()[0]
    cur.close()
    cnx.close()
    print("Estudiantes registrados:", total)

if __name__ == "__main__":
    probar_conexion()