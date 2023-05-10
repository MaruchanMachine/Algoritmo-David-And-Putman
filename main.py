"""
Alumnos: Figueroa Peña Angela Fabiana 19130188
         Espinoza Vega Enrique Manuel
         García Gutierrez Juan Antonio
"""

import re

from Modulos.Atomo import Atomo
from Modulos.Clausula import Clausula
from Modulos.Formula import Formula
def getPriority(a):
    if(a=="|"):
        return 1
    if(a=="&"):
        return 2
    if (a == ">"):
        return 3
    if (a == "="):
        return 4
    if (a == "-"):
        return 5
    if(a== "("):
        return -1
    if(a == ")"):
        return -2
    else:
        return 0
def infijo_a_postfijo(infijo):
    postfijo = []
    pila = []
    for ch in infijo:
        p=getPriority(ch)
        if p == -1:
            pila.append(ch)
        elif p == -2:
            while len(pila)>0:
                tope = pila.pop()
                if(tope != "("):
                    postfijo.append(tope)
                else:
                    break
        elif p > 0:
            if len(pila)==0 or p > getPriority(pila[-1]):
                pila.append(ch)
            else:
                while len(pila)>0 and p < getPriority(pila[-1]):
                    tope = pila.pop()
                    postfijo.append(tope)
                pila.append(ch)
        else:
            postfijo.append(ch)

    while len(pila) > 0:
        postfijo.append(pila.pop())
    return postfijo

def evaluarPosfijo(postfijo):
    pila = []
    for ch in postfijo:
        p=getPriority(ch)
        if p == 0:
            a = Atomo(ch)
            c= Clausula()
            f = Formula()
            c.addAtomo(a)
            f.addClausula(c)
            pila.append(f)
        elif p == 1:
            b = pila.pop()
            a = pila.pop()
            c = a.orFormula(b)
            pila.append(c)
        elif p == 2:
            b = pila.pop()
            a = pila.pop()
            c = a.andFormula(b)
            pila.append(c)
        elif p == 3:
            b = pila.pop()
            a = pila.pop()
            a = a.notFormula(a)
            c = a.orFormula(b)
            pila.append(c)
        elif p == 4:
            b = pila.pop()
            a = pila.pop()
            an = a.notFormula(a)
            c = an.orFormula(b)
            bn = b.notFormula(b)
            c1 = bn.orFormula(a)
            c2 = c.andFormula(c1)
            pila.append(c2)
        elif p == 5:
            a = pila.pop()
            b = a.notFormula(a)
            pila.append(b)
    return pila.pop()

def veriTaut(formula, cTaut):
    for clausula in formula.listClau:
        if clausula.isTaut():
            cTaut.append(clausula)
    for clausula in cTaut:
        formula.listClau.remove(clausula)
    return formula, cTaut

def resultForm(formula):
    result = None
    if len(formula.listClau) == 0:  # Si la formula no tiene clausulas
        result = True
    return result

def formVacia(formula,forA):
    if formula.contBif > 0:  # si la formula ya fue bifurcada
        if formula.contBif == 2:  # si es la segunda bifurcación, es insatisfactible
            result = False
        else:  # si es la primer bifurcación se vuelve a
            segB = formula.clIsBif(2, formula.forGuar)
            forA = formula.forGuar
            if dp(segB):
                forA.append(segB.aB)
                formula.contBif = 2
                result = True
            else:
                result = False
    else:
        result = False
    return result, forA, formula

def formNoVacia(formula,forA,result):
    if len(formula.listClau) == 0:
        result = True
    else:
        at = formula.clIsUnitaria()
        if at != None:
            forA.append(at)
        at2 = formula.clIsLitPura()
        if at2 != None:
            forA.append(at2)
        if at != None or at2 != None:
            pass
        else:
            Bf1 = formula.clIsBif(1, forA)
            if dp(Bf1):
                if Bf1.contBif != 2:
                    forA.append(Bf1.aB)
                result = True
            else:
                result = False
    return result, forA, formula

def resultado(result, formula,forA):
    if result:
        for atomo in forA:
            print(atomo.nombre,'=',atomo.estado)
    elif formula.contBif == 0:
        print('La fórmula es insatisfactible.')
    return result

def dp(formula):
    forA = []
    cTaut = []
    formula, cTaut = veriTaut(formula,cTaut)
    result = resultForm(formula)
    while result==None:  #mientras que el resultado sea nulo
        if formula.clIsVacia():
            result, forA, formula = formVacia(formula, forA)
        else:
            result, forA, formula = formNoVacia(formula,forA,result)
    result = resultado(result,formula,forA)
    return result


archivo = open("Data/formula11.txt")
lineas = archivo.readlines()
agregar = True
for linea in lineas:
    cadena = ''
    formula = []
    for caracter in linea:
        if caracter == '|' or caracter == '&' or caracter == '>' or caracter == '=' or caracter == '-'or caracter == '˜' or caracter == '(' or caracter == ')':
            if len(cadena) > 0:
                formula.append(cadena)
                cadena = ''
            formula.append(caracter)
        else:
            if caracter != ' ':
                cadena+=caracter
    if len(cadena) > 0 and cadena != '\n':
        formula.append(cadena)
    pos = infijo_a_postfijo(formula)
    FFinal = evaluarPosfijo(pos)
    print(f"Formula: {FFinal}")
    dp(FFinal)