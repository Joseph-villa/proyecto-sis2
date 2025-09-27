class Administrador:
    def _init_(self, usuario, contraseña):
        self.usuario = usuario.strip()
        self.contraseña = contraseña.strip()

    def es_valido(self):
        return bool(self.usuario and self.contraseña)

    def credenciales(self):
        return {"usuario": self.usuario, "contraseña": self.contraseña}
