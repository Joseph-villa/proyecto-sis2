from conexion_bd import ConexionBD
from admisiones_dao import AdmisionesDAO
from postulante import Postulante
from pago import Pago

class AdmisionesManager:
    def __init__(self):
        self.conexion = ConexionBD()
        self.dao = AdmisionesDAO(self.conexion.conn)

    def registrar_postulante(self, ci, nombre, carrera, modalidad):
        """Registra un nuevo postulante si no existe"""
        if self.dao.existe_ci(ci):
            return False
        
        postulante = Postulante(ci, nombre, carrera, modalidad)
        if not postulante.es_valido():
            return False
            
        self.dao.insertar_postulante(ci, nombre, carrera, modalidad)
        return True

    def registrar_pago(self, ci, monto, tipo, fecha):
        """Registra un pago para un postulante"""
        pago = Pago(monto, tipo, fecha)
        if not pago.es_valido():
            return False
            
        self.dao.registrar_pago(ci, monto, tipo, fecha)
        return True

    def consultar_estado(self, ci):
        """Consulta el estado de un postulante"""
        return self.dao.consultar_estado(ci)

    def publicar_resultado(self, ci, nota):
        """Publica el resultado de un postulante"""
        self.dao.actualizar_resultado(ci, nota)
        return True

    def editar_dato(self, ci, campo, nuevo_valor):
        """Edita un dato de un postulante"""
        self.dao.editar_postulante(ci, campo, nuevo_valor)
        return True

    def obtener_todos_postulantes(self):
        """Obtiene todos los postulantes"""
        self.dao.cursor.execute("SELECT ci, nombre, carrera, modalidad, estado, nota FROM postulantes")
        return self.dao.cursor.fetchall()

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos"""
        self.conexion.cerrar()
