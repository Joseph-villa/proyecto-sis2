class AdmisionesDAO:
    def __init__(self, conexion):
        self.cursor = conexion.cursor()
        self.conn = conexion

    def existe_ci(self, ci):
        try:
            self.cursor.execute("SELECT ci FROM postulantes WHERE ci = %s", (ci,))
            return self.cursor.fetchone() is not None
        except Exception as e:
            raise Exception(f"Error al verificar CI: {str(e)}")

    def insertar_postulante(self, ci, nombre, apellido_paterno, apellido_materno, fecha_nacimiento, telefono, email, direccion, facultad, modalidad):
        try:
            self.cursor.execute("""
                INSERT INTO postulantes (ci, nombre, apellido_paterno, apellido_materno, fecha_nacimiento, telefono, email, direccion, facultad, modalidad, estado, nota)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (ci, nombre, apellido_paterno, apellido_materno, fecha_nacimiento, telefono, email, direccion, facultad, modalidad, "Registrado", 0.0))
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Error al insertar postulante: {str(e)}")

    def registrar_pago(self, ci, monto, metodo, fecha, transaccion):
        try:
            self.cursor.execute("""
                INSERT INTO pagos (ci, monto, tipo, fecha, transaccion, registrado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (ci, monto, metodo, fecha, transaccion, True))
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Error al registrar pago: {str(e)}")

    def consultar_estado(self, ci):
        try:
            self.cursor.execute("SELECT estado, nota FROM postulantes WHERE ci = %s", (ci,))
            return self.cursor.fetchone()
        except Exception as e:
            raise Exception(f"Error al consultar estado: {str(e)}")

    def actualizar_resultado(self, ci, nota):
        try:
            if (nota < 0 or nota > 100):
                raise Exception("La nota debe estar entre 0 y 100")
            estado = "Admitido" if nota >= 51 else "No admitido"
            self.cursor.execute("""
                UPDATE postulantes SET nota = %s, estado = %s WHERE ci = %s
            """, (nota, estado, ci))
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Error al actualizar resultado: {str(e)}")

    def editar_postulante(self, ci, campo, nuevo_valor):
        try:
            if campo in ["nombre", "apellido_paterno", "apellido_materno", "fecha_nacimiento", "telefono", "email", "direccion", "facultad", "modalidad"]:
                self.cursor.execute(f"UPDATE postulantes SET {campo} = %s WHERE ci = %s", (nuevo_valor, ci))
                self.conn.commit()
            else:
                raise Exception("Campo no válido")
        except Exception as e:
            raise Exception(f"Error al editar postulante: {str(e)}")

    def eliminar_postulante(self, ci):
        try:
            self.cursor.execute("SELECT ci FROM postulantes WHERE ci = %s", (ci,))
            if not self.cursor.fetchone():
                raise Exception("Postulante no encontrado")
            self.cursor.execute("DELETE FROM postulantes WHERE ci = %s", (ci,))
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Error al eliminar postulante: {str(e)}")

    def listar_postulantes(self):
        try:
            self.cursor.execute("""
                SELECT p.ci, p.nombre, p.apellido_paterno, p.apellido_materno, p.fecha_nacimiento, p.telefono, p.email, p.direccion, p.facultad, p.modalidad, p.estado, p.nota,
                CASE WHEN EXISTS (SELECT 1 FROM pagos pg WHERE pg.ci = p.ci) THEN 'Sí' ELSE 'No' END AS pago
                FROM postulantes p
            """)
            return self.cursor.fetchall()
        except Exception as e:
            raise Exception(f"Error al listar postulantes: {str(e)}")
