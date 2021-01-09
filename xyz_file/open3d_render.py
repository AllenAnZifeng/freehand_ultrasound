#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Allen(Zifeng) An
@course: 
@contact: anz8@mcmaster.ca
@file: open3d_render.py
@time: 2021/1/9 21:30
'''
import copy

from open3d.cpu.pybind.geometry import TriangleMesh
from open3d.cpu.pybind.utility import Vector3dVector,Vector3iVector
import open3d as o3d
import numpy as np
from typing import List
import math

def scale(geometry_obj, scale_x: float = 1, scale_y: float = 1, scale_z: float = 1):
    T = np.eye(4)
    T[0, 0] = scale_x
    T[1, 1] = scale_y
    T[2, 2] = scale_z
    return copy.deepcopy(geometry_obj).transform(T)

def distance_squared(p1_id:int,p2_id:int)->int:
    return (point_cloud_array[p1_id][0]-point_cloud_array[p2_id][0])**2+(point_cloud_array[p1_id][1]-point_cloud_array[p2_id][1])**2+(point_cloud_array[p1_id][2]-point_cloud_array[p2_id][2])**2


def closest_next_frame_points(point_id:int,next_layer_id:int,number_of_points_to_return:int)->List[int]: # return close points id

    if next_layer_id in layered_point_array:
        points_id_in_next_frame = layered_point_array[next_layer_id]
    else:
        return []

    distance_id_tuple = []
    for id in points_id_in_next_frame:
        distance_id_tuple.append((distance_squared(point_id,id),id))
    distance_id_tuple.sort(key=lambda x:x[0])
    # print(distance_id_tuple)
    distance_id_tuple = distance_id_tuple[:number_of_points_to_return]
    return [ x[1] for x in distance_id_tuple]

if __name__ == '__main__':
    point_cloud_array= [] # index -> point id
    with open('trial1_azf.xyz', 'r') as file:
        for line in file.readlines():
            point = line.split()
            point = [int(x) for x in point]
            point_cloud_array.append(point)

    layered_point_array = {}
    for i in range(len(point_cloud_array)):
        if point_cloud_array[i][-1] not in layered_point_array:
            layered_point_array[point_cloud_array[i][-1]] = [i]
        else:
            layered_point_array[point_cloud_array[i][-1]].append(i)

    # print(point_cloud_array)
    # print(layered_point_array[2])

    triangle_array =[]

    for layer_number in range(1,len(layered_point_array)):
        for point_id in layered_point_array[layer_number]:

            fetched_points = closest_next_frame_points(point_id,layer_number+1,3)
            tri1 = [point_id,fetched_points[0],fetched_points[1]]
            tri2 = [point_id,fetched_points[1],fetched_points[2]]
            triangle_array.append(tri1)
            triangle_array.append(tri2)

    for layer_number in range(len(layered_point_array),1,-1):
        for point_id in layered_point_array[layer_number]:
            fetched_points = closest_next_frame_points(point_id,layer_number-1,3)

            tri1 = [point_id, fetched_points[0], fetched_points[1]]
            tri2 = [point_id, fetched_points[1], fetched_points[2]]

            triangle_array.append(tri1)
            triangle_array.append(tri2)


    # print(triangle_array)
    # print(len(point_cloud_array))

    vertices = Vector3dVector(np.array(point_cloud_array))
    triangles = Vector3iVector(np.array(triangle_array))
    mesh = TriangleMesh(vertices,triangles)
    mesh=scale(mesh, 0.077, 0.077, 0.21)
    mesh.paint_uniform_color([1, 0.706, 0])
    o3d.visualization.draw_geometries([mesh],mesh_show_back_face=True,point_show_normal=True,mesh_show_wireframe=True)
