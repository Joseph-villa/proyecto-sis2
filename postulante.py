class Postulante:
    def __init__(self, ci, nombre, carrera, modalidad):
        self.ci = ci.strip()
        self.nombre = nombre.strip()
        self.carrera = carrera.strip()
        self.modalidad = modalidad.strip()
        self.estado = "Registrado"
        self.nota = 0.0

    def es_valido(self):
        return (
            self.ci.isdigit() and len(self.ci) >= 5 and
            all([self.nombre, self.carrera, self.modalidad])
        )

    def resumen(self):
        return f"{self.nombre} ({self.ci}) - {self.carrera} [{self.modalidad}]"




