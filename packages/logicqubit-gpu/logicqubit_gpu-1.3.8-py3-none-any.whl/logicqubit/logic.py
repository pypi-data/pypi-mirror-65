#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Author Cleoner S. Pietralonga
# e-mail: cleonerp@gmail.com
# Apache License

import sympy as sp
from sympy.physics.quantum import TensorProduct
from cmath import *
import matplotlib.pyplot as plt

from logicqubit.qubits import *
from logicqubit.gates import *
from logicqubit.circuit import *
from logicqubit.zhegalkin import *
from logicqubit.oracle import *
from logicqubit.utils import *

class LogicQuBit(Qubits, Gates, Circuit):

    def __init__(self, qubits_number = 3, **kwargs):
        self.__cuda = kwargs.get('cuda', True)
        self.__symbolic = kwargs.get('symbolic', False)
        self.__first_left = kwargs.get('first_left', True)  # o qubit 1 é o mais a esquerda
        self.__qubits_number = qubits_number
        if(self.__symbolic):
            self.__cuda = False
        super().setCuda(self.__cuda)
        super().__init__(qubits_number, self.__symbolic, self.__first_left)
        Gates.__init__(self, qubits_number, self.__first_left)
        Circuit.__init__(self)

    def X(self, target):
        self.addOp("X", self.qubitsToList([target]))
        operator = super().X(target)
        self.setOperation(operator)

    def Y(self, target):
        self.addOp("Y", self.qubitsToList([target]))
        operator = super().Y(target)
        self.setOperation(operator)

    def Z(self, target):
        self.addOp("Z", self.qubitsToList([target]))
        operator = super().Z(target)
        self.setOperation(operator)

    def V(self, target):
        self.addOp("V", self.qubitsToList([target]))
        operator = super().V(target)
        self.setOperation(operator)

    def S(self, target):
        self.addOp("S", self.qubitsToList([target]))
        operator = super().S(target)
        self.setOperation(operator)

    def T(self, target):
        self.addOp("T", self.qubitsToList([target]))
        operator = super().T(target)
        self.setOperation(operator)

    def H(self, target):
        self.addOp("H", self.qubitsToList([target]))
        operator = super().H(target)
        self.setOperation(operator)

    def U(self, target, *argv):
        self.addOp("U", self.qubitsToList([target, argv]))
        operator = super().U(target, argv)
        self.setOperation(operator)

    def U3(self, target, theta, phi, _lambda):
        self.addOp("U3", self.qubitsToList([target, theta, phi, _lambda]))
        operator = super().U3(target, theta, phi, _lambda)
        self.setOperation(operator)

    def U2(self, target, phi, _lambda):
        self.addOp("U2", self.qubitsToList([target, phi, _lambda]))
        operator = super().U2(target, phi, _lambda)
        self.setOperation(operator)

    def U1(self, target, _lambda):
        self.addOp("U1", self.qubitsToList([target, _lambda]))
        operator = super().U1(target, _lambda)
        self.setOperation(operator)

    def RX(self, target, theta):
        self.addOp("RX", self.qubitsToList([target, theta]))
        operator = super().RX(target, theta)
        self.setOperation(operator)

    def RY(self, target, theta):
        self.addOp("RY", self.qubitsToList([target, theta]))
        operator = super().RY(target, theta)
        self.setOperation(operator)

    def RZ(self, target, phi):
        self.addOp("RZ", self.qubitsToList([target, phi]))
        operator = super().RZ(target, phi)
        self.setOperation(operator)

    def CX(self, control, target):
        self.addOp("CX", self.qubitsToList([control, target]))
        operator = super().CX(control, target)
        self.setOperation(operator)

    def CNOT(self, control, target):
        self.CX(control, target)

    def CY(self, control, target):
        self.addOp("CY", self.qubitsToList([control, target]))
        operator = super().CY(control, target)
        self.setOperation(operator)

    def CZ(self, control, target):
        self.addOp("CZ", self.qubitsToList([control, target]))
        operator = super().CZ(control, target)
        self.setOperation(operator)

    def CRX(self, control, target, theta):
        self.addOp("CRX", self.qubitsToList([control, target, theta]))
        operator = super().CRX(control, target, theta)
        self.setOperation(operator)

    def CRY(self, control, target, theta):
        self.addOp("CRY", self.qubitsToList([control, target, theta]))
        operator = super().CRY(control, target, theta)
        self.setOperation(operator)

    def CRZ(self, control, target, phi):
        self.addOp("CRZ", self.qubitsToList([control, target, phi]))
        operator = super().CRZ(control, target, phi)
        self.setOperation(operator)

    def CU(self, control, target, *argv):
        self.addOp("CU", self.qubitsToList([control, target]))
        operator = super().CU(control, target, argv)
        self.setOperation(operator)

    def CU3(self, control, target, theta, phi, _lambda):
        self.addOp("CU3", self.qubitsToList([control, target, theta, phi, _lambda]))
        operator = super().CU3(control, target, theta, phi, _lambda)
        self.setOperation(operator)

    def CU2(self, control, target, phi, _lambda):
        self.addOp("CU2", self.qubitsToList([control, target, phi, _lambda]))
        operator = super().CU2(control, target, phi, _lambda)
        self.setOperation(operator)

    def CU1(self, control, target, _lambda):
        self.addOp("CU1", self.qubitsToList([control, target, _lambda]))
        operator = super().CU1(control, target, _lambda)
        self.setOperation(operator)

    def CCX(self, control1, control2, target):
        self.addOp("CCX", self.qubitsToList([control1, control2, target]))
        operator = super().CCX(control1, control2, target)
        self.setOperation(operator)

    def Toffoli(self, control1, control2, target):
        self.CCX(control1, control2, target)

    def addOracle(self, oracle):
        targets, input_qubits, truth_table = oracle.get()
        poly = Zhegalkin_Poly()
        for bits in truth_table:
            poly.addTable(bits)
        result = poly.Compute()
        for target, p in enumerate(result):
            for i, value in reversed(list(enumerate(p))):
                if(value==1):
                    blist = [int(i, base=2) for i in bin(i)[2:].zfill(len(input_qubits))]
                    if(bin(i).count("1") == 2):
                        try:
                            q1 = blist.index(1)
                            q2 = blist[q1+1:].index(1)+q1+1
                            self.CCX(input_qubits[q1], input_qubits[q2], targets[target])
                        except:
                            print('fail')
                    elif(bin(i).count("1")==1):
                        try:
                            q = blist.index(1)
                            self.CX(input_qubits[q], targets[target])
                        except:
                            print('fail')
                    elif(i==0):
                        self.X(targets[target])

    def DensityMatrix(self):
        density_m = self.getPsi() * self.getPsiAdjoint()
        return density_m

    def Measure_One(self, target):
        if(not self.isMeasured(target)):
            self.addOp("Measure", self.qubitsToList([target]))
            density_m = self.DensityMatrix()
            list = self.getOrdListSimpleGate(target, super().P0())
            P0 = self.kronProduct(list)
            list = self.getOrdListSimpleGate(target, super().P1())
            P1 = self.kronProduct(list)
            measure_0 = (density_m*P0).trace()
            measure_1 = (density_m*P1).trace()
            self.setMeasuredQubits(target)
            self.setMeasuredValues([measure_0, measure_1])
            return [measure_0, measure_1]

    def Measure2(self, target):
        target = self.qubitsToList(target)
        self.setMeasuredQubits(target)
        target.sort()
        self.addOp("Measure", target)
        density_m = self.DensityMatrix()
        size_p = len(target)  # número de qubits a ser medidos
        size = 2 ** size_p  # número de estados possíveis
        result = []
        for i in range(size):
            tlist = [self.ID() for tl in range(self.__qubits_number)]
            blist = [i >> bl & 0x1 for bl in range(size_p)]  # bit list, bits de cada i
            cnt = 0
            if (self.__first_left):
                sing = 1
                offset_list = 0
                offset_cnt = 0
                plist = range(self.__qubits_number)
            else:
                sing = -1
                offset_list = self.__qubits_number-1
                offset_cnt = len(target)-1
                plist = reversed(range(self.__qubits_number))
            for j in plist:
                if j + 1 == target[offset_cnt+sing*cnt]:
                    if blist[size_p-1-cnt] == 0:  # mais significativo primeiro
                        tlist[offset_list+sing*j] = super().P0()
                    else:
                        tlist[offset_list+sing*j] = super().P1()
                    cnt += 1
                    if (cnt >= size_p):
                        break
            M = self.kronProduct(tlist)
            measure = (density_m * M).trace()  # valor esperado
            if(self.__cuda):
                measure = measure.item().real
            result.append(measure)
        self.setMeasuredValues(result)
        return result

    def Measure(self, target, fisrt_msb = False):  # ex: medir 3 qubits de 5: 2,1,4 do estado "010" -> M010 = |1><1| x |0><0| x 1 x |0><0| x 1
        target = self.qubitsToList(target)
        if(fisrt_msb):  # se fisrt_msb=True -> o primeiro da lista será o mais significativo
            target.reverse()
        self.setMeasuredQubits(target)
        self.addOp("Measure", target)
        density_m = self.DensityMatrix()
        size_p = len(target)  # número de qubits a ser medidos
        size = 2 ** size_p  # número de estados possíveis
        result = []
        for i in range(size):
            tlist = [self.ID() for tl in range(self.__qubits_number)]
            blist = [i >> bl & 0x1 for bl in range(size_p)]  # bit list, bits de cada i
            for j, value in enumerate(target):
                if blist[j] == 0:  # mais significativo primeiro
                    tlist[value-1] = super().P0()
                else:
                    tlist[value-1] = super().P1()
            if (not self.__first_left):
                tlist.reverse()
            M = self.kronProduct(tlist)
            measure = (density_m * M).trace()  # valor esperado
            if(self.__cuda):
                measure = measure.item().real
            result.append(measure)
        self.setMeasuredValues(result)
        return result

    def Plot(self, big_endian=False):
        size_p = len(self.getMeasuredQubits())  # número de bits medidos
        if(size_p > 0):
            size = 2 ** size_p
            if(big_endian):
                names = ["|" + ''.join(list(reversed("{0:b}".format(i).zfill(size_p)))) + ">" for i in range(size)]
            else:
                names = ["|" + "{0:b}".format(i).zfill(size_p) + ">" for i in range(size)]
            values = self.getMeasuredValues()
            #plt.figure(figsize = (5, 3))
            plt.bar(names, values)
            plt.xticks(rotation=50)
            plt.suptitle('')
            plt.show()
        else:
            print("No qubit measured!")

    def Pure(self):
        density_m = self.DensityMatrix()
        pure = (density_m*density_m).trace()
        return pure