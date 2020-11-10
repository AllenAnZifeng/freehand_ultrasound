import copy

import open3d as o3d
import numpy as np
from open3d.cpu.pybind.geometry import PointCloud
from open3d.cpu.pybind.utility import DoubleVector

POINT_CLOUD_PATH = '3d_coordinate.xyz'


def scale(geometry_obj, scale_x: float = 1, scale_y: float = 1, scale_z: float = 1):
    T = np.eye(4)
    T[0, 0] = scale_x
    T[1, 1] = scale_y
    T[2, 2] = scale_z
    return copy.deepcopy(geometry_obj).transform(T)


if __name__ == '__main__':
    pcd = o3d.io.read_point_cloud(POINT_CLOUD_PATH)  # type:PointCloud

    # estimate surface normals
    pcd.estimate_normals()
    # pcd.orient_normals_consistent_tangent_plane(100)
    # o3d.visualization.draw_geometries([pcd], mesh_show_back_face=True, point_show_normal=True)

    # Enable one of following algorithms

    # Use Ball pivoting
    # radii = [1,2,3,4,5]
    # mesh = o3d.geometry.TriangleMesh().create_from_point_cloud_ball_pivoting(
    #     pcd, o3d.utility.DoubleVector(radii))

    # Use Poisson surface reconstruction
    depth = 10
    min_density_percentile = 0.05
    mesh, densities = o3d.geometry.TriangleMesh().create_from_point_cloud_poisson(pcd, depth=depth)
    vertices_to_remove = densities < np.quantile(densities, min_density_percentile)
    mesh.remove_vertices_by_mask(vertices_to_remove)

    # Show result before scaling
    mesh.compute_vertex_normals()
    mesh.paint_uniform_color([0.5, 0.5, 0.5])
    o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True, point_show_normal=True)

    # Transform and show result after scaling
    z_scale = 4
    mesh_t = scale(mesh, scale_z=z_scale)
    # o3d.visualization.draw_geometries([mesh_t], mesh_show_back_face=True)
