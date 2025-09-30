from conexion_bd import ConexionBD
from admisiones_dao import AdmisionesDAO
from postulante import Postulante
from pago import Pago
from administrador import Administrador

class AdmisionesManager:
    def __init__(self):
        try:
            self.bd = ConexionBD()
            cursor, conn = self.bd.get_cursor()
            self.dao = AdmisionesDAO(conn)
        except Exception as e:
            raise Exception(f"Error al inicializar AdmisionesManager: {str(e)}")

    def registrar_postulante(self, ci, nombre, apellido_paterno, apellido_materno, fecha_nacimiento, telefono, email, direccion, facultad, modalidad):
        try:
            postulante = Postulante(ci, nombre, apellido_paterno, apellido_materno, fecha_nacimiento, telefono, email, direccion, facultad, modalidad)
            if not postulante.es_valido():
                return False, "Datos del postulante inválidos"
            if self.dao.existe_ci(ci):
                return False, "Ya existe un postulante con ese CI"
            self.dao.insertar_postulante(ci, nombre, apellido_paterno, apellido_materno, fecha_nacimiento, telefono, email, direccion, facultad, modalidad)
            return True, "Postulante registrado correctamente"
        except Exception as e:
            return False, f"Error al registrar postulante: {str(e)}"

    def registrar_pago(self, ci, monto, metodo, fecha, transaccion):
        try:
            pago = Pago(monto, metodo, fecha)
            if not pago.es_valido():
                return False, "Datos del pago inválidos"
            if not self.dao.existe_ci(ci):
                return False, "Postulante no encontrado"
            self.dao.registrar_pago(ci, monto, metodo, fecha, transaccion)
            return True, "Pago registrado correctamente"
        except Exception as e:
            return False, f"Error al registrar pago: {str(e)}"

    def consultar_estado(self, ci):
        try:
            estado = self.dao.consultar_estado(ci)
            if estado:
                return True, estado
            return False, "Postulante no encontrado"
        except Exception as e:
            return False, f"Error al consultar estado: {str(e)}"

    def publicar_resultado(self, ci, nota):
        try:
            if not self.dao.existe_ci(ci):
                return False, "Postulante no encontrado"
            self.dao.actualizar_resultado(ci, nota)
            return True, "Resultado publicado correctamente"
        except Exception as e:
            return False, f"Error al publicar resultado: {str(e)}"

    def editar_dato(self, ci, campo, nuevo_valor):
        try:
            if not self.dao.existe_ci(ci):
                return False, "Postulante no encontrado"
            self.dao.editar_postulante(ci, campo, nuevo_valor)
            return True, "Dato actualizado correctamente"
        except Exception as e:
            return False, f"Error al editar dato: {str(e)}"

    def eliminar_postulante(self, ci):
        try:
            self.dao.eliminar_postulante(ci)
            return True, "Postulante eliminado correctamente"
        except Exception as e:
            return False, f"Error al eliminar postulante: {str(e)}"

    def listar_postulantes(self):
        try:
            postulantes = self.dao.listar_postulantes()
            return True, postulantes
        except Exception as e:
            return False, f"Error al listar postulantes: {str(e)}"

    def verificar_admin(self, usuario, contraseña):
        try:
            admin = Administrador(usuario, contraseña)
            if admin.verificar():
                return True, "Verificación exitosa"
            return False, "Credenciales inválidas"
        except Exception as e:
            return False, f"Error al verificar administrador: {str(e)}"
