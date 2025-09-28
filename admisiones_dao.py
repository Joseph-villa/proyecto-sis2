from conexion_bd import ConexionBD
from postulante import Postulante
from pago import Pago
from administrador import Administrador
from datetime import datetime

class AdmisionesDAO:
    def __init__(self):
        self.conexion_bd = ConexionBD()
        self.facultades_umss = [
            "Facultad de Ciencias y Tecnología",
            "Facultad de Medicina",
            "Facultad de Odontología", 
            "Facultad de Arquitectura y Ciencias del Hábitat",
            "Facultad de Ciencias Económicas",
            "Facultad de Humanidades y Ciencias de la Educación",
            "Facultad de Ciencias Agrícolas y Pecuarias",
            "Facultad de Bioquímica y Farmacia",
            "Facultad de Enfermería",
            "Facultad de Ciencias Jurídicas y Políticas"
        ]

    def obtener_facultades(self):
        """Retorna la lista de facultades disponibles en UMSS"""
        return self.facultades_umss

    def registrar_postulante(self, postulante):
        try:
            errores = postulante.validar_datos()
            if errores:
                return {"success": False, "error": "Datos inválidos", "detalles": errores}
            
            if self.buscar_postulante(postulante.ci):
                return {"success": False, "error": "CI ya registrado", "detalles": ["Ya existe un postulante con este CI"]}
            
            if self.conexion_bd.conectar():
                cursor = self.conexion_bd.obtener_conexion().cursor()
                query = """INSERT INTO postulantes (ci, nombre, apellido, telefono, email, facultad, colegio, fecha_nacimiento) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                valores = (postulante.ci, postulante.nombre, postulante.apellido, 
                          postulante.telefono, postulante.email, postulante.facultad, 
                          postulante.colegio, postulante.fecha_nacimiento)
                cursor.execute(query, valores)
                self.conexion_bd.obtener_conexion().commit()
                cursor.close()
                self.conexion_bd.desconectar()
                return {"success": True, "mensaje": "Postulante registrado exitosamente"}
        except Exception as e:
            error_msg = str(e)
            if "Duplicate entry" in error_msg:
                return {"success": False, "error": "CI duplicado", "detalles": ["Ya existe un postulante con este CI"]}
            elif "cannot be null" in error_msg:
                return {"success": False, "error": "Campo requerido faltante", "detalles": ["Todos los campos son obligatorios"]}
            else:
                return {"success": False, "error": "Error de base de datos", "detalles": [f"Error técnico: {error_msg}"]}

    def buscar_postulante(self, ci):
        try:
            if self.conexion_bd.conectar():
                cursor = self.conexion_bd.obtener_conexion().cursor()
                query = "SELECT * FROM postulantes WHERE ci = %s"
                cursor.execute(query, (ci,))
                resultado = cursor.fetchone()
                cursor.close()
                self.conexion_bd.desconectar()
                
                if resultado:
                    return Postulante(*resultado)
                return None
        except Exception as e:
            print(f"Error al buscar postulante: {e}")
            return None

    def registrar_pago(self, pago):
        try:
            if self.conexion_bd.conectar():
                cursor = self.conexion_bd.obtener_conexion().cursor()
                query = """INSERT INTO pagos (ci_postulante, monto, fecha_pago, metodo_pago, estado) 
                          VALUES (%s, %s, %s, %s, %s)"""
                valores = (pago.ci_postulante, pago.monto, pago.fecha_pago, 
                          pago.metodo_pago, pago.estado)
                cursor.execute(query, valores)
                self.conexion_bd.obtener_conexion().commit()
                cursor.close()
                self.conexion_bd.desconectar()
                return True
        except Exception as e:
            print(f"Error al registrar pago: {e}")
            return False

    def obtener_todos_postulantes(self):
        try:
            if self.conexion_bd.conectar():
                cursor = self.conexion_bd.obtener_conexion().cursor()
                query = "SELECT * FROM postulantes"
                cursor.execute(query)
                resultados = cursor.fetchall()
                cursor.close()
                self.conexion_bd.desconectar()
                
                postulantes = []
                for resultado in resultados:
                    postulantes.append(Postulante(*resultado))
                return postulantes
        except Exception as e:
            print(f"Error al obtener postulantes: {e}")
            return []

    def verificar_pago(self, ci):
        try:
            if self.conexion_bd.conectar():
                cursor = self.conexion_bd.obtener_conexion().cursor()
                query = "SELECT * FROM pagos WHERE ci_postulante = %s AND estado = 'Aprobado'"
                cursor.execute(query, (ci,))
                resultado = cursor.fetchone()
                cursor.close()
                self.conexion_bd.desconectar()
                return resultado is not None
        except Exception as e:
            print(f"Error al verificar pago: {e}")
            return False
