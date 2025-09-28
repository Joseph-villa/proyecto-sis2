class Administrador:
    def __init__(self, id_admin=None, nombre=None, apellido=None, email=None, password=None):
        self.id_admin = id_admin
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.password = password

    def __str__(self):
        return f"Administrador: {self.nombre} {self.apellido}"
