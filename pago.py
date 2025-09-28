import re

class Pago:
    def __init__(self, monto, tipo, fecha):
        self.monto = monto
        self.tipo = tipo.strip()
        self.fecha = fecha.strip()
        self.registrado = False

    def es_valido(self):
        return (
            isinstance(self.monto, (int, float)) and self.monto > 0 and
            self.tipo and
            re.match(r"\d{2}/\d{2}/\d{4}", self.fecha)
        )

    def resumen(self):
        if(self.monto < 0)
            return "Monto negativo"
        else
            return f"{self.tipo} - Bs {self.monto} - {self.fecha}"






