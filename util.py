#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Allen(Zifeng) An
@course: 
@contact: anz8@mcmaster.ca
@file: matrix.py
@time: 2020/10/12 13:47
'''

from typing import List
import numpy as np
import math

class Matrix():
    def __init__(self, arr: List[List[float]]):
        self.val = arr

    @staticmethod
    def dot_product(v1: List[float], v2: List[float]) -> float:
        assert len(v1) == len(v2)
        res = 0
        for i in range(len(v1)):
            res += v1[i] * v2[i]
        return res

    @staticmethod
    def cross_product(v1: List[float], v2: List[float]) -> List[float]:
        return list(np.array(np.cross(np.array(v1), np.array(v2))).tolist())

    def __mul__(self, other: 'Matrix') -> 'Matrix':
        res = []

        for r in range(len(self.val)):
            temp = []
            for c in range(len(other.val[0])):
                temp.append(Matrix.dot_product(self.val[r], other.transpose().val[c]))
            res.append(temp)
        return Matrix(res)

    def __sub__(self, other: 'Matrix') -> 'Matrix':
        res = [[self.val[r][c] - other.val[r][c] for c in range(len(other.val[0]))] for r in range(len(other.val))]
        return Matrix(res)

    def transpose(self) -> 'Matrix':
        res = []
        for c in range(len(self.val[0])):
            temp = []
            for r in range(len(self.val)):
                temp.append(self.val[r][c])
            res.append(temp)

        return Matrix(res)

    def __str__(self):
        s = ''
        for r in range(len(self.val)):
            for c in range(len(self.val[0])):
                s += str(self.val[r][c]) + ' '
            s += '\n'
        return s


class Vector():
    def __init__(self, arr: List[float]):
        self.val = arr

    def __sub__(self, other: 'Vector') -> 'Vector':
        assert len(self.val) == len(other.val)
        res = [self.val[i] - other.val[i] for i in range(len(other.val))]
        return Vector(res)

    def __str__(self):
        s = ''
        for i in range(len(self.val)):
            s += str(self.val[i]) + ' '
        return s

    def __truediv__(self, divisor: float) -> 'Vector':
        res = [self.val[i] / divisor for i in range(len(self.val))]
        return Vector(res)

    def dot(self, other: 'Vector') -> float:
        assert len(self.val) == len(other.val)
        res = 0
        for i in range(len(self.val)):
            res += self.val[i] * other.val[i]
        return res

    def modulus(self):
        return math.sqrt(sum([self.val[i] ** 2 for i in range(len(self.val))]))


# a=Matrix([[1,2],[3,4]])
# b=Matrix([[1],[2]])
if __name__ == '__main__':
    a = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    b = Matrix([[1], [2], [3]])
    c = Matrix([[2], [3], [8]])

    # print(a*b)
    # ans= Matrix.cross_product([1,2,3],[4,5,6])
    # print(ans,type(ans))

    print(b - c)
