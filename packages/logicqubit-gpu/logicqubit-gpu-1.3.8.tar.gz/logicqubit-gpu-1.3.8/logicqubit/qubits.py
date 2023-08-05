#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Author Cleoner S. Pietralonga
# e-mail: cleonerp@gmail.com
# Apache License

import sympy as sp
from sympy.physics.quantum import TensorProduct
from IPython.display import display, Math, Latex

from logicqubit.hilbert import *
from logicqubit.gates import *
from logicqubit.circuit import *
from logicqubit.utils import *

class Qubits(Hilbert):

    def __init__(self, qubits_number, symbolic, first_left):
        Qubits.__q_number = qubits_number
        Qubits.__symbolic = symbolic
        Qubits.first_left = first_left
        Qubits.__number = 0
        Qubits.__used_qubits = []
        Qubits.__measured_qubits = []
        Qubits.__measured_values = []
        if(not Qubits.__symbolic):
            Qubits.__psi = self.kronProduct([self.ket(0) for i in range(Qubits.__q_number)])
        else:
            if(Qubits.first_left):  # o qubit 1 é o primeiro a esquerda
                a = sp.symbols([str(i) + "a" + str(i) + "_0" for i in range(1, Qubits.__q_number + 1)])
                b = sp.symbols([str(i) + "b" + str(i) + "_1" for i in range(1, Qubits.__q_number + 1)])
            else:
                a = sp.symbols([str(Qubits.__q_number+1-i) + "a" + str(i) + "_0" for i in reversed(range(1, Qubits.__q_number + 1))])
                b = sp.symbols([str(Qubits.__q_number+1-i) + "b" + str(i) + "_1" for i in reversed(range(1, Qubits.__q_number + 1))])
            Qubits.__psi = self.kronProduct([a[i]*self.ket(0)+b[i]*self.ket(1) for i in range(Qubits.__q_number)])

    def addQubit(self, id=None):
        if(len(Qubits.__used_qubits) < Qubits.__q_number):
            if(id != None):
                if(not id in Qubits.__used_qubits):
                    Qubits.__used_qubits.append(id)
                else:
                    print("Qubit already used!")
            else:
                id = self.getLowestIdAvailable()
                Qubits.__used_qubits.append(id)
            return id
        else:
            print("All qubits have already been used!")
            return None

    def getLowestIdAvailable(self):
        all = list(range(1, Qubits.__q_number + 1))
        for i in Qubits.__used_qubits:
            all.remove(i)
        return min(all)

    def getBiggestIdAvailable(self):
        all = list(range(1, Qubits.__q_number + 1))
        for i in Qubits.__used_qubits:
            all.remove(i)
        return max(all)

    def getQubitsNumber(self):
        return Qubits.__q_number

    def getUsedQubits(self):
        return len(Qubits.__used_qubits)

    def setMeasuredQubits(self, target):
        if(isinstance(target, list)):
            for id in target:
                Qubits.__measured_qubits.append(id)
        else:
            Qubits.__measured_qubits.append(target)

    def getMeasuredQubits(self):
        return Qubits.__measured_qubits

    def isMeasured(self, target):
        if (isinstance(target, list)):
            for id in target:
                if(id in Qubits.__measured_qubits):
                    print("Qubit "+str(id)+" alredy measured!")
                    return True
        else:
            if(target in Qubits.__measured_qubits):
                return True
        return False

    def setMeasuredValues(self, value):
        Qubits.__measured_values = value

    def getMeasuredValues(self):
        return Qubits.__measured_values

    def isSymbolic(self):
        return Qubits.__symbolic == True

    def setPsi(self, psi):
        if (not Qubits.__symbolic):
            Qubits.__psi = sp.Matrix(psi)
        else:
            Qubits.__psi = cp.array(psi)

    def getPsi(self):
        return Qubits.__psi

    def getPsiAtAngles(self, degree = False):
        angles = []
        if (not Qubits.__symbolic):
            angles = cp.angle(Qubits.__psi)
            if(degree):
                angles = angles*180/pi
        return angles

    def getPsiAdjoint(self):
        if(self.getCuda()):
            result = Qubits.__psi.transpose().conj()
        else:
            result = Qubits.__psi.adjoint()
        return result

    def setOperation(self, operator):
        Qubits.__psi = self.product(operator, Qubits.__psi)
        Qubits.__last_operator = operator

    def qubitsToList(self, values):
        result = []
        for value in values:
            if (isinstance(value, Qubit)):
                result.append(value.getId())
            else:
                result.append(value)
        return result

    def setSymbolValuesForAll(self, a, b):
        if(Qubits.__symbolic):
            for i in range(1, Qubits.__q_number+1):
                if (Qubits.first_left):
                    Qubits.__psi = Qubits.__psi.subs(str(i)+"a"+str(i)+"_0", a)
                    Qubits.__psi = Qubits.__psi.subs(str(i)+"a"+str(i)+"_1", a)
                    Qubits.__psi = Qubits.__psi.subs(str(i)+"b"+str(i)+"_0", b)
                    Qubits.__psi = Qubits.__psi.subs(str(i)+"b"+str(i)+"_1", b)
                else:
                    Qubits.__psi = Qubits.__psi.subs(str(Qubits.__q_number+1-i)+"a"+str(i)+"_0", a)
                    Qubits.__psi = Qubits.__psi.subs(str(Qubits.__q_number+1-i)+"a"+str(i)+"_1", a)
                    Qubits.__psi = Qubits.__psi.subs(str(Qubits.__q_number+1-i)+"b"+str(i)+"_0", b)
                    Qubits.__psi = Qubits.__psi.subs(str(Qubits.__q_number+1-i)+"b"+str(i)+"_1", b)
        else:
            print("This session is not symbolic!")

    def setSymbolValuesForListId(self, id, a, b):
        if(Qubits.__symbolic):
            list_id = self.qubitsToList(id)
            for i in list_id:
                if (Qubits.first_left):
                    Qubits.__psi = Qubits.__psi.subs(str(i)+"a"+str(i)+"_0", a)
                    Qubits.__psi = Qubits.__psi.subs(str(i)+"a"+str(i)+"_1", a)
                    Qubits.__psi = Qubits.__psi.subs(str(i)+"b"+str(i)+"_0", b)
                    Qubits.__psi = Qubits.__psi.subs(str(i)+"b"+str(i)+"_1", b)
                else:
                    Qubits.__psi = Qubits.__psi.subs(str(Qubits.__q_number+1-i)+"a"+str(i)+"_0", a)
                    Qubits.__psi = Qubits.__psi.subs(str(Qubits.__q_number+1-i)+"a"+str(i)+"_1", a)
                    Qubits.__psi = Qubits.__psi.subs(str(Qubits.__q_number+1-i)+"b"+str(i)+"_0", b)
                    Qubits.__psi = Qubits.__psi.subs(str(Qubits.__q_number+1-i)+"b"+str(i)+"_1", b)
        else:
            print("This session is not symbolic!")

    def setSymbolValue(self, id, symbol, value):
        if(Qubits.__symbolic):
            list_id = self.qubitsToList(id)
            for i in list_id:
                if (Qubits.first_left):
                    Qubits.__psi = Qubits.__psi.subs(str(i)+symbol+str(i)+"_0", value)
                    Qubits.__psi = Qubits.__psi.subs(str(i)+symbol+str(i)+"_1", value)
                else:
                    Qubits.__psi = Qubits.__psi.subs(str(Qubits.__q_number+1-i)+symbol+str(i)+"_0", value)
                    Qubits.__psi = Qubits.__psi.subs(str(Qubits.__q_number+1-i)+symbol+str(i)+"_1", value)
        else:
            print("This session is not symbolic!")

    def PrintState(self, simple = False):
        if(not self.__symbolic):
            value = Utils.vec2tex(Qubits.__psi)
        else:
            value = Utils.texfix(Qubits.__psi, self.__q_number, Qubits.first_left)

        if(not simple):
            display(Math(value))
        else:
            print(value)

    def PrintLastOperator(self, tex = True):
        if(tex):
            value = sp.latex(Qubits.__last_operator)
            display(Math(value))
        else:
            print(Qubits.__last_operator)


class Qubit(Qubits, Gates, Circuit):
    def __init__(self, id = None):
        self.__id = self.addQubit(id)
        self.__name = "q"+str(self.__id)

    def __eq__(self, other):
        return self.__id == other

    def setName(self, name):
        self.__name = name

    def getName(self):
        return self.__name

    def getId(self):
        return self.__id

    def setSymbolValues(self, a, b):
        self.setSymbolValuesForListId([self.__id], a, b)

    def X(self):
        self.addOp("X", [self.__id])
        operator = super().X(self.__id)
        self.setOperation(operator)

    def Y(self):
        self.addOp("Y", [self.__id])
        operator = super().Y(self.__id)
        self.setOperation(operator)

    def Z(self):
        self.addOp("Z", [self.__id])
        operator = super().Z(self.__id)
        self.setOperation(operator)

    def V(self, target):
        self.addOp("V", [self.__id])
        operator = super().V(self.__id)
        self.setOperation(operator)

    def S(self, target):
        self.addOp("S", [self.__id])
        operator = super().S(self.__id)
        self.setOperation(operator)

    def T(self, target):
        self.addOp("T", [self.__id])
        operator = super().T(self.__id)
        self.setOperation(operator)

    def H(self):
        self.addOp("H", [self.__id])
        operator = super().H(self.__id)
        self.setOperation(operator)

    def U(self, *argv):
        self.addOp("U", self.qubitsToList([self.__id, argv]))
        operator = super().U(self.__id, argv)
        self.setOperation(operator)

    def U3(self, theta, phi, _lambda):
        self.addOp("U3", self.qubitsToList([self.__id, theta, phi, _lambda]))
        operator = super().U3(self.__id, theta, phi, _lambda)
        self.setOperation(operator)

    def U2(self, phi, _lambda):
        self.addOp("U2", self.qubitsToList([self.__id, phi, _lambda]))
        operator = super().U2(self.__id, phi, _lambda)
        self.setOperation(operator)

    def U1(self, _lambda):
        self.addOp("U1", self.qubitsToList([self.__id, _lambda]))
        operator = super().U1(self.__id, _lambda)
        self.setOperation(operator)

    def RX(self, theta):
        self.addOp("RX", self.qubitsToList([self.__id, theta]))
        operator = super().RX(self.__id, theta)
        self.setOperation(operator)

    def RY(self, theta):
        self.addOp("RY", self.qubitsToList([self.__id, theta]))
        operator = super().RY(self.__id, theta)
        self.setOperation(operator)

    def RZ(self, phi):
        self.addOp("RZ", self.qubitsToList([self.__id, phi]))
        operator = super().RZ(self.__id, phi)
        self.setOperation(operator)

    def CX(self, control):
        self.addOp("CX", self.qubitsToList([control, self.__id]))
        operator = super().CX(control, self.__id)
        self.setOperation(operator)

    def CNOT(self, control):
        self.CX(control)

    def CY(self, control):
        self.addOp("CY", self.qubitsToList([control, self.__id]))
        operator = super().CY(control, self.__id)
        self.setOperation(operator)

    def CZ(self, control):
        self.addOp("CZ", self.qubitsToList([control, self.__id]))
        operator = super().CZ(control, self.__id)
        self.setOperation(operator)

    def CRX(self, control, theta):
        self.addOp("CRX", self.qubitsToList([control, self.__id, theta]))
        operator = super().CRX(control, self.__id, theta)
        self.setOperation(operator)

    def CRY(self, control, theta):
        self.addOp("CRY", self.qubitsToList([control, self.__id, theta]))
        operator = super().CRY(control, self.__id, theta)
        self.setOperation(operator)

    def CRZ(self, control, phi):
        self.addOp("CRZ", self.qubitsToList([control, self.__id, phi]))
        operator = super().CRZ(control, self.__id, phi)
        self.setOperation(operator)

    def CU(self, control, *argv):
        self.addOp("CU", self.qubitsToList([control, self.__id]))
        operator = super().CU(control, self.__id, argv)
        self.setOperation(operator)

    def CU3(self, control, theta, phi, _lambda):
        self.addOp("CU3", self.qubitsToList([control, self.__id, theta, phi, _lambda]))
        operator = super().CU3(control, self.__id, theta, phi, _lambda)
        self.setOperation(operator)

    def CU2(self, control, phi, _lambda):
        self.addOp("CU2", self.qubitsToList([control, self.__id, phi, _lambda]))
        operator = super().CU2(control, self.__id, phi, _lambda)
        self.setOperation(operator)

    def CU1(self, control, _lambda):
        self.addOp("CU1", self.qubitsToList([control, self.__id, _lambda]))
        operator = super().CU1(control, self.__id, _lambda)
        self.setOperation(operator)

    def CCX(self, control1, control2):
        self.addOp("CCX", self.qubitsToList([control1, control2, self.__id]))
        operator = super().CCX(control1, control2, self.__id)
        self.setOperation(operator)

    def Toffoli(self, control1, control2):
        self.CCX(control1, control2)

class QubitRegister(Qubit):
    def __init__(self, number = 3):
        self.__number = number
        if(self.getUsedQubits() < self.getQubitsNumber()):
            self.__reg = [Qubit() for i in range(1, number+1)]

    def __getitem__(self, key):
        return self.__reg[key-1]

    def getQubits(self):
        return self.__reg

    def X(self):
        for qubit in self.__reg:
            qubit.X()

    def Y(self):
        for qubit in self.__reg:
            qubit.Y()

    def Z(self):
        for qubit in self.__reg:
            qubit.Z()

    def V(self, target):
        for qubit in self.__reg:
            qubit.V()

    def S(self, target):
        for qubit in self.__reg:
            qubit.S()

    def T(self, target):
        for qubit in self.__reg:
            qubit.T()

    def H(self):
        for qubit in self.__reg:
            qubit.H()
