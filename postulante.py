class Postulante:
    def __init__(self, ci, nombre, carrera, modalidad):
        self.ci = ci.strip()
        self.nombre = nombre.strip()
        self.carrera = carrera.strip()
        self.modalidad = modalidad.strip()
        self.estado = "Registrado"
        self.nota = 0.0
