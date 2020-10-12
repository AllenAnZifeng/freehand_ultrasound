# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Allen(Zifeng) An
@course: 
@contact: anz8@mcmaster.ca
@file: transformation.py
@time: 2020/10/12 14:28
'''
from typing import List
from util import Matrix, Vector

global_i = Vector([1, 0, 0])
global_j = Vector([0, 1, 0])
global_k = Vector([0, 0, 1])


# vector b coordinate serves as the origin for the LCS
def Matrix_LCS_TO_GCS(a: Vector, b: Vector, c: Vector):
    v1 = a - b
    v2 = c - b
    v3 = Vector(Matrix.cross_product(v1.val, v2.val))
    v4 = Vector(Matrix.cross_product(v3.val, v1.val))

    x = v3
    y = v1
    z = v4

    local_i = x / x.modulus()
    local_j = y / y.modulus()
    local_k = z / z.modulus()

    matrix_arr = [[global_i.dot(local_i), global_i.dot(local_j), global_i.dot(local_k), b.val[0]],
                  [global_j.dot(local_i), global_j.dot(local_j), global_j.dot(local_k), b.val[1]],
                  [global_k.dot(local_i), global_k.dot(local_j), global_k.dot(local_k), b.val[2]],
                  [0, 0, 0, 1]]

    return Matrix(matrix_arr)


if __name__ == '__main__':
    a = Vector([1, 2, 3])
    b = Vector([1, 0, 1])
