from Modulos.Clausula import Clausula
import copy


class Formula:
    def __init__(self):
        self.listClau = []
        self.forGuar = []
        self.contBif = 0
        self.aB = None
        self.clausulasFB = []

    def addClausula(self, clausula):
        self.listClau.append(clausula)

    def addClausulaBif(self, clausula):
        self.clausulasFB.append(clausula)

    def __str__(self):
        cadena = '['
        lista = []
        for a in self.listClau:
            lista.append(str(a))
        cadena += ' '.join(lista)
        cadena += ']'
        return str(cadena)

    def andFormula(self, formula):
        f = Formula()
        for c in self.listClau:
            f.addClausula(c.getClon())
        for c in formula.listClau:
            f.addClausula(c.getClon())
        return f

    def orFormulaAux(self, formula, clausula):
        for c in self.listClau:
            clon = c.getClon()
            for a in clausula.atomos:
                clon.addAtomo(a)
            formula.addClausula(clon)

    def orFormula(self, formula):
        f = Formula()
        for c in formula.listClau:
            self.orFormulaAux(f, c)
        return f

    def notFormula(self, formula):
        result = Formula()
        clone = Formula()
        if len(formula.listClau) == 1:
            cl = Clausula()
            for a in formula.listClau[0].atomos:
                cl.addAtomo(a)
            for a in cl.atomos:
                a.negar()
                clN = Clausula()
                clN.addAtomo(a)
                result.addClausula(clN)
            return result
        for c in formula.listClau:
            clone.addClausula(c.getClon())
        for c in clone.listClau:
            for a in c.atomos:
                a.negar()
        while (len(clone.listClau) > 0):
            c = clone.listClau.pop()
            for a in c.atomos:
                for c2 in clone.listClau:
                    for a2 in c2.atomos:
                        cl = Clausula()
                        cl.addAtomo(a)
                        cl.addAtomo(a2)
                        result.addClausula(cl)
        return result

    def clIsVacia(self):
        for clausula in self.listClau:
            if len(clausula.atomos) == 0:
                return True
        return False

    def clIsUnitaria(self):
        atomos_unitarios = []
        for clausula in self.listClau:
            if len(clausula.atomos) == 1:
                atomos_unitarios.append(clausula.atomos[0].getClon())
        if len(atomos_unitarios) > 0:
            clausulasElim = []
            for clausulaaux in self.listClau:
                for a in clausulaaux.atomos:
                    if a.nombre == atomos_unitarios[0].nombre \
                            and a.estado == atomos_unitarios[0].estado:
                        clausulasElim.append(clausulaaux)
            for clausulaElim in clausulasElim:
                self.listClau.remove(clausulaElim)
            for clausula in self.listClau:
                atomosElim = []
                for atomo in clausula.atomos:
                    if atomos_unitarios[0].nombre == atomo.nombre:
                        atomosElim.append(atomo)
                for atomoElim in atomosElim:
                    clausula.atomos.remove(atomoElim)
            return atomos_unitarios[0]
        return None

    def clIsLitPura(self):
        atomos = []
        for clausula in self.listClau:
            for atomo in clausula.atomos:
                guardar = True
                for atomoaux in atomos:
                    if atomo.nombre == atomoaux.nombre:
                        guardar = False
                if guardar:
                    atomos.append(atomo)
        atomosElim = []
        for a in atomos:
            for clausula in self.listClau:
                for a2 in clausula.atomos:
                    if a2.nombre == a.nombre and a2.estado != a.estado:
                        if a not in atomosElim:
                            atomosElim.append(a)
        for a in atomosElim:
            atomos.remove(a)
        if len(atomos) > 0:
            clausulasElim = []
            for clausula in self.listClau:
                for a2 in clausula.atomos:
                    if a2.nombre == atomos[0].nombre:
                        clausulasElim.append(clausula)

            for clausulaElim in clausulasElim:
                self.listClau.remove(clausulaElim)
            return atomos[0]
        return None

    def clIsBif(self, contBif, forG):
        if contBif == 2:
            self.listClau = self.clausulasFB
        atomoaux = self.listClau[0].atomos[0].getClon()
        if contBif == 2:
            atomoaux.negar()
        formula = Formula()
        formula.aB = atomoaux
        formula.contBif = contBif
        for c in self.listClau:
            formula.addClausula(c.getClon())
        if contBif == 1:
            self.forGuar = copy.copy(forG)
            for c in self.listClau:
                formula.addClausulaBif(c.getClon())
        clElim = []
        for clausula in formula.listClau:
            for atomo in clausula.atomos:
                if atomo.nombre == atomoaux.nombre and atomo.estado == atomoaux.estado:
                    clElim.append(clausula)
        for clausulaElim in clElim:
            formula.listClau.remove(clausulaElim)
        for clausula in formula.listClau:
            atomElim = []
            for atom2 in clausula.atomos:
                if atomoaux.nombre == atom2.nombre:
                    atomElim.append(atom2)
            for aElim in atomElim:
                clausula.atomos.remove(aElim)
        return formula
