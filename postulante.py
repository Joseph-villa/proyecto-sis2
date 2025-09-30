import re
from datetime import datetime

class Postulante:
    def __init__(self, ci, nombre, apellido_paterno, apellido_materno, fecha_nacimiento, telefono, email, direccion, facultad, modalidad):
        self.ci = ci.strip()
        self.nombre = nombre.strip()
        self.apellido_paterno = apellido_paterno.strip()
        self.apellido_materno = apellido_materno.strip()
        self.fecha_nacimiento = fecha_nacimiento.strip()
        self.telefono = telefono.strip()
        self.email = email.strip()
        self.direccion = direccion.strip()
        self.facultad = facultad.strip()
        self.modalidad = modalidad.strip()
        self.estado = "Registrado"
        self.nota = 0.0

    def es_valido(self):
        if not (self.ci.isdigit() and 5 <= len(self.ci) <= 10):  # Corregido el operador lógico
            return False

        required = [
            self.nombre, self.apellido_paterno, self.apellido_materno,
            self.fecha_nacimiento, self.telefono, self.email,
            self.direccion, self.facultad, self.modalidad
        ]
        if not all(field and field.strip() for field in required):
            return False

        try:
            nacimiento = datetime.strptime(self.fecha_nacimiento, "%d/%m/%Y")
        except ValueError:
            return False

        hoy = datetime.today()
        edad = hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
        if not (12 <= edad <= 150):
            return False

        email_re = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
        if not email_re.fullmatch(self.email):
            return False

        return True

    def resumen(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno} ({self.ci}) - {self.facultad} [{self.modalidad}]"
