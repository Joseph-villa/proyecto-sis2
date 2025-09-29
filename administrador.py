class Administrador:
    def __init__(self, usuario, contraseña):
        self.usuario = usuario.strip()
        self.contraseña = contraseña.strip()

    def es_valido(self):
        return bool(self.usuario and self.contraseña)

    def verificar(self):
        return self.es_valido() and self.usuario == "admin" and self.contraseña == "123456"
