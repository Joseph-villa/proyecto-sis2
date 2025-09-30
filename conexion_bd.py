import mysql.connector

class ConexionBD:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConexionBD, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.db_config = {
            "host": "mysql-1c4f6993-alexxd012017-2b6e.d.aivencloud.com",
            "port": 24227,
            "user": "avnadmin",
            "password": "AVNS_PiB1kFEkACBlzX5zNzp",
            "database": "admisiones_umss2",
            "ssl_ca": "ca.pem"
        }
        self._connect()

    def _connect(self):
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            self.crear_tablas()
        except Exception as e:
            raise Exception(f"Error al conectar con la base de datos: {str(e)}")

    def get_cursor(self):
        try:
            # Verificar si la conexión está activa
            if not self.conn.is_connected():
                self._connect()  # Reconectar si está cerrada
            return self.cursor, self.conn
        except Exception as e:
            raise Exception(f"Error al obtener cursor: {str(e)}")

    def crear_tablas(self):
        try:
            self.cursor.execute("SHOW TABLES LIKE 'postulantes'")
            if not self.cursor.fetchone():
                self.cursor.execute("""
                    CREATE TABLE postulantes (
                        ci VARCHAR(20) PRIMARY KEY,
                        nombre VARCHAR(100),
                        apellido_paterno VARCHAR(100),
                        apellido_materno VARCHAR(100),
                        fecha_nacimiento VARCHAR(10),
                        telefono VARCHAR(20),
                        email VARCHAR(100),
                        direccion VARCHAR(200),
                        facultad VARCHAR(100),
                        modalidad VARCHAR(50),
                        estado VARCHAR(50),
                        nota FLOAT
                    )
                """)
            self.cursor.execute("SHOW TABLES LIKE 'pagos'")
            if not self.cursor.fetchone():
                self.cursor.execute("""
                    CREATE TABLE pagos (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        ci VARCHAR(20),
                        monto FLOAT,
                        tipo VARCHAR(50),
                        fecha VARCHAR(10),
                        transaccion VARCHAR(50),
                        registrado BOOLEAN,
                        FOREIGN KEY (ci) REFERENCES postulantes(ci) ON DELETE CASCADE
                    )
                """)
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Error al crear tablas: {str(e)}")

    def cerrar(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn and self.conn.is_connected():
                self.conn.close()
        except Exception as e:
            raise Exception(f"Error al cerrar la conexión: {str(e)}")
