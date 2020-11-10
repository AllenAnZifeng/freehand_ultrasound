import open3d as o3d
import numpy as np
from open3d.cpu.pybind.geometry import PointCloud
from open3d.cpu.pybind.utility import DoubleVector

POINT_CLOUD_PATH = '3d_coordinate.xyz'

if __name__ == '__main__':
    pcd = o3d.io.read_point_cloud(POINT_CLOUD_PATH)  # type:PointCloud
    pcd.estimate_normals()
    pcd.orient_normals_consistent_tangent_plane(100)
    alpha = 0.3
    radii = [0.005, 0.01, 0.02, 0.04]
    o3d.visualization.draw_geometries([pcd], mesh_show_back_face=True, point_show_normal=True)

    # tetra_mesh, pt_map = o3d.geometry.TetraMesh().create_from_point_cloud(pcd)
    mesh,densities = o3d.geometry.TriangleMesh().create_from_point_cloud_poisson(pcd, 9)
    vertices_to_remove = densities < np.quantile(densities, 0.01)
    mesh.remove_vertices_by_mask(vertices_to_remove)
    mesh.compute_vertex_normals()
    mesh.paint_uniform_color([0.5, 0.5, 0.5])

    o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True, point_show_normal=True)
