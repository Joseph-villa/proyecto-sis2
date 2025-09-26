import mysql.connector

class ConexionBD:
    def __init__(self):
        self.db_config = {
            "host": "mysql-1c4f6993-alexxd012017-2b6e.d.aivencloud.com",
            "port": 24227,
            "user": "avnadmin",
            "password": "AVNS_PiB1kFEkACBlzX5zNzp",
            "database": "carreras_db",
            "ssl_ca": "ca.pem"
        }
        self.conn = mysql.connector.connect(**self.db_config)
        self.cursor = self.conn.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS postulantes(
                ci VARCHAR(20) PRIMARY KEY,
                nombre VARCHAR(100),
                carrera VARCHAR(100),
                modalidad VARCHAR(50),
                estado VARCHAR(50),
                nota FLOAT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pagos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ci VARCHAR(20),
                monto FLOAT,
                tipo VARCHAR(50),
                fecha VARCHAR(50),
                registrado BOOLEAN,
                FOREIGN KEY (ci) REFERENCES postulantes(ci)
            )
        """)
        self.conn.commit()

    def cerrar(self):
        self.cursor.close()
        self.conn.close()



