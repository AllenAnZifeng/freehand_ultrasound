import copy
from typing import List, Tuple

import open3d as o3d
import numpy as np
from open3d.cpu.pybind.geometry import TriangleMesh
from open3d.cpu.pybind.utility import Vector3dVector, Vector3iVector

def scale(geometry_obj, scale_x: float = 1, scale_y: float = 1, scale_z: float = 1):
    T = np.eye(4)
    T[0, 0] = scale_x
    T[1, 1] = scale_y
    T[2, 2] = scale_z
    return copy.deepcopy(geometry_obj).transform(T)

class LayeredPoints:
    def __init__(self, points: List[Tuple[int, int, int]]):
        self.points = points
        self.layers = {}
        for i in range(len(points)):
            p = points[i]
            x, y, z = p
            if z not in self.layers:
                self.layers[z] = []
            self.layers[z].append(i)

    def get_closest_n_points_from(self, p_origin_i: int, p_dest_is: List[int], n: int) -> List[int]:
        p_sorted_is = sorted(p_dest_is,
                             key=lambda p_dest_i: self.point_distance_squared(p_origin_i, p_dest_i))
        return p_sorted_is[:n]

    @classmethod
    def from_xyz_file(cls, path: str) -> 'LayeredPoints':
        with open(path) as f:
            rows = f.readlines()
            points = []
            for row in rows:
                point = tuple([int(v) for v in row.split(' ')])
                assert len(point) == 3
                points.append(point)
            return cls(points)

    def point_distance_squared(self, p1_i: int, p2_i: int) -> int:
        p1, p2 = self.points[p1_i], self.points[p2_i]
        return sum([(a - b) ** 2 for a, b in zip(p1, p2)])


def make_triangles(points: LayeredPoints, l1: int, l2: int) -> List[Tuple[int, int, int]]:
    triangles = []

    l1_point_is = points.layers[l1]
    l2_point_is = points.layers[l2]

    for p_i in l1_point_is:
        p_dest_1, p_dest_2 = points.get_closest_n_points_from(p_i, l2_point_is, 2)
        triangles.append((p_i, p_dest_1, p_dest_2))

    for p_i in l2_point_is:
        p_dest_1, p_dest_2 = points.get_closest_n_points_from(p_i, l1_point_is, 2)
        triangles.append((p_i, p_dest_1, p_dest_2))

    return triangles

def make_triangles_overlap(points: LayeredPoints, l1: int, l2: int) -> List[Tuple[int, int, int]]:
    triangles = []

    l1_point_is = points.layers[l1]
    l2_point_is = points.layers[l2]

    for p_i in l1_point_is:
        p_dest_1, p_dest_2, p_dest_3 = points.get_closest_n_points_from(p_i, l2_point_is, 3)
        triangles.append((p_i, p_dest_1, p_dest_2))
        triangles.append((p_i, p_dest_2, p_dest_3))

    for p_i in l2_point_is:
        p_dest_1, p_dest_2, p_dest_3 = points.get_closest_n_points_from(p_i, l1_point_is, 3)
        triangles.append((p_i, p_dest_1, p_dest_2))
        triangles.append((p_i, p_dest_2, p_dest_3))

    return triangles

if __name__ == '__main__':
    #     vertices_array = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
    #     triangles_array = np.array([[0, 1, 2]])
    #
    #     vertices = Vector3dVector(vertices_array)
    #     triangles = Vector3iVector(triangles_array)
    #
    #     mesh = TriangleMesh(vertices, triangles)
    #     mesh.paint_uniform_color([0.5, 0.5, 0.5])
    #     # mesh.compute_vertex_normals()
    #     o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True, point_show_normal=True,
    #                                       mesh_show_wireframe=True)
    POINT_CLOUD_PATH = 'xyz_file/trial1_azf.xyz'
    points = LayeredPoints.from_xyz_file(POINT_CLOUD_PATH)

    layers = list(points.layers.keys())
    layers.sort()

    triangles = []

    for layer_i in range(len(layers) - 1):
        current_l = layers[layer_i]
        next_l = layers[layer_i + 1]
        triangles.extend(make_triangles_overlap(points, current_l, next_l))

    vertices_array = np.array(points.points)
    triangles_array = np.array(triangles)

    vertices = Vector3dVector(vertices_array)
    triangles = Vector3iVector(triangles_array)

    mesh = TriangleMesh(vertices, triangles)
    mesh = scale(mesh,0.077,0.077,0.21)
    mesh.paint_uniform_color([0.5, 0.5, 0.5])
    mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True, point_show_normal=True)