class Atomo:

    def __init__(self,nombre):
        self.nombre = nombre
        self.estado = True

    def negar(self):
        self.estado = not(self.estado)

    def __str__(self):
        if self.estado:
            return self.nombre
        else:
            return f"~{self.nombre}"

    def getClon(self):
        a = Atomo(self.nombre)
        a.estado = self.estado
        return a